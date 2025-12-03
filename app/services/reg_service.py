from langchain_openai import ChatOpenAI
# from langchain_community.chains import ConversationalRetrievalChain
from langchain.chains import RetrievalQA

from langchain_core import ConversationBufferMemory
from langchain_core import PromptTemplate
from app.core.vectorestore import vector_store
from app.config import settings
from typing import List, Tuple


class RAGService:
    """RAG (Retrieval Augmented Generation) service"""
    
    def __init__(self):
        # OpenAI LLM
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo",
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Custom prompt template
        self.prompt_template = """You are a helpful customer support assistant. 
Use the following pieces of context to answer the customer's question. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}

Chat History: {chat_history}

Customer Question: {question}

Assistant Answer:"""
    
    def get_answer(
        self, 
        company_id: int, 
        question: str, 
        chat_history: List[Tuple[str, str]] = None
    ) -> dict:
        """
        Question ka answer return karta hai with sources
        
        Args:
            company_id: Company ID
            question: Customer ka question
            chat_history: Previous conversation [(user_msg, bot_msg), ...]
        
        Returns:
            dict with 'answer' and 'sources'
        """
        
        # Vector store se relevant documents
        vectorstore = vector_store.get_collection(company_id)
        
        # Memory for conversation
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Add chat history to memory
        if chat_history:
            for user_msg, bot_msg in chat_history:
                memory.save_context(
                    {"input": user_msg},
                    {"answer": bot_msg}
                )
        
        # Custom prompt
        qa_prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["context", "chat_history", "question"]
        )
        
        # Conversational Retrieval Chain
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
            memory=memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": qa_prompt}
        )
        
        # Get answer
        result = qa_chain({"question": question})
        
        # Extract sources
        sources = []
        for doc in result.get("source_documents", []):
            sources.append({
                "content": doc.page_content[:200],  # First 200 chars
                "metadata": doc.metadata
            })
        
        return {
            "answer": result["answer"],
            "sources": sources
        }


# Global instance
rag_service = RAGService()