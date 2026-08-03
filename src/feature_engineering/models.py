"""Domain models for feature engineering."""

from typing import Literal

from pydantic import BaseModel

Year = Literal[2024, 2025, 2026, 2027]


class MockedUser(BaseModel):
    id: int
    name: str
    free_days_off_left: dict[Year, int]
