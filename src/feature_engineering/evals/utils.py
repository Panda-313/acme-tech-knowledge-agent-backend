import json
from pathlib import Path
from typing import Any

from src.feature_engineering.models import EvalResult


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

    num_of_errors = sum(1 for result in results if result.error)
    num_of_results_with_no_errors = len(results) - num_of_errors
    tool_selection_accuracy = sum(1 for result in results if result.tools_match) / num_of_results_with_no_errors
    refusal_accuracy = sum(1 for result in results if result.refusal_match) / num_of_results_with_no_errors
    answer_match = sum(1 for result in results if (result.answer_match or result.llm_judge_passed)) / num_of_results_with_no_errors

    print(f"Tool selection accuracy: {tool_selection_accuracy:.2f}%")
    print(f"Refusal accuracy: {refusal_accuracy:.2f}%")
    print(f"Answer match: {answer_match:.2f}%")