import os
from openai import OpenAI

JUDGE_PROMPT = """Jesteś surowym sędzią oceniającym odpowiedzi asystenta AI.

Pytanie: {question}

Odpowiedź asystenta: {answer}

Czy ta odpowiedź poprawnie i kompletnie odpowiada na pytanie?
Odpowiedz tylko YES lub NO."""


def llm_judge(question: str, answer: str) -> bool:
    """Zwraca True jeśli LLM-judge uzna odpowiedź za poprawną."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    prompt = JUDGE_PROMPT.format(question=question, answer=answer)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=5,
    )

    verdict = response.choices[0].message.content.strip().upper()
    return verdict.startswith("YES")
