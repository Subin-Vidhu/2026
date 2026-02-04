from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Telegram
    telegram_bot_token: str = ""
    
    # Ollama
    ollama_base_url: str = "http://192.168.0.18:11444"
    ollama_model: str = "kimi-k2.5:cloud"
    ollama_fallback_model: str = "glm-4.7-flash:latest"
    
    # Database
    database_url: str = "sqlite:///./data/health_agent.db"
    
    # FastAPI
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # Logging
    log_level: str = "INFO"
    
    # MCP
    mcp_transport: str = "stdio"
    
    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:8000"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
