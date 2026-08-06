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

RATE_LIMIT_RETRIES = 4
RATE_LIMIT_BASE_BACKOFF_SECONDS = 15
INTER_QUESTION_DELAY_SECONDS = 0.5
LLM_TIMEOUT_SECONDS = 45

# Paths
DATA_RAW_PATH = PROJECT_ROOT / "data" / "raw"
CHROMA_DB_PATH = PROJECT_ROOT / "chromadb"
CHROMA_COLLECTION_NAME = "company_docs"
DATASET_PATH = Path(__file__).parent / "evals" / "eval_dataset.jsonl"
RESULTS_PATH = Path(__file__).parent / "evals" / "eval_results.jsonl"

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
MIN_SIMILARITY_SCORE = 2  # Minimum score threshold (lower is better in Chroma)

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
- policy_search_tool: użyj gdy użytkownik prosi o konkretną politykę po nazwie i chce pełny dokument
- search_docs: domyślne narzędzie dla pytań faktograficznych i ogólnych o firmę, procesy, onboarding itp.
- days_off_left_counter_tool: użyj tylko gdy użytkownik pyta o pozostały urlop konkretnej osoby
- summarize_document: użyj tylko gdy użytkownik WYRAŹNIE prosi o streszczenie/podsumowanie dokumentu

Twarde zasady wyboru narzędzia:
1. Jeśli pytanie jest faktograficzne (np. zaczyna się od: ile, jak długo, kiedy, gdzie, kto, czy) -> użyj search_docs.
2. summarize_document używaj wyłącznie przy jawnej intencji streszczenia (np. "streść", "podsumuj", "w skrócie", "TL;DR").
3. Samo wystąpienie słowa "onboarding", "roadmap" lub nazwy dokumentu NIE oznacza prośby o streszczenie.
4. Gdy masz wątpliwość między search_docs a summarize_document, wybierz search_docs.

Jeśli pytanie jest proste, odpowiadaj krótko i bezpośrednio.
Odpowiedź opieraj wyłącznie na kontekście zwróconym z narzędzi.

Jeśli pytanie nie dotyczy AcmeTech (np. pogoda, gotowanie, polityka, wiedza ogólna), odpowiedz dokładnie:
"Nie mogę pomóc w tym temacie – jestem asystentem wewnętrznym AcmeTech." i nie używaj żadnych narzędzi."""

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