"""RAG retrieval pipeline for question answering.

Implements retrieval-augmented generation using LangChain and Chroma
vector store for context-aware question answering.
"""

import getpass
import logging
import os

from langchain_chroma import Chroma
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from ..config import (
    CHROMA_COLLECTION_NAME,
    CHROMA_DB_PATH,
    EMBEDDING_MODEL_NAME,
    LLM_MODEL_NAME,
    MIN_SIMILARITY_SCORE,
    RETRIEVER_K,
    SYSTEM_PROMPT,
)
from ...api.types import Answer

logger = logging.getLogger(__name__)


def _ensure_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        logger.warning("OPENAI_API_KEY not found in environment")
        api_key = getpass.getpass("Enter your OpenAI API key: ")
        if not api_key:
            logger.error("No API key provided")
            raise ValueError("OpenAI API key is required")
    return api_key


def load_vectorstore(
    persist_directory: str = str(CHROMA_DB_PATH),
    collection_name: str = CHROMA_COLLECTION_NAME,
    model_name: str = EMBEDDING_MODEL_NAME,
) -> Chroma:
    logger.info(f"Loading vectorstore from {persist_directory}")

    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name=collection_name,
    )

    logger.info(f"Vectorstore loaded with collection: {collection_name}")
    return vectorstore


def create_rag_chain(
    vectorstore: Chroma,
    model_name: str = LLM_MODEL_NAME,
    retriever_k: int = RETRIEVER_K,
    system_prompt: str = SYSTEM_PROMPT,
) -> tuple[ChatOpenAI, Chroma]:
    logger.info(f"Creating RAG chain with model: {model_name}")

    api_key = _ensure_api_key()

    llm = ChatOpenAI(model=model_name, api_key=api_key)

    retriever = vectorstore.as_retriever(search_kwargs={"k": retriever_k})

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "Kontekst: \n{context}\n\nPytanie:{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    logger.info("RAG chain created successfully")
    return rag_chain, vectorstore


def ask_question(
    question: str,
    vectorstore: Chroma,
    min_score: float = MIN_SIMILARITY_SCORE,
) -> Answer:
    logger.debug(f"Processing question: {question}")

    results = vectorstore.similarity_search_with_score(question, k=RETRIEVER_K)

    if not results:
        logger.warning(f"No results found for question: {question}")
        return Answer(answer="Nie wiem", sources=[])

    best_score = results[0][1]
    logger.info(f"Question: {question}, Best score: {best_score}")

    if best_score > min_score:
        logger.warning(
            f"Score {best_score} exceeds threshold {min_score} - "
            "cannot answer with confidence"
        )
        return Answer(answer="Nie wiem", sources=[])

    context_docs = [doc for doc, score in results]
    logger.info(f"doc: {context_docs}")
    sources = [doc.metadata.get('source') for doc in  context_docs]
  

    rag_chain, _ = create_rag_chain(vectorstore)

    response = rag_chain.invoke({
        "input": question,
        "context": context_docs,
    })

    # create_retrieval_chain returns dict with 'answer' key
    answer = response.get("answer", "")
    logger.debug(f"Generated answer: {answer[:100]}...")

    return Answer(answer=answer, sources=sources)
