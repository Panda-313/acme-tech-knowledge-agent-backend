"""Feature engineering module for document processing and RAG."""

from .rag import (
    ask_question,
    create_rag_chain,
    ingest_documents,
    load_documents,
    load_vectorstore,
    split_documents,
)

__all__ = [
    "ingest_documents",
    "load_documents",
    "split_documents",
    "ask_question",
    "create_rag_chain",
    "load_vectorstore",
]
