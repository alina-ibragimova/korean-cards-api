from sqlalchemy import Column, Integer, String, Text,ForeignKey, DateTime, Boolean, Float
from .database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, nullable=False)
    translation = Column(String, nullable=False)
    example = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    repetitions = Column(Integer, default=0, nullable=False)
    ease_factor = Column(Float, default= 2.5, nullable=False)
    interval = Column(Integer, default=0, nullable=False)
    next_review = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="cards")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    cards = relationship("Card", back_populates="owner")