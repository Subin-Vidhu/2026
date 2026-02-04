from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging
import os
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import init_db, get_db, User, WearableData, HealthGoal
from app.models import (
    HealthQueryRequest,
    HealthQueryResponse,
    UploadDataRequest,
    UserStatsResponse,
    HealthGoalCreate
)
from app.mcp_client.orchestrator import MCPClient, HealthAgentOrchestrator
from app.telegram.bot import HealthAgentBot
from datetime import datetime, timedelta
from typing import List

# Setup logging
def _setup_logging() -> None:
    log_level = logging.INFO
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Ensure logs directory exists
    logs_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Date-based log file name (DDMMYYYY)
    log_file_name = f"app_{datetime.now().strftime('%d%m%Y')}.log"
    log_file_path = os.path.join(logs_dir, log_file_name)

    root_logger = logging.getLogger()
    if not root_logger.handlers:
        logging.basicConfig(level=log_level, format=log_format)

    # Avoid duplicate file handlers on reload
    has_file_handler = any(
        isinstance(handler, logging.FileHandler) and getattr(handler, "baseFilename", "") == log_file_path
        for handler in root_logger.handlers
    )
    if not has_file_handler:
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(log_format))
        root_logger.addHandler(file_handler)


_setup_logging()
logger = logging.getLogger(__name__)

settings = get_settings()

# Global instances
mcp_client = MCPClient()
orchestrator = HealthAgentOrchestrator(mcp_client)
telegram_bot = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Personal Health Agent application...")
    
    # Initialize database
    init_db()
    logger.info("Database initialized")
    
    # Start MCP servers
    await mcp_client.start()
    
    # Start Telegram bot if token is provided and valid
    if settings.telegram_bot_token and settings.telegram_bot_token != "your_telegram_bot_token_here":
        global telegram_bot
        try:
            telegram_bot = HealthAgentBot(orchestrator)
            telegram_bot.setup()
            await telegram_bot.start_polling()
            logger.info("Telegram bot started successfully")
        except Exception as e:
            logger.error(f"Failed to start Telegram bot: {e}")
            logger.warning("Continuing without Telegram bot...")
    else:
        logger.warning("No valid Telegram bot token provided. Bot will not start.")
        logger.info("To enable Telegram bot, set TELEGRAM_BOT_TOKEN in .env")
    
    logger.info("Application started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    
    if telegram_bot:
        await telegram_bot.stop()
    
    await mcp_client.stop()
    logger.info("Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="Personal Health Agent API",
    description="Multi-agent health assistant powered by MCP and Ollama",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Personal Health Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "mcp_servers_running": mcp_client.running,
        "telegram_bot_active": telegram_bot is not None
    }


@app.post("/api/query", response_model=HealthQueryResponse)
async def query_health_agent(
    request: HealthQueryRequest
) -> HealthQueryResponse:
    """
    Query the health agent with a user message.
    
    This endpoint routes the query to the appropriate agent(s) and returns the response.
    """
    try:
        response = await orchestrator.process_query(
            user_id=request.user_id,
            message=request.message,
            conversation_history=request.conversation_history
        )
        
        return HealthQueryResponse(
            agent=response["agent"],
            response=response["response"],
            data=response.get("data")
        )
    
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload_data")
async def upload_health_data(
    request: UploadDataRequest,
    db: Session = Depends(get_db)
):
    """
    Upload health data for a user.
    
    Supports: wearable data, medical records
    """
    try:
        if request.data_type == "wearable":
            # Create wearable data entry
            wearable_data = WearableData(
                user_id=request.user_id,
                date=datetime.fromisoformat(request.data.get("date", datetime.now().isoformat())),
                heart_rate=request.data.get("heart_rate"),
                steps=request.data.get("steps"),
                sleep_hours=request.data.get("sleep_hours"),
                hrv=request.data.get("hrv"),
                calories=request.data.get("calories"),
                active_minutes=request.data.get("active_minutes")
            )
            db.add(wearable_data)
            db.commit()
            
            return {"success": True, "message": "Wearable data uploaded successfully"}
        
        else:
            return {"success": False, "message": f"Unsupported data type: {request.data_type}"}
    
    except Exception as e:
        logger.error(f"Error uploading data: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/users/{user_id}/stats", response_model=UserStatsResponse)
async def get_user_stats(
    user_id: int,
    db: Session = Depends(get_db)
) -> UserStatsResponse:
    """Get user health statistics."""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get recent data (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_data = db.query(WearableData).filter(
            WearableData.user_id == user_id,
            WearableData.date >= thirty_days_ago
        ).all()
        
        # Calculate averages
        latest_hr = None
        avg_steps = None
        avg_sleep = None
        
        if recent_data:
            heart_rates = [d.heart_rate for d in recent_data if d.heart_rate]
            if heart_rates:
                latest_hr = heart_rates[-1]
            
            steps_data = [d.steps for d in recent_data if d.steps]
            if steps_data:
                avg_steps = sum(steps_data) / len(steps_data)
            
            sleep_data = [d.sleep_hours for d in recent_data if d.sleep_hours]
            if sleep_data:
                avg_sleep = sum(sleep_data) / len(sleep_data)
        
        # Count active goals
        active_goals = db.query(HealthGoal).filter(
            HealthGoal.user_id == user_id,
            HealthGoal.status == "active"
        ).count()
        
        return UserStatsResponse(
            user_id=user_id,
            total_data_points=len(recent_data),
            latest_heart_rate=latest_hr,
            avg_steps_30d=round(avg_steps, 1) if avg_steps else None,
            avg_sleep_30d=round(avg_sleep, 1) if avg_sleep else None,
            active_goals=active_goals
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/users/{user_id}/goals")
async def create_goal(
    user_id: int,
    goal: HealthGoalCreate,
    db: Session = Depends(get_db)
):
    """Create a new health goal."""
    try:
        new_goal = HealthGoal(
            user_id=user_id,
            goal_type=goal.goal_type,
            description=goal.description,
            target_value=goal.target_value,
            timeline_days=goal.timeline_days,
            status="active"
        )
        db.add(new_goal)
        db.commit()
        db.refresh(new_goal)
        
        return {
            "success": True,
            "goal_id": new_goal.id,
            "message": "Goal created successfully"
        }
    
    except Exception as e:
        logger.error(f"Error creating goal: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/users/{user_id}/goals")
async def get_user_goals(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user's active goals."""
    try:
        goals = db.query(HealthGoal).filter(
            HealthGoal.user_id == user_id,
            HealthGoal.status == "active"
        ).all()
        
        return {
            "user_id": user_id,
            "goals": [{
                "id": g.id,
                "goal_type": g.goal_type,
                "description": g.description,
                "target_value": g.target_value,
                "current_value": g.current_value,
                "timeline_days": g.timeline_days,
                "created_at": g.created_at.isoformat()
            } for g in goals]
        }
    
    except Exception as e:
        logger.error(f"Error getting goals: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
