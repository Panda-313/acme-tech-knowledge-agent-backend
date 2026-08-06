"""Tool for summarizing internal company documents."""

import logging

from pydantic import SecretStr

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from src.feature_engineering.config import POLICY_MAP, DATA_RAW_PATH, LLM_MODEL_NAME

SUMMARIZE_PROMPT = """Streść poniższy dokument w 3-5 kluczowych punktach.
Bądź zwięzły i skup się na najważniejszych informacjach.

Dokument:
{content}
"""


def build_summarize_document_tool(
        logger: logging.Logger,
        used_sources: list[str],
        api_key: str | SecretStr,
):
    @tool("summarize_document", description="""Streszcza wewnętrzny dokument AcmeTech.

Użyj tego narzędzia gdy użytkownik prosi o:
- streszczenie konkretnego dokumentu ("streść mi roadmap", "podsumuj onboarding")
- krótki przegląd treści dokumentu ("w skrócie co zawiera Y?")
- szybkie podsumowanie zamiast pełnej treści

NIE używaj tego narzędzia, gdy pytanie jest faktograficzne lub punktowe
(np. "ile", "jak długo", "kiedy", "gdzie", "kto", "czy"). Wtedy użyj search_docs.

Dostępne dokumenty: vacation, remote_work, ai_usage, code_review, security, deployment, incident_response, testing, api_design, performance, knowledge_sharing, onboarding, architecture, tech_stack, team_structure, roadmap, faq

Input: nazwa dokumentu (np. "roadmap", "onboarding", "ai_usage")
Output: zwięzłe streszczenie w 3-5 punktach.""")
    def summarize_document(document_name: str) -> str:
        document_name = document_name.lower().strip()

        if document_name not in POLICY_MAP:
            available_docs = ", ".join(POLICY_MAP.keys())

            return f"Couldn't find the document you were asking for. Here is a list of available documents: {available_docs}. "

        full_document_path = DATA_RAW_PATH / POLICY_MAP[document_name]

        logger.info(f"Summarizing {full_document_path}")

        if not full_document_path.exists():
            return f"Couldnt not find the document you were asking for. With path: {full_document_path}"

        content = full_document_path.read_text(encoding="utf-8")

        if full_document_path not in used_sources:
            used_sources.append(str(full_document_path))

        llm = ChatOpenAI(model=LLM_MODEL_NAME, api_key=api_key, temperature=0)
        prompt = SUMMARIZE_PROMPT.format(content=content)
        response = llm.invoke(prompt)

        logger.info(f"LLM summarized content and responded with: {response.content}")

        return response.content

    return summarize_document
