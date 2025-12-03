from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_core import RecursiveCharacterTextSplitter
from app.core.vectorestore import vector_store
from app.models.documents import Document
from sqlmodel import Session
import os
from typing import List
import json


class DocumentService:
    """Document processing service"""
    
    def __init__(self):
        # Text splitter - documents ko chunks mein split karne ke liye
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
    
    def load_document(self, file_path: str, file_type: str) -> List[str]:
        """
        File ko load karke text extract karta hai
        
        Args:
            file_path: File ka path
            file_type: pdf, docx, txt
        
        Returns:
            List of text chunks
        """
        
        # File type ke hisab se loader
        if file_type == "pdf":
            loader = PyPDFLoader(file_path)
        elif file_type == "docx":
            loader = Docx2txtLoader(file_path)
        elif file_type == "txt":
            loader = TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Load document
        documents = loader.load()
        
        # Split into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        return chunks
    
    def process_and_store(
        self, 
        db: Session,
        company_id: int, 
        user_id: int,
        file_path: str, 
        filename: str,
        file_type: str
    ) -> Document:
        """
        Document ko process karke vector store mein store karta hai
        
        Args:
            db: Database session
            company_id: Company ID
            user_id: User ID who uploaded
            file_path: File path
            filename: Original filename
            file_type: File type
        
        Returns:
            Document model instance
        """
        
        # Load and chunk document
        chunks = self.load_document(file_path, file_type)
        
        # Prepare texts and metadata
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [
            {
                "filename": filename,
                "chunk_index": i,
                "company_id": company_id
            }
            for i in range(len(chunks))
        ]
        
        # Store in vector database
        vector_ids = vector_store.add_documents(company_id, texts, metadatas)
        
        # Create document record in SQL database
        document = Document(
            company_id=company_id,
            filename=filename,
            file_type=file_type,
            file_path=file_path,
            vector_ids=json.dumps(vector_ids),
            chunk_count=len(chunks),
            uploaded_by=user_id
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        return document


# Global instance
document_service = DocumentService()