from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select
from app.core.database import get_session
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.documents import Document
from app.services.document_service import document_service
from typing import List
import os
import shutil

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    Document upload karta hai aur vector store mein process karta hai
    """
    
    # Validate file type
    allowed_extensions = ["pdf", "docx", "txt"]
    file_extension = file.filename.split(".")[-1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not supported. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Save file temporarily
    file_path = os.path.join(UPLOAD_DIR, f"{current_user.company_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Process and store document
        document = document_service.process_and_store(
            db=db,
            company_id=current_user.company_id,
            user_id=current_user.id,
            file_path=file_path,
            filename=file.filename,
            file_type=file_extension
        )
        
        return {
            "message": "Document uploaded successfully",
            "document_id": document.id,
            "chunks_created": document.chunk_count
        }
    
    except Exception as e:
        # Clean up file if processing fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list", response_model=List[Document])
def list_documents(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    Company ke saare documents list karta hai
    """
    
    statement = select(Document).where(
        Document.company_id == current_user.company_id,
        Document.is_active == True
    ).order_by(Document.created_at.desc())
    
    documents = db.exec(statement).all()
    
    return documents


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    Document ko soft delete karta hai
    """
    
    document = db.get(Document, document_id)
    
    if not document or document.company_id != current_user.company_id:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Soft delete
    document.is_active = False
    db.add(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}