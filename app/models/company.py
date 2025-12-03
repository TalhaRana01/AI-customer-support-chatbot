from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Company(SQLModel, table=True):
    """Company/Tenant model - har company ka alag data"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    domain: str = Field(unique=True)  # e.g., "acme-corp"
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)