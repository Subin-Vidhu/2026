from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class HealthQueryRequest(BaseModel):
    """Request model for health queries."""
    user_id: int
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = []


class HealthQueryResponse(BaseModel):
    """Response model for health queries."""
    agent: str
    response: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class WearableDataCreate(BaseModel):
    """Create wearable data entry."""
    date: datetime
    heart_rate: Optional[int] = None
    steps: Optional[int] = None
    sleep_hours: Optional[float] = None
    hrv: Optional[int] = None
    calories: Optional[int] = None
    active_minutes: Optional[int] = None


class UploadDataRequest(BaseModel):
    """Upload health data request."""
    user_id: int
    data_type: str  # wearable, medical_record
    data: Dict[str, Any]


class UserStatsResponse(BaseModel):
    """User statistics response."""
    user_id: int
    total_data_points: int
    latest_heart_rate: Optional[int]
    avg_steps_30d: Optional[float]
    avg_sleep_30d: Optional[float]
    active_goals: int


class HealthGoalCreate(BaseModel):
    """Create health goal."""
    goal_type: str
    description: str
    target_value: Optional[float] = None
    timeline_days: int = 30
