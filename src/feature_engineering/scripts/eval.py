import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import httpx
from openai import RateLimitError
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel

from src.api.types import Answer
from src.feature_engineering import ask_question_agent, load_vectorstore
from src.feature_engineering.config import CHROMA_COLLECTION_NAME, CHROMA_DB_PATH
from src.feature_engineering.evals.llm_judge import llm_judge
from src.refusal_detection import detect_refusal
from src.feature_engineering.scripts.rag_demo import MOCKED_USERS

DATASET_PATH = Path(__file__).resolve().parent.parent / "evals" / "eval_dataset.jsonl"
RESULTS_PATH = Path(__file__).resolve().parent.parent / "evals" / "eval_results.jsonl"
RATE_LIMIT_RETRIES = int(os.getenv("EVAL_RATE_LIMIT_RETRIES", "3"))
RATE_LIMIT_BASE_BACKOFF_SECONDS = float(os.getenv("EVAL_RATE_LIMIT_BASE_BACKOFF_SECONDS", "15"))
INTER_QUESTION_DELAY_SECONDS = float(os.getenv("EVAL_INTER_QUESTION_DELAY_SECONDS", "0.5"))
LLM_TIMEOUT_SECONDS = float(os.getenv("EVAL_LLM_TIMEOUT_SECONDS", "45"))


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
    llm_judge_passed: bool | None = None
    error: str | None = None


def validate_questions(questions: list[dict[str, Any]]) -> list[EvalQuestion]:
    return [EvalQuestion(**question) for question in questions]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    json_list: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as jsonl_file:
        for line in jsonl_file:
            if line.strip():
                json_list.append(json.loads(line))
    return json_list


def write_jsonl(path: Path, records: list[EvalResult]) -> None:
    with path.open("w", encoding="utf-8") as output:
        for record in records:
            output.write(record.model_dump_json(ensure_ascii=False) + "\n")


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
        except KeyboardInterrupt:
            raise
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

    print("*" * 60)
    print(f"{question.id}: {question.question}")
    print(f"latency = {latency}")
    print(f"actual_tools = {actual_tools}")
    print(f"final_answer = {final_answer}")
    print(f"did_refuse = {did_refuse}")
    print(f"tools_match = {tools_match}")
    print(f"answer_match = {answer_match}")
    print(f"refusal_match = {refusal_match}")
    print(f"passed = {passed}")
    print(f"llm_judge_passed = {judge_passed}")
    print("*" * 60)
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


def print_summary(results: list[EvalResult]) -> None:
    total = len(results)
    passed = sum(1 for result in results if result.passed)
    judge_passed = sum(1 for result in results if result.llm_judge_passed is True)
    errors = sum(1 for result in results if result.status == "error")
    successful_latencies = [result.latency_seconds for result in results if result.status == "success"]
    average_latency = sum(successful_latencies) / len(successful_latencies) if successful_latencies else 0.0

    print("\n=== Eval summary ===")
    print(f"Total: {total}")
    print(f"Passed (keyword): {passed}")
    print(f"Passed (llm_judge): {judge_passed}")
    print(f"Errors: {errors}")
    print(f"Average latency (success only): {average_latency:.2f}s")


def main() -> int:
    questions = validate_questions(read_jsonl(DATASET_PATH))
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
