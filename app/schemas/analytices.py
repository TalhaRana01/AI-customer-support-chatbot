from pydantic import BaseModel
from typing import Optional


class AnalyticsResponse(BaseModel):
    """Analytics dashboard data"""
    total_conversations: int
    active_conversations: int
    closed_conversations: int
    total_messages: int
    average_messages_per_conversation: float
    average_satisfaction_rating: Optional[float]
    total_documents: int


class ConversationStats(BaseModel):
    """Conversation statistics"""
    conversation_id: int
    message_count: int
    duration_minutes: Optional[float]
    satisfaction_rating: Optional[int]
    status: str