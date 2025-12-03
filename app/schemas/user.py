from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """User registration ke liye"""
    email: EmailStr
    password: str
    full_name: str
    company_id: int


class UserLogin(BaseModel):
    """User login ke liye"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response"""
    id: int
    email: str
    full_name: str
    company_id: int
    is_active: bool
    is_admin: bool
    created_at: datetime


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload"""
    user_id: Optional[int] = None