#!/usr/bin/env python3
"""
Main entry point for Personal Health Agent.
Starts all MCP servers, FastAPI backend, and Telegram bot.
"""

import uvicorn
import sys
import os
from app.config import get_settings

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Run the application."""
    settings = get_settings()
    
    print("🏥 Personal Health Agent")
    print("=" * 60)
    print(f"Starting application on {settings.api_host}:{settings.api_port}")
    print("\nServices:")
    print("  • FastAPI Backend")
    print("  • MCP Servers (Data Science, Domain Expert, Health Coach)")
    if settings.telegram_bot_token:
        print("  • Telegram Bot")
    print("\nAPI Documentation: http://localhost:8000/docs")
    print("=" * 60)
    print()
    
    # Run FastAPI with uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    main()
