from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.chat import (
    ChatRequest, 
    ChatResponse, 
    ConversationResponse,
    MessageResponse
)
from app.services.chat_service import chat_service
from typing import List

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/message", response_model=ChatResponse)
def send_message(
    request: ChatRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    Chat message send karta hai aur response return karta hai
    """
    
    # Get or create conversation
    conversation = chat_service.get_or_create_conversation(
        db=db,
        company_id=current_user.company_id,
        conversation_id=request.conversation_id,
        user_id=current_user.id,
        customer_name=request.customer_name,
        customer_email=request.customer_email
    )
    
    # Process message
    result = chat_service.process_message(
        db=db,
        company_id=current_user.company_id,
        conversation_id=conversation.id,
        user_message=request.message
    )
    
    return result


@router.get("/conversations", response_model=List[ConversationResponse])
def get_conversations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    User ke saare conversations return karta hai
    """
    
    statement = select(Conversation).where(
        Conversation.company_id == current_user.company_id
    ).order_by(Conversation.created_at.desc())
    
    conversations = db.exec(statement).all()
    
    return conversations


@router.get("/conversation/{conversation_id}/messages", response_model=List[MessageResponse])
def get_conversation_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    Specific conversation ke saare messages return karta hai
    """
    
    # Verify conversation belongs to user's company
    conversation = db.get(Conversation, conversation_id)
    if not conversation or conversation.company_id != current_user.company_id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at)
    
    messages = db.exec(statement).all()
    
    return messages


@router.post("/conversation/{conversation_id}/close")
def close_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    Conversation ko close karta hai
    """
    
    conversation = db.get(Conversation, conversation_id)
    if not conversation or conversation.company_id != current_user.company_id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conversation.status = "closed"
    db.add(conversation)
    db.commit()
    
    return {"message": "Conversation closed successfully"}