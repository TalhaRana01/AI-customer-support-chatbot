from sqlmodel import Session, select
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.reg_service import rag_service
from typing import Optional, List, Tuple
import json


class ChatService:
    """Chat logic ko handle karta hai"""
    
    def get_or_create_conversation(
        self,
        db: Session,
        company_id: int,
        conversation_id: Optional[int] = None,
        user_id: Optional[int] = None,
        customer_name: Optional[str] = None,
        customer_email: Optional[str] = None
    ) -> Conversation:
        """
        Existing conversation get karta hai ya new create karta hai
        """
        
        if conversation_id:
            # Get existing conversation
            conversation = db.get(Conversation, conversation_id)
            if not conversation:
                raise ValueError("Conversation not found")
            return conversation
        
        # Create new conversation
        conversation = Conversation(
            company_id=company_id,
            user_id=user_id,
            customer_name=customer_name,
            customer_email=customer_email
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        return conversation
    
    def get_chat_history(
        self, 
        db: Session, 
        conversation_id: int
    ) -> List[Tuple[str, str]]:
        """
        Conversation ka history return karta hai
        Format: [(user_message, bot_message), ...]
        """
        
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at)
        
        messages = db.exec(statement).all()
        
        # Group messages into pairs
        history = []
        for i in range(0, len(messages) - 1, 2):
            if i + 1 < len(messages):
                user_msg = messages[i].content if messages[i].role == "user" else ""
                bot_msg = messages[i + 1].content if messages[i + 1].role == "assistant" else ""
                history.append((user_msg, bot_msg))
        
        return history
    
    def process_message(
        self,
        db: Session,
        company_id: int,
        conversation_id: int,
        user_message: str
    ) -> dict:
        """
        User message ko process karke response generate karta hai
        
        Returns:
            dict with 'message', 'sources', 'conversation_id'
        """
        
        # Get conversation
        conversation = db.get(Conversation, conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
        
        # Get chat history
        chat_history = self.get_chat_history(db, conversation_id)
        
        # Save user message
        user_msg = Message(
            conversation_id=conversation_id,
            role="user",
            content=user_message
        )
        db.add(user_msg)
        db.commit()
        
        # Get answer from RAG
        result = rag_service.get_answer(
            company_id=company_id,
            question=user_message,
            chat_history=chat_history
        )
        
        # Save assistant message
        assistant_msg = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=result["answer"],
            sources_used=json.dumps(result["sources"]) if result["sources"] else None
        )
        db.add(assistant_msg)
        db.commit()
        db.refresh(assistant_msg)
        
        return {
            "conversation_id": conversation_id,
            "message": result["answer"],
            "sources": result["sources"],
            "created_at": assistant_msg.created_at
        }


# Global instance
chat_service = ChatService()