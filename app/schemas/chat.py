from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatRequest(BaseModel):
    """Chat message request"""
    message: str
    conversation_id: Optional[int] = None
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat message response"""
    conversation_id: int
    message: str
    sources: Optional[List[dict]] = None
    created_at: datetime


class ConversationCreate(BaseModel):
    """New conversation create karne ke liye"""
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None


class ConversationResponse(BaseModel):
    """Conversation details"""
    id: int
    company_id: int
    status: str
    customer_name: Optional[str]
    customer_email: Optional[str]
    created_at: datetime
    updated_at: datetime


class MessageResponse(BaseModel):
    """Message details"""
    id: int
    conversation_id: int
    role: str
    content: str
    sources_used: Optional[str]
    created_at: datetime