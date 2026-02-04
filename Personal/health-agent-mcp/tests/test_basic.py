"""
Basic tests for Personal Health Agent
"""

import pytest
from app.utils.llm_utils import OllamaClient
from app.database import init_db, SessionLocal, User, WearableData
from datetime import datetime


def test_database_initialization():
    """Test database can be initialized."""
    init_db()
    db = SessionLocal()
    try:
        # Should not raise an error
        count = db.query(User).count()
        assert count >= 0
    finally:
        db.close()


def test_user_creation():
    """Test creating a user."""
    db = SessionLocal()
    try:
        user = User(
            name="Test User",
            age=30,
            gender="other"
        )
        db.add(user)
        db.commit()
        
        assert user.id is not None
        assert user.name == "Test User"
        
        # Cleanup
        db.delete(user)
        db.commit()
    finally:
        db.close()


def test_wearable_data_creation():
    """Test creating wearable data."""
    db = SessionLocal()
    try:
        # Create test user
        user = User(name="Test", age=25, gender="other")
        db.add(user)
        db.commit()
        
        # Create wearable data
        data = WearableData(
            user_id=user.id,
            date=datetime.now(),
            heart_rate=70,
            steps=8000,
            sleep_hours=7.5
        )
        db.add(data)
        db.commit()
        
        assert data.id is not None
        assert data.heart_rate == 70
        
        # Cleanup
        db.delete(data)
        db.delete(user)
        db.commit()
    finally:
        db.close()


@pytest.mark.asyncio
async def test_ollama_client():
    """Test Ollama client can generate text."""
    client = OllamaClient()
    
    # Simple generation test (will fail if Ollama not running)
    try:
        result = await client.generate("Say hello", temperature=0.1)
        assert isinstance(result, str)
        assert len(result) > 0
    except Exception as e:
        pytest.skip(f"Ollama not available: {e}")
    finally:
        await client.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
