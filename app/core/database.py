from sqlmodel import create_engine, SQLModel, Session
from app.config import settings

# Database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # SQL queries ko console mein print karega
    pool_pre_ping=True  # Connection health check
)


def create_db_and_tables():
    """Database tables create karne ke liye"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Database session provide karta hai"""
    with Session(engine) as session:
        yield session