"""Utilities for detecting refusal-like answers in eval outputs."""

import re

_REFUSAL_PATTERNS = (
    re.compile(r"\bnie\s+wiem\b"),
    re.compile(r"\bnie\s+mog(?:ę|e)\b"),
    re.compile(r"\bpoza\s+zakresem\b"),
    re.compile(r"\bnie\s+jestem\s+w\s+stanie\b"),
    re.compile(r"\bnie\s+dotyczy\b"),
    re.compile(r"nie\s+mog(?:ę|e)\s+pomóc\s+w\s+tym\s+temacie"),
)


def detect_refusal(final_answer: str, actual_tools: list[str]) -> bool:
    lowered_answer = final_answer.lower()
    if any(pattern.search(lowered_answer) for pattern in _REFUSAL_PATTERNS):
        return True
    return not actual_tools and len(lowered_answer.strip()) == 0
