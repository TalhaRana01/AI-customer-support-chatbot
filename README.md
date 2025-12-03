# AI-Powered Customer Support Chatbot System

FastAPI, LangChain, aur SQLModel se bana ek complete customer support chatbot system with RAG (Retrieval Augmented Generation).

## 🎯 Features

- ✅ **Multi-tenant Support** - Har company ka alag data
- ✅ **RAG Pipeline** - Company documents se intelligent answers
- ✅ **Conversation History** - Complete chat tracking
- ✅ **Document Upload** - PDF, DOCX, TXT support
- ✅ **JWT Authentication** - Secure user management
- ✅ **Vector Database** - Semantic search with ChromaDB
- ✅ **RESTful API** - Well-documented endpoints

## 🛠️ Tech Stack

- **FastAPI** - High-performance web framework
- **SQLModel** - SQL databases with Python type hints
- **LangChain** - LLM application framework
- **ChromaDB** - Vector database for embeddings
- **PostgreSQL** - Relational database
- **OpenAI GPT** - Language model
- **Docker** - Containerization

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 15+
- OpenAI API Key
- Docker & Docker Compose (optional)

## 🚀 Installation

### Method 1: Local Setup

1. **Clone repository**
```bash
git clone <your-repo-url>
cd ai-customer-support
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env file with your credentials
```

5. **Setup PostgreSQL**
```bash
# Create database
createdb chatbot_db
```

6. **Run application**
```bash
uvicorn app.main:app --reload
```

### Method 2: Docker Setup

1. **Set environment variables**
```bash
export OPENAI_API_KEY="your-api-key"
```

2. **Run with Docker Compose**
```bash
docker-compose up --build
```

## 📚 API Documentation

Application run hone ke baad:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login

### Chat
- `POST /api/v1/chat/message` - Send chat message
- `GET /api/v1/chat/conversations` - Get all conversations
- `GET /api/v1/chat/conversation/{id}/messages` - Get conversation messages
- `POST /api/v1/chat/conversation/{id}/close` - Close conversation

### Documents
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents/list` - List all documents
- `DELETE /api/v1/documents/{id}` - Delete document

## 💡 Usage Example

### 1. Register User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123",
    "full_name": "John Doe",
    "company_id": 1
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

### 3. Upload Document
```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf"
```

### 4. Send Chat Message
```bash
curl -X POST "http://localhost:8000/api/v1/chat/message" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are your refund policies?",
    "customer_name": "Jane Smith"
  }'
```

## 🏗️ Project Structure

```
ai-customer-support/
├── app/
│   ├── api/          # API endpoints
│   ├── core/         # Core functionality (DB, security)
│   ├── models/       # SQLModel models
│   ├── schemas/      # Pydantic schemas
│   └── services/     # Business logic
├── uploads/          # File uploads
├── chroma_db/        # Vector database
└── tests/            # Test files
```

## 🔧 Configuration

`.env` file mein yeh settings configure karein:

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/chatbot_db
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

## 🧪 Testing

```bash
pytest tests/
```

## 📦 Deployment

### Production Recommendations

1. **Environment Variables** - Use proper secrets management
2. **Database** - Use managed PostgreSQL (AWS RDS, etc.)
3. **Vector Store** - Consider Pinecone for production scale
4. **File Storage** - Use S3 instead of local uploads
5. **Monitoring** - Add logging and monitoring tools

### Deploy to Railway/Render

1. Connect GitHub repository
2. Set environment variables
3. Deploy automatically

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## 📄 License

MIT License

## 🆘 Support

Issues ya questions ke liye GitHub Issues use karein.

## 📝 Todo / Future Enhancements

- [ ] WhatsApp/Telegram integration
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] Voice chat support
- [ ] Admin panel
- [ ] Sentiment analysis
- [ ] Auto-escalation to human agents

---

**Made with ❤️ using FastAPI, LangChain & SQLModel**
