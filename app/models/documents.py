from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Document(SQLModel, table=True):
    """Document model - uploaded company documents"""
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="company.id")
    
    filename: str
    file_type: str  # pdf, docx, txt
    file_path: str
    
    # Vector store metadata
    vector_ids: Optional[str] = None  # JSON array of vector IDs
    chunk_count: int = Field(default=0)
    
    is_active: bool = Field(default=True)
    uploaded_by: int = Field(foreign_key="user.id")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)