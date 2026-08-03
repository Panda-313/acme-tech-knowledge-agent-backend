from langchain_core.tools import tool

from src.feature_engineering.models import MockedUser


def build_calculate_leave_days_tool(logger, current_user: MockedUser):
    @tool(
        "days_off_left_counter_tool",
        description="""Oblicza pozostałe dni urlopowe dla bieżącego użytkownika w danym roku.

Użyj gdy użytkownik pyta o pozostałe dni wolne, bilans urlopowy lub ile dni urlopu mu zostało
(np. "ile mam jeszcze dni urlopowych w 2026?", "ile zostało mi urlopu?").

Input: rok, o który pyta użytkownik."""
    )
    def days_off_left_counter_tool(year: int):
        logger.info("Agent requested search for days left in: %s", year)


        if year < 2024 or year > 2027:
            return "Nie posiadam danych na te lata. MOje dane obejmuja 2024 - 2027"

        try:
            return f"Pozostalo Ci {current_user.free_days_off_left[year]} dni urlopowych"
        except Exception as e:
            return f"Nie wiem ile zostalo Ci dni urlopowych - zapewne nie posiadam danych na rok ktory podales"

    return days_off_left_counter_tool



