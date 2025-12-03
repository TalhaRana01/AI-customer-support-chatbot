from sqlmodel import Session, select, func
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.documents import Document
from typing import Optional


class AnalyticsService:
    """Analytics and reporting service"""
    
    def get_dashboard_stats(self, db: Session, company_id: int) -> dict:
        """
        Company ke liye dashboard statistics return karta hai
        
        Args:
            db: Database session
            company_id: Company ID
        
        Returns:
            Dictionary with analytics data
        """
        
        # Total conversations
        total_conversations = db.exec(
            select(func.count(Conversation.id)).where(
                Conversation.company_id == company_id
            )
        ).one()
        
        # Active conversations
        active_conversations = db.exec(
            select(func.count(Conversation.id)).where(
                Conversation.company_id == company_id,
                Conversation.status == "active"
            )
        ).one()
        
        # Closed conversations
        closed_conversations = db.exec(
            select(func.count(Conversation.id)).where(
                Conversation.company_id == company_id,
                Conversation.status == "closed"
            )
        ).one()
        
        # Total messages
        total_messages = db.exec(
            select(func.count(Message.id)).where(
                Message.conversation_id.in_(
                    select(Conversation.id).where(
                        Conversation.company_id == company_id
                    )
                )
            )
        ).one()
        
        # Average messages per conversation
        avg_messages = total_messages / total_conversations if total_conversations > 0 else 0
        
        # Average satisfaction rating
        avg_rating = db.exec(
            select(func.avg(Conversation.satisfaction_rating)).where(
                Conversation.company_id == company_id,
                Conversation.satisfaction_rating.is_not(None)
            )
        ).one()
        
        # Total documents
        total_documents = db.exec(
            select(func.count(Document.id)).where(
                Document.company_id == company_id,
                Document.is_active == True
            )
        ).one()
        
        return {
            "total_conversations": total_conversations,
            "active_conversations": active_conversations,
            "closed_conversations": closed_conversations,
            "total_messages": total_messages,
            "average_messages_per_conversation": round(avg_messages, 2),
            "average_satisfaction_rating": round(float(avg_rating), 2) if avg_rating else None,
            "total_documents": total_documents
        }
    
    def get_conversation_stats(self, db: Session, conversation_id: int) -> dict:
        """
        Single conversation ki detailed statistics
        
        Args:
            db: Database session
            conversation_id: Conversation ID
        
        Returns:
            Dictionary with conversation stats
        """
        conversation = db.get(Conversation, conversation_id)
        if not conversation:
            return None
        
        # Message count
        message_count = db.exec(
            select(func.count(Message.id)).where(
                Message.conversation_id == conversation_id
            )
        ).one()
        
        # Duration calculation
        duration_minutes = None
        if conversation.closed_at:
            duration = conversation.closed_at - conversation.created_at
            duration_minutes = duration.total_seconds() / 60
        
        return {
            "conversation_id": conversation_id,
            "message_count": message_count,
            "duration_minutes": round(duration_minutes, 2) if duration_minutes else None,
            "satisfaction_rating": conversation.satisfaction_rating,
            "status": conversation.status
        }


# Global instance
analytics_service = AnalyticsService()