from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.api.deps import get_current_active_user
from app.models.user import User
from app.services.analytics_service import analytics_service
from app.schemas.analytices import AnalyticsResponse, ConversationStats

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=AnalyticsResponse)
def get_dashboard_analytics(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    Company ke liye dashboard analytics return karta hai
    """
    stats = analytics_service.get_dashboard_stats(
        db=db,
        company_id=current_user.company_id
    )
    
    return stats


@router.get("/conversation/{conversation_id}", response_model=ConversationStats)
def get_conversation_analytics(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    Specific conversation ki detailed statistics
    """
    stats = analytics_service.get_conversation_stats(
        db=db,
        conversation_id=conversation_id
    )
    
    if not stats:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return stats