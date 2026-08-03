import logging
from typing import Any

from langchain_core.tools import tool

from src.feature_engineering.config import MIN_SIMILARITY_SCORE, RETRIEVER_K


def build_search_docs_tool(
        logger: logging.Logger,
        vectorstore: Any,
        used_sources: list[str],
        min_score: float = MIN_SIMILARITY_SCORE,
):
    @tool("search_docs", description="""Przeszukuje wewnętrzną bazę wiedzy AcmeTech.

Użyj tego narzędzia gdy użytkownik pyta o:
- polityki firmowe
- wewnętrzne procesy (onboarding, code review, remote work, itp.)
- wytyczne (AI usage, security, itp.)
- roadmapy produktowe lub inne dokumenty wewnętrzne

Input: jasne zapytanie związane z AcmeTech.""")
    def search_docs(query: str) -> str:
        logger.info("Agent requested document search for: %s", query)
        results = vectorstore.similarity_search_with_score(query, k=RETRIEVER_K)

        if not results:
            return "Brak wynikow w dokumentach firmowych."

        best_score = results[0][1]
        if best_score > min_score:
            return "Brak pewnych wynikow w dokumentach firmowych."

        formatted_results: list[str] = []
        for index, (doc, _) in enumerate(results, start=1):
            source = str(doc.metadata.get("source", "unknown"))
            if source not in used_sources:
                used_sources.append(source)
            formatted_results.append(
                f"[{index}] source: {source}\n{doc.page_content}"
            )

        return "\n\n".join(formatted_results)

    return search_docs

