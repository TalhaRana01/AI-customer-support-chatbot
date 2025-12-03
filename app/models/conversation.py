from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Conversation(SQLModel, table=True):
    """Conversation model - har chat session"""
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="company.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Customer info (agar guest user hai)
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    
    status: str = Field(default="active")  # active, closed, archived
    satisfaction_rating: Optional[int] = None  # 1-5 rating
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    closed_at: Optional[datetime] = None