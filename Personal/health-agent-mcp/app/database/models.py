from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=True)
    name = Column(String(100))
    age = Column(Integer)
    gender = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    wearable_data = relationship("WearableData", back_populates="user")
    medical_records = relationship("MedicalRecord", back_populates="user")
    goals = relationship("HealthGoal", back_populates="user")
    conversations = relationship("Conversation", back_populates="user")


class WearableData(Base):
    """Wearable device data."""
    __tablename__ = "wearable_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, index=True)
    heart_rate = Column(Integer)
    steps = Column(Integer)
    sleep_hours = Column(Float)
    hrv = Column(Integer)  # Heart Rate Variability
    calories = Column(Integer)
    active_minutes = Column(Integer, nullable=True)
    
    user = relationship("User", back_populates="wearable_data")


class MedicalRecord(Base):
    """Medical records and lab results."""
    __tablename__ = "medical_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    record_type = Column(String(50))  # blood_work, diagnosis, medication
    date = Column(DateTime, default=datetime.utcnow)
    data = Column(JSON)  # Flexible JSON storage for various record types
    notes = Column(Text, nullable=True)
    
    user = relationship("User", back_populates="medical_records")


class HealthGoal(Base):
    """User health goals."""
    __tablename__ = "health_goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    goal_type = Column(String(50))  # sleep, exercise, nutrition, weight
    description = Column(Text)
    target_value = Column(Float, nullable=True)
    current_value = Column(Float, nullable=True)
    timeline_days = Column(Integer, default=30)
    status = Column(String(20), default="active")  # active, completed, abandoned
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="goals")


class Conversation(Base):
    """Conversation history."""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String(20))  # user, assistant, system
    content = Column(Text)
    agent_type = Column(String(50), nullable=True)  # ds, de, hc, multi
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="conversations")
