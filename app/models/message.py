from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Message(SQLModel, table=True):
    """Message model - har individual message"""
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")
    
    role: str  # "user" ya "assistant"
    content: str
    
    # RAG metadata
    sources_used: Optional[str] = None  # JSON string of document sources
    
    created_at: datetime = Field(default_factory=datetime.utcnow)