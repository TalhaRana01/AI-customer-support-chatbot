from sqlmodel import Session, select
from app.models.user import User
from app.core.security import verify_password, get_password_hash, create_access_token
from typing import Optional


class AuthService:
    """Authentication service"""
    
    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """
        User ko authenticate karta hai
        
        Args:
            db: Database session
            email: User email
            password: Plain password
        
        Returns:
            User object if authenticated, None otherwise
        """
        statement = select(User).where(User.email == email)
        user = db.exec(statement).first()
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def create_user(
        self, 
        db: Session, 
        email: str, 
        password: str, 
        full_name: str,
        company_id: int
    ) -> User:
        """
        New user create karta hai
        
        Args:
            db: Database session
            email: User email
            password: Plain password
            full_name: User's full name
            company_id: Company ID
        
        Returns:
            Created User object
        """
        hashed_password = get_password_hash(password)
        
        user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            company_id=company_id
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    def generate_token(self, user_id: int) -> str:
        """
        User ke liye JWT token generate karta hai
        
        Args:
            user_id: User ID
        
        Returns:
            JWT access token
        """
        return create_access_token(data={"sub": user_id})


# Global instance
auth_service = AuthService()