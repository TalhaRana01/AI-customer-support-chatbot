"""
Chat endpoints tests
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message


def test_send_message_creates_new_conversation(
    client: TestClient,
    auth_headers: dict,
    test_user: User
):
    """Test sending message creates new conversation"""
    response = client.post(
        "/api/v1/chat/message",
        headers=auth_headers,
        json={
            "message": "Hello, I need help",
            "customer_name": "John Doe",
            "customer_email": "john@example.com"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "conversation_id" in data
    assert "message" in data
    assert data["conversation_id"] > 0


def test_send_message_existing_conversation(
    client: TestClient,
    session: Session,
    auth_headers: dict,
    test_user: User
):
    """Test sending message to existing conversation"""
    # Create conversation
    conversation = Conversation(
        company_id=test_user.company_id,
        user_id=test_user.id,
        customer_name="Jane Doe",
        status="active"
    )
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    
    # Send message
    response = client.post(
        "/api/v1/chat/message",
        headers=auth_headers,
        json={
            "message": "Follow up question",
            "conversation_id": conversation.id
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"] == conversation.id


def test_get_conversations(
    client: TestClient,
    session: Session,
    auth_headers: dict,
    test_user: User
):
    """Test getting all conversations"""
    # Create multiple conversations
    for i in range(3):
        conv = Conversation(
            company_id=test_user.company_id,
            customer_name=f"Customer {i}",
            status="active"
        )
        session.add(conv)
    session.commit()
    
    # Get conversations
    response = client.get(
        "/api/v1/chat/conversations",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_get_conversation_messages(
    client: TestClient,
    session: Session,
    auth_headers: dict,
    test_user: User
):
    """Test getting messages from a conversation"""
    # Create conversation
    conversation = Conversation(
        company_id=test_user.company_id,
        customer_name="Test Customer",
        status="active"
    )
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    
    # Add messages
    messages_data = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi, how can I help?"},
        {"role": "user", "content": "I need info"}
    ]
    
    for msg_data in messages_data:
        msg = Message(
            conversation_id=conversation.id,
            role=msg_data["role"],
            content=msg_data["content"]
        )
        session.add(msg)
    session.commit()
    
    # Get messages
    response = client.get(
        f"/api/v1/chat/conversation/{conversation.id}/messages",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["content"] == "Hello"


def test_close_conversation(
    client: TestClient,
    session: Session,
    auth_headers: dict,
    test_user: User
):
    """Test closing a conversation"""
    # Create conversation
    conversation = Conversation(
        company_id=test_user.company_id,
        customer_name="Test Customer",
        status="active"
    )
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    
    # Close conversation
    response = client.post(
        f"/api/v1/chat/conversation/{conversation.id}/close",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    
    # Verify status changed
    session.refresh(conversation)
    assert conversation.status == "closed"


def test_send_message_without_auth(client: TestClient):
    """Test sending message without authentication"""
    response = client.post(
        "/api/v1/chat/message",
        json={"message": "Hello"}
    )
    
    assert response.status_code == 403  # Forbidden


def test_get_messages_wrong_company(
    client: TestClient,
    session: Session,
    auth_headers: dict,
    test_user: User
):
    """Test getting messages from another company's conversation"""
    # Create conversation for different company
    conversation = Conversation(
        company_id=999,  # Different company
        customer_name="Other Company Customer",
        status="active"
    )
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    
    # Try to access
    response = client.get(
        f"/api/v1/chat/conversation/{conversation.id}/messages",
        headers=auth_headers
    )
    
    assert response.status_code == 404








# import pytest
# from fastapi.testclient import TestClient
# from sqlmodel import Session, create_engine, SQLModel
# from app.main import app
# from app.core.database import get_session
# from app.models.company import Company


# # Test database
# DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# def get_test_session():
#     with Session(engine) as session:
#         yield session


# @pytest.fixture(name="client")
# def client_fixture():
#     """Test client with test database"""
#     SQLModel.metadata.create_all(engine)
    
#     # Override dependency
#     app.dependency_overrides[get_session] = get_test_session
    
#     client = TestClient(app)
#     yield client
    
#     # Cleanup
#     SQLModel.metadata.drop_all(engine)


# @pytest.fixture(name="test_company")
# def test_company_fixture(client):
#     """Create test company"""
#     with Session(engine) as session:
#         company = Company(name="Test Company", domain="test")
#         session.add(company)
#         session.commit()
#         session.refresh(company)
#         return company


# def test_register_user(client, test_company):
#     """Test user registration"""
#     response = client.post(
#         "/api/v1/auth/register",
#         json={
#             "email": "test@example.com",
#             "password": "testpass123",
#             "full_name": "Test User",
#             "company_id": test_company.id
#         }
#     )
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["email"] == "test@example.com"
#     assert "id" in data


# def test_login_user(client, test_company):
#     """Test user login"""
#     # First register
#     client.post(
#         "/api/v1/auth/register",
#         json={
#             "email": "test@example.com",
#             "password": "testpass123",
#             "full_name": "Test User",
#             "company_id": test_company.id
#         }
#     )
    
#     # Then login
#     response = client.post(
#         "/api/v1/auth/login",
#         json={
#             "email": "test@example.com",
#             "password": "testpass123"
#         }
#     )
    
#     assert response.status_code == 200
#     data = response.json()
#     assert "access_token" in data
#     assert data["token_type"] == "bearer"


# def test_login_invalid_credentials(client):
#     """Test login with invalid credentials"""
#     response = client.post(
#         "/api/v1/auth/login",
#         json={
#             "email": "wrong@example.com",
#             "password": "wrongpass"
#         }
#     )
    
#     assert response.status_code == 401