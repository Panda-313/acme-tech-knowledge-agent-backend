"""RAG module for document ingestion and retrieval."""

from .ingestion import ingest_documents, load_documents, split_documents
from .agent import ask_question_agent
from .retrieval import ask_question, create_rag_chain, load_vectorstore

__all__ = [
    "ingest_documents",
    "load_documents",
    "split_documents",
    "ask_question",
    "ask_question_agent",
    "create_rag_chain",
    "load_vectorstore",
]
