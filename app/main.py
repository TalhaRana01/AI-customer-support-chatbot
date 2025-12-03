from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.core.database import create_db_and_tables
from app.api.v1.router import api_router

# FastAPI app initialize
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Powered Customer Support Chatbot System"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Application start hone par"""
    # Create database tables
    create_db_and_tables()
    print("✅ Database tables created")


@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "message": "AI Customer Support Chatbot API",
        "version": settings.VERSION,
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "vector_store": "initialized"
    }


# Include API v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)