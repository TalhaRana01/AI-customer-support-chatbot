from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DocumentUpload(BaseModel):
    """Document upload request"""
    pass  # File multipart/form-data se aayega


class DocumentResponse(BaseModel):
    """Document response"""
    id: int
    company_id: int
    filename: str
    file_type: str
    chunk_count: int
    is_active: bool
    uploaded_by: int
    created_at: datetime
    updated_at: datetime


class DocumentListResponse(BaseModel):
    """Document list response"""
    documents: list[DocumentResponse]
    total: int