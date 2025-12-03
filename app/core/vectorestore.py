from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from app.config import settings
import chromadb
from chromadb.config import Settings as ChromaSettings


class VectorStoreManager:
    """Vector store ko manage karne ke liye"""
    
    def __init__(self):
        # ChromaDB client
        self.client = chromadb.Client(
            ChromaSettings(
                persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
                anonymized_telemetry=False
            )
        )
        
        # OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY
        )
    
    def get_collection(self, company_id: int):
        """Company-specific collection get karta hai"""
        collection_name = f"company_{company_id}"
        
        vectorstore = Chroma(
            client=self.client,
            collection_name=collection_name,
            embedding_function=self.embeddings
        )
        
        return vectorstore
    
    def add_documents(self, company_id: int, texts: list, metadatas: list):
        """Documents ko vector store mein add karta hai"""
        vectorstore = self.get_collection(company_id)
        ids = vectorstore.add_texts(texts=texts, metadatas=metadatas)
        return ids
    
    def search(self, company_id: int, query: str, k: int = 4):
        """Relevant documents search karta hai"""
        vectorstore = self.get_collection(company_id)
        results = vectorstore.similarity_search_with_score(query, k=k)
        return results


# Global instance
vector_store = VectorStoreManager()