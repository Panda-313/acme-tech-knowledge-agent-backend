"""Domain models for feature engineering."""

from typing import Literal

from pydantic import BaseModel

Year = Literal[2024, 2025, 2026, 2027]


class MockedUser(BaseModel):
    id: int
    name: str
    free_days_off_left: dict[Year, int]

class EvalQuestion(BaseModel):
    id: str
    category: str
    question: str
    expected_tools: list[str]
    expected_answer_contains: list[str]
    should_refuse: bool
    notes: str


class EvalResult(BaseModel):
    id: str
    question: str
    expected_tools: list[str]
    actual_tools: list[str]
    expected_answer_contains: list[str]
    final_answer: str
    should_refuse: bool
    did_refuse: bool
    latency_seconds: float
    sources: list[str]
    status: str
    passed: bool
    tools_match: bool
    refusal_match: bool
    answer_match: bool
    llm_judge_passed: bool | None = None
    error: str | None = None


