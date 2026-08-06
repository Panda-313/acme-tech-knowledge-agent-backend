import sys
import time
from typing import Any

import httpx
from openai import RateLimitError
from langgraph.checkpoint.memory import InMemorySaver

from src.api.types import Answer
from src.feature_engineering import ask_question_agent, load_vectorstore
from src.feature_engineering.config import CHROMA_COLLECTION_NAME, CHROMA_DB_PATH, DATASET_PATH, RESULTS_PATH, \
    RATE_LIMIT_RETRIES, LLM_TIMEOUT_SECONDS, RATE_LIMIT_BASE_BACKOFF_SECONDS, INTER_QUESTION_DELAY_SECONDS
from src.feature_engineering.evals import read_jsonl, write_jsonl, print_summary
from src.feature_engineering.evals.llm_judge import llm_judge
from src.feature_engineering.models import EvalQuestion, EvalResult
from src.refusal_detection import detect_refusal
from src.feature_engineering.scripts.rag_demo import MOCKED_USERS


def create_validation_questions_list(questions: list[dict[str, Any]]) -> list[EvalQuestion]:
    return [EvalQuestion(**question) for question in questions]

def has_expected_answer_content(final_answer: str, expected: list[str]) -> bool:
    lowered_answer = final_answer.lower()
    for fragment in expected:
        alternatives = [option.strip().lower() for option in fragment.split("||") if option.strip()]
        if not alternatives:
            continue
        if not any(option in lowered_answer for option in alternatives):
            return False
    return True


def run_single_question(
    question: EvalQuestion,
    vectorstore: Any,
    checkpointer: InMemorySaver,
    thread_id: int,
) -> EvalResult:
    started_at = time.perf_counter()
    for attempt in range(RATE_LIMIT_RETRIES + 1):
        try:
            response: Answer = ask_question_agent(
                question.question,
                vectorstore,
                current_user=MOCKED_USERS[0],
                checkpointer=checkpointer,
                thread_id=thread_id,
                llm_max_retries=0,
                llm_timeout_seconds=LLM_TIMEOUT_SECONDS,
            )
            break
        except (RateLimitError, httpx.HTTPStatusError) as exc:
            is_429 = isinstance(exc, RateLimitError) or (
                isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 429
            )
            if not is_429:
                raise
            if attempt >= RATE_LIMIT_RETRIES:
                latency = time.perf_counter() - started_at
                return EvalResult(
                    id=question.id,
                    question=question.question,
                    expected_tools=question.expected_tools,
                    actual_tools=[],
                    expected_answer_contains=question.expected_answer_contains,
                    final_answer="",
                    should_refuse=question.should_refuse,
                    did_refuse=False,
                    latency_seconds=latency,
                    sources=[],
                    status="error",
                    passed=False,
                    error=f"429 Rate limit after {RATE_LIMIT_RETRIES + 1} attempts: {exc}",
                )
            backoff_seconds = RATE_LIMIT_BASE_BACKOFF_SECONDS * (2**attempt)
            print(
                f"[{question.id}] 429 rate limit. Retry {attempt + 1}/{RATE_LIMIT_RETRIES} in {backoff_seconds:.1f}s..."
            )
            time.sleep(backoff_seconds)
        except Exception as exc:
            latency = time.perf_counter() - started_at
            return EvalResult(
                id=question.id,
                question=question.question,
                expected_tools=question.expected_tools,
                actual_tools=[],
                expected_answer_contains=question.expected_answer_contains,
                final_answer="",
                should_refuse=question.should_refuse,
                did_refuse=False,
                latency_seconds=latency,
                sources=[],
                status="error",
                passed=False,
                error=f"{type(exc).__name__}: {exc}",
            )
    else:
        latency = time.perf_counter() - started_at
        return EvalResult(
            id=question.id,
            question=question.question,
            expected_tools=question.expected_tools,
            actual_tools=[],
            expected_answer_contains=question.expected_answer_contains,
            final_answer="",
            should_refuse=question.should_refuse,
            did_refuse=False,
            latency_seconds=latency,
            sources=[],
            status="error",
            passed=False,
            error="Unknown eval error",
        )

    latency = time.perf_counter() - started_at
    actual_tools = response.used_tools
    final_answer = response.answer
    did_refuse = detect_refusal(final_answer, actual_tools)
    tools_match = all(expected_tool in actual_tools for expected_tool in question.expected_tools)
    answer_match = has_expected_answer_content(final_answer, question.expected_answer_contains)
    refusal_match = did_refuse == question.should_refuse

    judge_passed = llm_judge(question.question, final_answer)

    passed = tools_match and refusal_match and (answer_match or judge_passed)

    return EvalResult(
        id=question.id,
        question=question.question,
        expected_tools=question.expected_tools,
        actual_tools=actual_tools,
        expected_answer_contains=question.expected_answer_contains,
        final_answer=final_answer,
        should_refuse=question.should_refuse,
        did_refuse=did_refuse,
        latency_seconds=latency,
        sources=response.sources,
        status="success",
        passed=passed,
        llm_judge_passed=judge_passed,
    )


def run_eval_dataset(questions: list[EvalQuestion]) -> list[EvalResult]:
    vectorstore = load_vectorstore(
        persist_directory=str(CHROMA_DB_PATH),
        collection_name=CHROMA_COLLECTION_NAME,
    )
    checkpointer = InMemorySaver()
    results: list[EvalResult] = []

    for idx, question in enumerate(questions, start=1):
        thread_id = idx
        result = run_single_question(question, vectorstore, checkpointer, thread_id=thread_id)
        results.append(result)
        if idx < len(questions) and INTER_QUESTION_DELAY_SECONDS > 0:
            time.sleep(INTER_QUESTION_DELAY_SECONDS)

    return results


def main() -> int:
    questions = create_validation_questions_list(read_jsonl(DATASET_PATH))
    try:
        results = run_eval_dataset(questions)
        write_jsonl(RESULTS_PATH, results)
        print_summary(results)
        print(f"Saved results to: {RESULTS_PATH}")
        return 0
    except KeyboardInterrupt:
        print("\nEval interrupted by user.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
