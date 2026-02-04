import httpx
from typing import Dict, Any, List, Optional
import logging
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class OllamaClient:
    """Client for interacting with Ollama API."""
    
    def __init__(
        self,
        base_url: str = None,
        model: str = None,
        fallback_model: str = None,
        timeout: float = 120.0
    ):
        self.base_url = base_url or settings.ollama_base_url
        self.model = model or settings.ollama_model
        self.fallback_model = fallback_model or getattr(settings, 'ollama_fallback_model', settings.ollama_model)
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
        self._last_successful_model = self.model
    
    def _get_model(self) -> str:
        """Get the model to use (primary or fallback)."""
        return self._last_successful_model
    
    async def _try_request(
        self,
        endpoint: str,
        payload: Dict[str, Any],
        retry_with_fallback: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Try a request with fallback logic."""
        current_model = self._get_model()
        payload["model"] = current_model
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/{endpoint}",
                json=payload
            )
            response.raise_for_status()
            self._last_successful_model = current_model
            logger.info(f"Successfully used model: {current_model}")
            return response.json()
            
        except (httpx.TimeoutException, httpx.ReadTimeout) as e:
            logger.warning(f"Timeout error with {current_model}: {e}")
            if retry_with_fallback and current_model != self.fallback_model:
                logger.info(f"Switching to fallback model: {self.fallback_model}")
                self._last_successful_model = self.fallback_model
                payload["model"] = self.fallback_model
                response = await self.client.post(
                    f"{self.base_url}/api/{endpoint}",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
            raise
            
        except Exception as e:
            if "session" in str(e).lower() and retry_with_fallback and current_model != self.fallback_model:
                logger.warning(f"Session limit/error with {current_model}: {e}")
                logger.info(f"Switching to fallback model: {self.fallback_model}")
                self._last_successful_model = self.fallback_model
                payload["model"] = self.fallback_model
                response = await self.client.post(
                    f"{self.base_url}/api/{endpoint}",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
            raise
    
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate text completion from Ollama."""
        try:
            payload = {
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                }
            }
            
            if system:
                payload["system"] = system
            
            result = await self._try_request("generate", payload)
            return result.get("response", "")
            
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            return f"Error generating response: {str(e)}"
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Chat completion with conversation history."""
        try:
            payload = {
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                }
            }
            
            result = await self._try_request("chat", payload)
            return result.get("message", {}).get("content", "")
            
        except Exception as e:
            logger.error(f"Ollama chat error: {e}")
            return f"Error in chat completion: {str(e)}"
    
    async def classify_intent(self, user_message: str) -> str:
        """Classify user message intent."""
        prompt = f"""Classify this health query into ONE category:

Categories:
- data_analysis: Questions about trends, statistics, patterns in health data
- medical_question: Medical interpretation, symptoms, conditions, health concerns
- coaching: Goal-setting, motivation, behavior change, lifestyle advice
- multi_agent: Complex queries requiring multiple perspectives

Query: "{user_message}"

Respond with ONLY the category name (no explanation)."""

        result = await self.generate(prompt, temperature=0.1)
        intent = result.strip().lower()
        
        # Validate intent
        valid_intents = ["data_analysis", "medical_question", "coaching", "multi_agent"]
        for valid in valid_intents:
            if valid in intent:
                return valid
        
        return "multi_agent"  # Default fallback
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Global instance
ollama_client = OllamaClient(
    fallback_model=getattr(settings, 'ollama_fallback_model', settings.ollama_model)
)
