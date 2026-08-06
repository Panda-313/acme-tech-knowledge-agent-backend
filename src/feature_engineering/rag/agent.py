"""Basic LangChain agent for deciding when to search company documents."""

import getpass
import logging
import os
from typing import Any

from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

from .tools import build_search_docs_tool, build_policy_search_tool, build_calculate_leave_days_tool, build_summarize_document_tool
from ..config import AGENT_SYSTEM_PROMPT, LLM_MODEL_NAME, MIN_SIMILARITY_SCORE, RETRIEVER_K
from ..models import MockedUser
from ...api.types import Answer


def _ensure_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        api_key = getpass.getpass("Enter your OpenAI API key: ")
        if not api_key:
            raise ValueError("OpenAI API key is required")
    return api_key



def ask_question_agent(
    question: str,
    vectorstore: Any,
    current_user: MockedUser,
    checkpointer: InMemorySaver | None = None,
    logger: logging.Logger | None = None,
    min_score: float = MIN_SIMILARITY_SCORE,
    thread_id: int = 1,
    llm_max_retries: int = 2,
    llm_timeout_seconds: float = 60.0,
) -> Answer:
    logger = logger or logging.getLogger(__name__)
    used_sources: list[str] = []
    api_key = _ensure_api_key()
    
    search_docs = build_search_docs_tool(logger, vectorstore, used_sources, min_score=min_score)
    policy_search_tool = build_policy_search_tool(logger, used_sources)
    days_off_left_counter_tool = build_calculate_leave_days_tool(logger, current_user)
    summarize_document_tool = build_summarize_document_tool(logger, used_sources, api_key)

    llm = ChatOpenAI(
        model=LLM_MODEL_NAME,
        api_key=api_key,
        temperature=0,
        max_retries=llm_max_retries,
        timeout=llm_timeout_seconds,
    )
    thread_config = {"configurable": {"thread_id": thread_id}}

    agent = create_agent(
        model=llm,
        tools=[search_docs, policy_search_tool, days_off_left_counter_tool, summarize_document_tool],
        system_prompt=AGENT_SYSTEM_PROMPT,
        response_format=Answer,
        checkpointer=checkpointer,
    )


    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config=thread_config,
    )

    used_tools = []

    for message in result["messages"]:
        if isinstance(message, AIMessage):
            used_tools.extend(
                tool_call['name'].removeprefix('functions.')
                for tool_call in message.tool_calls
            )

    return add_source(used_sources, used_tools, result)


def add_source(used_sources: list[str], used_tools: list[str], result) -> Answer:
    structured_response = result.get("structured_response")

    if isinstance(structured_response, Answer):
        updates = {}
        if not structured_response.sources and used_sources:
            updates["sources"] = used_sources
        updates["used_tools"] = used_tools
        return structured_response.model_copy(update=updates)

    if isinstance(structured_response, dict):
        structured_response["sources"] = structured_response.get("sources") or used_sources
        structured_response["used_tools"] = used_tools
        return Answer.model_validate(structured_response)

    messages = result.get("messages", [])
    answer_text = str(messages[-1].content).strip() if messages else "Nie wiem"
    if not answer_text:
        answer_text = "Nie wiem"
    return Answer(answer=answer_text, sources=used_sources, used_tools=used_tools)
