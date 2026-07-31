"""Configuration constants for RAG feature engineering.

Centralized configuration for paths, model names, and parameters used across
the RAG ingestion and retrieval pipeline.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Resolve project root and load .env before reading env-based settings.
PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# Environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# Paths
DATA_RAW_PATH = PROJECT_ROOT / "data" / "raw"
CHROMA_DB_PATH = PROJECT_ROOT / "chromadb"
CHROMA_COLLECTION_NAME = "company_docs"

# Embedding model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# LLM model
LLM_MODEL_NAME = "gpt-4o-mini"

# Ingestion parameters
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
DOCUMENT_GLOB_PATTERN = "**/*.md"

# Retrieval parameters
RETRIEVER_K = 3  # Number of documents to retrieve
MIN_SIMILARITY_SCORE = 1.48  # Minimum score threshold (lower is better in Chroma)

# Logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# RAG prompt system message
SYSTEM_PROMPT = """Jesteś wewnętrznym asystentem firmy AcmeTech.
Odpowiadaj WYŁĄCZNIE na podstawie dostarczonego kontekstu.
Jeśli w kontekście nie ma jasnej odpowiedzi na pytanie — odpowiedz dokładnie:
"Nie wiem".

Zakazane:
- korzystanie z własnej wiedzy
- zgadywanie
- domyślanie się
"""
