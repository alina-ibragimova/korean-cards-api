from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class CardCreate(BaseModel):
    word: str
    translation: str
    example: Optional[str] = None

class CardResponse(BaseModel):
    id: int
    word: str
    translation: str
    example: Optional[str] = None
    created_at: datetime
    repetitions: int
    ease_factor: float
    interval:int
    next_review: datetime

    model_config = ConfigDict(from_attributes=True) 

class CardUpdate(BaseModel):
    word: Optional[str] = None
    translation: Optional[str] = None
    example: Optional[str] = None

class ReviewCreate(BaseModel):
    quality: int = Field(ge=0, le=5, description="Оценка от 0 до 5")

class StatsResponse(BaseModel):
    total_cards: int
    due_today: int
    learned: int
    new_cards: int
    average_ease_factor: float
    model_config = ConfigDict(from_attributes=True) 

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) 