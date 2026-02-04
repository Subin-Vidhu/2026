from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    """Create user model."""
    telegram_id: Optional[int] = None
    name: str
    age: int
    gender: str


class UserResponse(BaseModel):
    """User response model."""
    id: int
    name: str
    age: int
    gender: str
    telegram_id: Optional[int] = None
    
    class Config:
        from_attributes = True
