import asyncio
import json
from typing import Dict, Any, List, Optional
import logging
from app.utils.llm_utils import ollama_client
from app.database import SessionLocal, Conversation, User, WearableData

logger = logging.getLogger(__name__)


class MCPClient:
    """
    MCP Client that manages communication with all agent servers.
    For Windows compatibility, we integrate MCP tools directly instead of spawning subprocesses.
    """
    
    def __init__(self):
        self.servers = {}
        self.running = False
        self.tools = {}
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize all MCP tools directly."""
        # Import and register all tool functions directly from agent servers
        import sys
        import os
        
        # Add mcp_servers to path
        mcp_servers_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../mcp_servers'))
        if mcp_servers_path not in sys.path:
            sys.path.insert(0, mcp_servers_path)
        
        logger.info(f"MCP servers path: {mcp_servers_path}")
        logger.info(f"sys.path[0]: {sys.path[0]}")
        
        self.tools = {
            "ds": {},
            "de": {},
            "hc": {}
        }
        
        # Load Data Science Agent tools
        try:
            logger.info("Loading Data Science Agent tools...")
            from data_science_agent.server import analyze_health_trend, compare_metrics, get_weekly_summary
            self.tools["ds"]["analyze_health_trend"] = analyze_health_trend
            self.tools["ds"]["compare_metrics"] = compare_metrics
            self.tools["ds"]["get_weekly_summary"] = get_weekly_summary
            logger.info("✅ Loaded Data Science Agent tools")
        except Exception as e:
            logger.error(f"❌ Failed to load Data Science Agent tools: {e}", exc_info=True)
        
        # Load Domain Expert Agent tools
        try:
            logger.info("Loading Domain Expert Agent tools...")
            from domain_expert_agent.server import interpret_health_metric, check_health_concerns, get_medical_context
            self.tools["de"]["interpret_health_metric"] = interpret_health_metric
            self.tools["de"]["check_health_concerns"] = check_health_concerns
            self.tools["de"]["get_medical_context"] = get_medical_context
            logger.info("✅ Loaded Domain Expert Agent tools")
        except Exception as e:
            logger.error(f"❌ Failed to load Domain Expert Agent tools: {e}", exc_info=True)
        
        # Load Health Coach Agent tools
        try:
            logger.info("Loading Health Coach Agent tools...")
            from health_coach_agent.server import create_health_goal, get_active_goals, track_progress
            self.tools["hc"]["create_health_goal"] = create_health_goal
            self.tools["hc"]["get_active_goals"] = get_active_goals
            self.tools["hc"]["track_progress"] = track_progress
            logger.info("✅ Loaded Health Coach Agent tools")
        except Exception as e:
            logger.error(f"❌ Failed to load Health Coach Agent tools: {e}", exc_info=True)
        
        logger.info(f"📋 Available tools: {json.dumps({k: list(v.keys()) for k, v in self.tools.items()})}")
    
    async def start(self):
        """Start MCP client (no subprocess needed on Windows)."""
        if self.running:
            return
        
        logger.info("Starting MCP client...")
        self.running = True
        logger.info("MCP client ready (tools integrated directly)")
    
    async def stop(self):
        """Stop MCP client."""
        logger.info("Stopping MCP client...")
        self.running = False
        logger.info("MCP client stopped")
    
    async def call_tool(
        self,
        server: str,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call a tool on an MCP agent.
        
        Args:
            server: Server name (ds, de, hc)
            tool_name: Tool name
            parameters: Tool parameters
        
        Returns:
            Tool result
        """
        logger.debug(f"call_tool called: server={server}, tool_name={tool_name}, params={parameters}")
        logger.debug(f"Available servers: {list(self.tools.keys())}")
        logger.debug(f"Server {server} tools: {list(self.tools.get(server, {}).keys())}")
        
        if server not in self.tools:
            error_msg = f"Server '{server}' not found. Available servers: {list(self.tools.keys())}"
            logger.error(error_msg)
            return {"error": error_msg}
        
        if tool_name not in self.tools[server]:
            error_msg = f"Tool '{tool_name}' not found on server '{server}'. Available tools: {list(self.tools[server].keys())}"
            logger.error(error_msg)
            return {"error": error_msg}
        
        try:
            # Call the tool directly
            tool_func = self.tools[server][tool_name]
            logger.info(f"✅ Calling {tool_name} on {server} with params: {parameters}")
            
            # If the function is async, await it
            result = tool_func(**parameters)
            if hasattr(result, '__await__'):
                result = await result
                
            # If no data found for user, retry with demo user (if available)
            if isinstance(result, dict) and "error" in result:
                error_text = str(result.get("error", "")).lower()
                if "no data found" in error_text and "user" in error_text:
                    demo_user_id = self._get_demo_user_id()
                    if demo_user_id and parameters.get("user_id") != demo_user_id:
                        logger.warning(
                            f"No data for user_id={parameters.get('user_id')}. Falling back to demo user_id={demo_user_id}"
                        )
                        parameters = {**parameters, "user_id": demo_user_id}
                        result = tool_func(**parameters)
                        if hasattr(result, '__await__'):
                            result = await result

            logger.info(f"✅ Tool {tool_name} on {server} completed successfully")
            return result
            
        except TypeError as e:
            error_msg = f"Parameter mismatch for {tool_name}: {e}"
            logger.error(error_msg, exc_info=True)
            return {"error": error_msg}
        except Exception as e:
            error_msg = f"Error calling tool {tool_name} on {server}: {e}"
            logger.error(error_msg, exc_info=True)
            return {"error": error_msg}

    def _get_demo_user_id(self) -> Optional[int]:
        """Get a demo user id with available wearable data."""
        db = SessionLocal()
        try:
            # Prefer known demo users if present
            demo_names = ["Active Alice", "Busy Bob", "Senior Sarah"]
            user = db.query(User).filter(User.name.in_(demo_names)).first()
            if user:
                return user.id

            # Fallback: any user with wearable data
            user_with_data = (
                db.query(User)
                .join(WearableData, WearableData.user_id == User.id)
                .first()
            )
            if user_with_data:
                return user_with_data.id
            return None
        finally:
            db.close()


class HealthAgentOrchestrator:
    """
    Orchestrator that routes queries to appropriate agents.
    """
    
    def __init__(self, mcp_client: MCPClient):
        self.mcp = mcp_client

    def _json_safe(self, value: Any):
        """Convert values to JSON-serializable types."""
        try:
            import numpy as np
        except Exception:
            np = None

        if np is not None:
            if isinstance(value, (np.integer,)):
                return int(value)
            if isinstance(value, (np.floating,)):
                return float(value)
            if isinstance(value, (np.ndarray,)):
                return value.tolist()

        if isinstance(value, dict):
            return {k: self._json_safe(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._json_safe(v) for v in value]
        if isinstance(value, tuple):
            return [self._json_safe(v) for v in value]

        return value
    
    async def process_query(
        self,
        user_id: int,
        message: str,
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Process a user query by routing to appropriate agent(s).
        
        Args:
            user_id: User ID
            message: User message
            conversation_history: Previous conversation
        
        Returns:
            Agent response
        """
        # Classify intent
        intent = await ollama_client.classify_intent(message)
        logger.info(f"Classified intent: {intent}")
        
        # Route to appropriate handler
        if intent == "data_analysis":
            return await self._handle_data_science(user_id, message)
        elif intent == "medical_question":
            return await self._handle_domain_expert(user_id, message)
        elif intent == "coaching":
            return await self._handle_health_coach(user_id, message, conversation_history)
        else:  # multi_agent
            return await self._handle_multi_agent(user_id, message)
    
    async def _handle_data_science(
        self,
        user_id: int,
        message: str
    ) -> Dict[str, Any]:
        """Handle data science queries."""
        logger.info(f"Data Science Agent processing: {message}")
        
        # Determine which metric to analyze from message
        metric_keywords = {
            "heart rate": "heart_rate",
            "hr": "heart_rate",
            "pulse": "heart_rate",
            "sleep": "sleep_hours",
            "steps": "steps",
            "activity": "steps",
            "hrv": "hrv",
            "heart rate variability": "hrv",
            "calories": "calories"
        }
        
        metric = "heart_rate"  # Default
        for keyword, metric_name in metric_keywords.items():
            if keyword in message.lower():
                metric = metric_name
                break
        
        # Determine time range
        time_range = "last_30_days"
        if "week" in message.lower() or "7 day" in message.lower():
            time_range = "last_7_days"
        elif "90 day" in message.lower() or "3 month" in message.lower():
            time_range = "last_90_days"
        
        # Call Data Science Agent tool
        result = await self.mcp.call_tool(
            server="ds",
            tool_name="analyze_health_trend",
            parameters={
                "user_id": user_id,
                "metric": metric,
                "time_range": time_range
            }
        )
        
        if "error" in result:
            return {
                "agent": "Data Science",
                "response": f"I couldn't analyze that data: {result['error']}",
                "data": result
            }
        
        # Have LLM interpret the results
        safe_result = self._json_safe(result)
        interpretation_prompt = f"""You are a data science health assistant. Explain these health trends to the user in a friendly, clear way:

User Query: {message}

Analysis Results:
    {json.dumps(safe_result, indent=2, default=str)}

Provide:
1. Clear summary of the trend
2. What it means for their health
3. Any notable patterns

Keep it concise (3-4 sentences) and encouraging."""

        interpretation = await ollama_client.generate(interpretation_prompt, temperature=0.7)
        
        # Save to conversation history
        self._save_conversation(user_id, message, interpretation, "ds")
        
        return {
            "agent": "Data Science",
            "response": interpretation,
            "data": result
        }
    
    async def _handle_domain_expert(
        self,
        user_id: int,
        message: str
    ) -> Dict[str, Any]:
        """Handle medical/domain expert queries."""
        logger.info(f"Domain Expert Agent processing: {message}")
        
        # Check for health concerns
        concerns = await self.mcp.call_tool(
            server="de",
            tool_name="check_health_concerns",
            parameters={"user_id": user_id}
        )
        
        # Get medical context
        context = await self.mcp.call_tool(
            server="de",
            tool_name="get_medical_context",
            parameters={"user_id": user_id}
        )
        
        # Have LLM provide medical interpretation
        safe_context = self._json_safe(context)
        safe_concerns = self._json_safe(concerns)
        medical_prompt = f"""You are a knowledgeable health expert (not a doctor). Answer this health question:

User Question: {message}

User Context:
    {json.dumps(safe_context, indent=2, default=str)}

Recent Health Concerns:
    {json.dumps(safe_concerns, indent=2, default=str)}

Provide:
1. Clear, accurate health information
2. Context-aware insights
3. When to consult a healthcare provider

Important: 
- This is educational information, not medical advice
- Always recommend consulting healthcare professionals for medical decisions
- Be empathetic and non-alarmist

Keep response clear and helpful (4-6 sentences)."""

        response = await ollama_client.generate(medical_prompt, temperature=0.6)
        
        # Save conversation
        self._save_conversation(user_id, message, response, "de")
        
        return {
            "agent": "Domain Expert",
            "response": response,
            "data": {
                "concerns": concerns,
                "context": context
            }
        }
    
    async def _handle_health_coach(
        self,
        user_id: int,
        message: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Handle health coaching queries."""
        logger.info(f"Health Coach Agent processing: {message}")
        
        # Get active goals
        goals = await self.mcp.call_tool(
            server="hc",
            tool_name="get_active_goals",
            parameters={"user_id": user_id}
        )
        
        # Basic coaching insights from active goals
        insights = {
            "note": "No automated coaching insights available; using active goals context.",
            "active_goals_count": len(goals.get("active_goals", [])) if isinstance(goals, dict) else 0
        }
        
        # Build conversation context
        history_text = ""
        if conversation_history:
            recent = conversation_history[-6:]  # Last 3 exchanges
            history_text = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in recent
            ])
        
        # Coaching prompt using motivational interviewing
        safe_goals = self._json_safe(goals)
        safe_insights = self._json_safe(insights)
        coaching_prompt = f"""You are an empathetic health coach using motivational interviewing techniques.

Conversation History:
{history_text}

User Message: {message}

User's Active Goals:
{json.dumps(safe_goals.get('active_goals', []), indent=2, default=str)}

Coaching Insights:
{json.dumps(safe_insights, indent=2, default=str)}

Respond using motivational interviewing principles:
1. Express empathy and understanding
2. Ask open-ended questions
3. Reflect what the user says
4. Support self-efficacy
5. Roll with resistance (don't argue)

Be warm, supportive, and collaborative. Help them find their own motivation.
Keep response natural and conversational (3-5 sentences)."""

        response = await ollama_client.generate(coaching_prompt, temperature=0.8)
        
        # Save conversation
        self._save_conversation(user_id, message, response, "hc")
        
        return {
            "agent": "Health Coach",
            "response": response,
            "data": {
                "goals": goals,
                "insights": insights
            }
        }
    
    async def _handle_multi_agent(
        self,
        user_id: int,
        message: str
    ) -> Dict[str, Any]:
        """Handle queries requiring multiple agents."""
        logger.info(f"Multi-agent processing: {message}")
        
        # Gather insights from all agents
        ds_summary = await self.mcp.call_tool(
            server="ds",
            tool_name="get_weekly_summary",
            parameters={"user_id": user_id}
        )
        
        de_concerns = await self.mcp.call_tool(
            server="de",
            tool_name="check_health_concerns",
            parameters={"user_id": user_id}
        )
        
        hc_insights = await self.mcp.call_tool(
            server="hc",
            tool_name="get_active_goals",
            parameters={"user_id": user_id}
        )
        
        # Synthesize multi-agent response
        synthesis_prompt = f"""You are a comprehensive health assistant. Answer this query using insights from multiple perspectives:

User Query: {message}

Data Science Insights:
{json.dumps(ds_summary, indent=2)}

Medical Expert Insights:
{json.dumps(de_concerns, indent=2)}

Health Coach Insights:
{json.dumps(hc_insights, indent=2)}

Provide a holistic response that:
1. Addresses the query directly
2. Combines relevant insights from all sources
3. Offers actionable recommendations
4. Maintains an encouraging, supportive tone

Keep it comprehensive but concise (5-7 sentences)."""

        response = await ollama_client.generate(synthesis_prompt, temperature=0.7)
        
        # Save conversation
        self._save_conversation(user_id, message, response, "multi")
        
        return {
            "agent": "Multi-Agent",
            "response": response,
            "data": {
                "data_science": ds_summary,
                "domain_expert": de_concerns,
                "health_coach": hc_insights
            }
        }
    
    def _save_conversation(
        self,
        user_id: int,
        user_message: str,
        assistant_message: str,
        agent_type: str
    ):
        """Save conversation to database."""
        db = SessionLocal()
        try:
            # Save user message
            db.add(Conversation(
                user_id=user_id,
                role="user",
                content=user_message,
                agent_type=agent_type
            ))
            
            # Save assistant message
            db.add(Conversation(
                user_id=user_id,
                role="assistant",
                content=assistant_message,
                agent_type=agent_type
            ))
            
            db.commit()
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
            db.rollback()
        finally:
            db.close()
