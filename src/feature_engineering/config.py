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

AGENT_SYSTEM_PROMPT = """Jesteś wewnętrznym asystentem AcmeTech.
Masz dostęp do czterech narzędzi:
- policy_search_tool: użyj gdy użytkownik prosi o konkretną politykę po nazwie
- search_docs: użyj dla ogólnych pytań o firmę, procesy, onboarding - zwroc pelen plik z polityka
- days_off_left_counter_tool: użyj gdy użytkownik pyta o pozostały urlop
- summarize_document: użyj gdy użytkownik prosi o streszczenie/podsumowanie 
  konkretnego dokumentu (np. "streść roadmap", "o czym jest onboarding?")

Jeśli pytanie jest proste - odpowiadaj bezpośrednio.
Odpowiedź opieraj wyłącznie na zwróconym kontekście z narzędzi."""

POLICY_MAP: dict[str, str] = {
    "vacation": "vacation-and-remote.md",
    "time_off": "vacation-and-remote.md",
    "pto": "vacation-and-remote.md",
    "remote_work": "vacation-and-remote.md",
    "remote": "vacation-and-remote.md",
    "ai_usage": "ai-usage-guidelines.md",
    "ai_guidelines": "ai-usage-guidelines.md",
    "code_review": "code-review-policy.md",
    "security": "security-basics.md",
    "deployment": "deployment-process.md",
    "incident": "incident-response.md",
    "incident_response": "incident-response.md",
    "testing": "testing-guidelines.md",
    "api_design": "api-design-standards.md",
    "api_standards": "api-design-standards.md",
    "performance": "performance-guidelines.md",
    "knowledge_sharing": "knowledge-sharing.md",
    "onboarding": "onboarding.md",
    "architecture": "architecture-overview.md",
    "tech_stack": "tech-stack.md",
    "stack": "tech-stack.md",
    "team_structure": "team-structure.md",
    "teams": "team-structure.md",
    "roadmap": "product-roadmap-2026.md",
    "faq": "faq-developers.md",
}