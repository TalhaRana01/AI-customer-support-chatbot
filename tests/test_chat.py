"""
RAG service tests
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.reg_service import RAGService
from app.core.vectorestore import VectorStoreManager


@pytest.fixture
def rag_service():
    """RAG service instance"""
    return RAGService()


@pytest.fixture
def mock_vectorstore():
    """Mock vector store"""
    with patch('app.core.vectorstore.vector_store') as mock:
        mock_retriever = Mock()
        mock_retriever.similarity_search_with_score.return_value = [
            (Mock(page_content="Test content 1", metadata={"source": "doc1.pdf"}), 0.9),
            (Mock(page_content="Test content 2", metadata={"source": "doc2.pdf"}), 0.8),
        ]
        mock.get_collection.return_value.as_retriever.return_value = mock_retriever
        yield mock


def test_rag_service_initialization(rag_service):
    """Test RAG service initializes correctly"""
    assert rag_service is not None
    assert rag_service.llm is not None
    assert rag_service.prompt_template is not None


@patch('app.services.rag_service.ConversationalRetrievalChain')
@patch('app.core.vectorstore.vector_store')
def test_get_answer_without_history(
    mock_vectorstore,
    mock_chain,
    rag_service
):
    """Test getting answer without chat history"""
    # Setup mocks
    mock_vectorstore.get_collection.return_value = Mock()
    mock_chain_instance = Mock()
    mock_chain_instance.return_value = {
        "answer": "This is the answer",
        "source_documents": [
            Mock(page_content="Doc content", metadata={"source": "test.pdf"})
        ]
    }
    mock_chain.from_llm.return_value = mock_chain_instance
    
    # Get answer
    result = rag_service.get_answer(
        company_id=1,
        question="What is your refund policy?"
    )
    
    assert "answer" in result
    assert "sources" in result


@patch('app.services.rag_service.ConversationalRetrievalChain')
@patch('app.core.vectorstore.vector_store')
def test_get_answer_with_history(
    mock_vectorstore,
    mock_chain,
    rag_service
):
    """Test getting answer with chat history"""
    # Setup mocks
    mock_vectorstore.get_collection.return_value = Mock()
    mock_chain_instance = Mock()
    mock_chain_instance.return_value = {
        "answer": "Based on our previous conversation, here's the answer",
        "source_documents": []
    }
    mock_chain.from_llm.return_value = mock_chain_instance
    
    # Chat history
    chat_history = [
        ("Hello", "Hi, how can I help?"),
        ("Tell me about refunds", "Our refund policy is 30 days")
    ]
    
    # Get answer
    result = rag_service.get_answer(
        company_id=1,
        question="How do I request a refund?",
        chat_history=chat_history
    )
    
    assert "answer" in result
    assert "sources" in result


def test_vector_store_manager_initialization():
    """Test vector store manager initialization"""
    manager = VectorStoreManager()
    assert manager.client is not None
    assert manager.embeddings is not None


@patch('chromadb.Client')
def test_get_collection(mock_chroma):
    """Test getting collection for a company"""
    manager = VectorStoreManager()
    collection = manager.get_collection(company_id=1)
    
    assert collection is not None


@patch('app.core.vectorstore.vector_store.get_collection')
def test_add_documents_to_vectorstore(mock_get_collection):
    """Test adding documents to vector store"""
    # Setup mock
    mock_vectorstore = Mock()
    mock_vectorstore.add_texts.return_value = ["id1", "id2", "id3"]
    mock_get_collection.return_value = mock_vectorstore
    
    manager = VectorStoreManager()
    
    texts = ["Text 1", "Text 2", "Text 3"]
    metadatas = [
        {"source": "doc1.pdf"},
        {"source": "doc2.pdf"},
        {"source": "doc3.pdf"}
    ]
    
    ids = manager.add_documents(
        company_id=1,
        texts=texts,
        metadatas=metadatas
    )
    
    assert len(ids) == 3


@patch('app.core.vectorstore.vector_store.get_collection')
def test_search_documents(mock_get_collection):
    """Test searching documents in vector store"""
    # Setup mock
    mock_vectorstore = Mock()
    mock_vectorstore.similarity_search_with_score.return_value = [
        (Mock(page_content="Relevant content", metadata={"source": "doc.pdf"}), 0.95)
    ]
    mock_get_collection.return_value = mock_vectorstore
    
    manager = VectorStoreManager()
    
    results = manager.search(
        company_id=1,
        query="refund policy",
        k=4
    )
    
    assert len(results) > 0
    assert results[0][1] == 0.95  # Score


def test_rag_prompt_template_format(rag_service):
    """Test RAG prompt template formatting"""
    template = rag_service.prompt_template
    
    assert "context" in template.lower()
    assert "question" in template.lower()
    assert "chat_history" in template.lower()
    assert "customer" in template.lower() or "assistant" in template.lower()