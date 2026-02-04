#!/usr/bin/env python3
"""
Health Coach Agent MCP Server
Provides coaching, motivation, and goal management.
"""

from fastmcp import FastMCP
from typing import Dict, Any, List
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.database import SessionLocal, User, HealthGoal, WearableData
from datetime import datetime, timedelta

mcp = FastMCP("Health Coach Agent")


@mcp.tool()
def create_health_goal(
    user_id: int,
    goal_type: str,
    description: str,
    target_value: float = None,
    timeline_days: int = 30
) -> Dict[str, Any]:
    """
    Create a new health goal for the user.
    
    Args:
        user_id: User ID
        goal_type: Type of goal (sleep, exercise, nutrition, weight)
        description: Goal description
        target_value: Target value (optional)
        timeline_days: Days to achieve goal
    
    Returns:
        Created goal information
    """
    db = SessionLocal()
    try:
        # Get current baseline
        start_date = datetime.now() - timedelta(days=7)
        recent_data = db.query(WearableData).filter(
            WearableData.user_id == user_id,
            WearableData.date >= start_date
        ).all()
        
        current_value = None
        if goal_type == "sleep" and recent_data:
            sleep_hours = [d.sleep_hours for d in recent_data if d.sleep_hours]
            if sleep_hours:
                current_value = sum(sleep_hours) / len(sleep_hours)
        elif goal_type == "exercise" and recent_data:
            steps = [d.steps for d in recent_data if d.steps]
            if steps:
                current_value = sum(steps) / len(steps)
        
        # Create goal
        goal = HealthGoal(
            user_id=user_id,
            goal_type=goal_type,
            description=description,
            target_value=target_value,
            current_value=current_value,
            timeline_days=timeline_days,
            status="active"
        )
        
        db.add(goal)
        db.commit()
        db.refresh(goal)
        
        return {
            "goal_id": goal.id,
            "goal_type": goal_type,
            "description": description,
            "current_value": current_value,
            "target_value": target_value,
            "timeline_days": timeline_days,
            "created_at": goal.created_at.isoformat(),
            "milestones": generate_milestones(goal_type, current_value, target_value, timeline_days)
        }
        
    finally:
        db.close()


def generate_milestones(goal_type: str, current: float, target: float, days: int) -> List[Dict]:
    """Generate milestones for goal achievement."""
    if not current or not target:
        return []
    
    milestones = []
    steps = 4  # Number of milestones
    increment = (target - current) / steps
    
    for i in range(1, steps + 1):
        milestone_value = current + (increment * i)
        milestone_day = int((days / steps) * i)
        
        milestones.append({
            "day": milestone_day,
            "target_value": round(milestone_value, 1),
            "description": f"Reach {round(milestone_value, 1)} by day {milestone_day}"
        })
    
    return milestones


@mcp.tool()
def get_active_goals(user_id: int) -> Dict[str, Any]:
    """
    Get all active goals for a user.
    
    Args:
        user_id: User ID
    
    Returns:
        List of active goals
    """
    db = SessionLocal()
    try:
        goals = db.query(HealthGoal).filter(
            HealthGoal.user_id == user_id,
            HealthGoal.status == "active"
        ).all()
        
        return {
            "user_id": user_id,
            "active_goals": [{
                "goal_id": g.id,
                "goal_type": g.goal_type,
                "description": g.description,
                "target_value": g.target_value,
                "current_value": g.current_value,
                "days_remaining": (g.created_at + timedelta(days=g.timeline_days) - datetime.now()).days,
                "created_at": g.created_at.isoformat()
            } for g in goals]
        }
        
    finally:
        db.close()


@mcp.tool()
def track_progress(user_id: int, goal_id: int) -> Dict[str, Any]:
    """
    Track progress towards a specific goal.
    
    Args:
        user_id: User ID
        goal_id: Goal ID
    
    Returns:
        Progress information
    """
    db = SessionLocal()
    try:
        goal = db.query(HealthGoal).filter(
            HealthGoal.id == goal_id,
            HealthGoal.user_id == user_id
        ).first()
        
        if not goal:
            return {"error": "Goal not found"}
        
        # Get recent data
        since_goal_created = db.query(WearableData).filter(
            WearableData.user_id == user_id,
            WearableData.date >= goal.created_at
        ).all()
        
        if not since_goal_created:
            return {
                "goal_id": goal_id,
                "message": "No data recorded since goal creation"
            }
        
        # Calculate current progress
        current_avg = None
        if goal.goal_type == "sleep":
            sleep_hours = [d.sleep_hours for d in since_goal_created if d.sleep_hours]
            if sleep_hours:
                current_avg = sum(sleep_hours) / len(sleep_hours)
        elif goal.goal_type == "exercise":
            steps = [d.steps for d in since_goal_created if d.steps]
            if steps:
                current_avg = sum(steps) / len(steps)
        
        # Calculate progress percentage
        if current_avg and goal.target_value and goal.current_value:
            progress = ((current_avg - goal.current_value) / (goal.target_value - goal.current_value)) * 100
        else:
            progress = 0
        
        days_elapsed = (datetime.now() - goal.created_at).days
        days_remaining = goal.timeline_days - days_elapsed
        
        return {
            "goal_id": goal_id,
            "goal_type": goal.goal_type,
            "description": goal.description,
            "initial_value": goal.current_value,
            "current_value": round(current_avg, 1) if current_avg else None,
            "target_value": goal.target_value,
            "progress_percent": round(min(progress, 100), 1),
            "days_elapsed": days_elapsed,
            "days_remaining": max(days_remaining, 0),
            "on_track": progress >= (days_elapsed / goal.timeline_days * 100) if progress else False,
            "data_points": len(since_goal_created)
        }
        
    finally:
        db.close()


@mcp.tool()
def generate_motivation(
    user_id: int,
    situation: str = "general"
) -> str:
    """
    Generate motivational message based on situation.
    
    Args:
        user_id: User ID
        situation: Situation type (general, struggling, success, starting)
    
    Returns:
        Motivational message prompt for LLM
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        goals = db.query(HealthGoal).filter(
            HealthGoal.user_id == user_id,
            HealthGoal.status == "active"
        ).all()
        
        context = {
            "user_name": user.name if user else "there",
            "goals": [g.description for g in goals] if goals else ["improve health"],
            "situation": situation
        }
        
        # Return prompt for LLM to generate personalized motivation
        prompts = {
            "general": f"""Generate a brief, encouraging message for {context['user_name']} who is working on: {', '.join(context['goals'])}. 
Use motivational interviewing techniques: be empathetic, supportive, and help them find their own motivation.""",
            
            "struggling": f"""Generate an empathetic, non-judgmental message for {context['user_name']} who is struggling with: {', '.join(context['goals'])}. 
Acknowledge their challenges, normalize setbacks, and help them identify small, achievable next steps.""",
            
            "success": f"""Generate a celebratory message for {context['user_name']} who made progress on: {', '.join(context['goals'])}. 
Celebrate their effort, link it to their values, and encourage continued momentum.""",
            
            "starting": f"""Generate a welcoming, enthusiastic message for {context['user_name']} who is starting their journey with: {', '.join(context['goals'])}. 
Express confidence in them, normalize the journey, and help set realistic expectations."""
        }
        
        return prompts.get(situation, prompts["general"])
        
    finally:
        db.close()


@mcp.tool()
def get_coaching_insights(user_id: int) -> Dict[str, Any]:
    """
    Get coaching insights based on user's data and goals.
    
    Args:
        user_id: User ID
    
    Returns:
        Coaching insights and recommendations
    """
    db = SessionLocal()
    try:
        # Get recent data
        start_date = datetime.now() - timedelta(days=30)
        data = db.query(WearableData).filter(
            WearableData.user_id == user_id,
            WearableData.date >= start_date
        ).all()
        
        goals = db.query(HealthGoal).filter(
            HealthGoal.user_id == user_id,
            HealthGoal.status == "active"
        ).all()
        
        insights = {
            "consistency": {},
            "trends": {},
            "recommendations": []
        }
        
        if data:
            # Check consistency (how many days have data)
            days_with_data = len(set(d.date.date() for d in data))
            insights["consistency"]["data_recording"] = {
                "days_recorded": days_with_data,
                "days_in_period": 30,
                "consistency_score": round((days_with_data / 30) * 100, 1)
            }
            
            # Analyze sleep consistency
            sleep_data = [d.sleep_hours for d in data if d.sleep_hours]
            if sleep_data:
                import statistics
                insights["consistency"]["sleep"] = {
                    "average": round(sum(sleep_data) / len(sleep_data), 1),
                    "variability": round(statistics.stdev(sleep_data), 2) if len(sleep_data) > 1 else 0
                }
                
                if statistics.stdev(sleep_data) > 1.5 if len(sleep_data) > 1 else False:
                    insights["recommendations"].append(
                        "Your sleep schedule varies significantly. Aim for a consistent bedtime and wake time."
                    )
            
            # Analyze activity patterns
            steps_data = [d.steps for d in data if d.steps]
            if steps_data:
                avg_steps = sum(steps_data) / len(steps_data)
                if avg_steps < 7000:
                    insights["recommendations"].append(
                        "Consider setting a daily step goal. Even small increases can make a big difference!"
                    )
        
        # Goal-specific insights
        for goal in goals:
            days_since_created = (datetime.now() - goal.created_at).days
            if days_since_created > 7:
                insights["recommendations"].append(
                    f"Check in on your goal: {goal.description}. How's it going?"
                )
        
        return insights
        
    finally:
        db.close()


if __name__ == "__main__":
    mcp.run()
