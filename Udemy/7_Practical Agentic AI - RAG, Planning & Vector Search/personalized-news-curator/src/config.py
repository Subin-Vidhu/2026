"""Configuration management for the News Curator application."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Application settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MAX_ARTICLES_PER_TOPIC = int(os.getenv("MAX_ARTICLES_PER_TOPIC", 5))
RERANK_THRESHOLD = float(os.getenv("RERANK_THRESHOLD", 0.6))
USE_MOCKS = os.getenv("USE_MOCKS", "True").lower() == "true"
USE_LLM_RERANK = os.getenv("USE_LLM_RERANK", "False").lower() == "true"
USE_GROQ_RERANK = os.getenv("USE_GROQ_RERANK", "False").lower() == "true"

# Model configuration
LLM_MODEL = "gpt-4o"
TEMPERATURE = 0.7

# Application constants
INITIAL_TOPICS_COUNT = 3
PREFERENCE_UPDATE_FACTOR = 0.1  # Linear update: score += rating * PREFERENCE_UPDATE_FACTOR

def validate_config():
    """Validate that required configuration is set."""
    if not USE_MOCKS:
        if not TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY not set in .env file")
        if USE_LLM_RERANK and not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in .env file")
        if USE_GROQ_RERANK and not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not set in .env file")
    return True
