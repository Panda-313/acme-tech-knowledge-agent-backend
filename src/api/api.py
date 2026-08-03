import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
import logging
from fastapi.middleware.cors import CORSMiddleware
from langgraph.checkpoint.memory import InMemorySaver

from src.api.types import Question, Answer
from src.feature_engineering import ask_question_agent, load_vectorstore
from src.feature_engineering.config import (
    CHROMA_COLLECTION_NAME,
    CHROMA_DB_PATH,
    LOG_FORMAT,
    LOG_LEVEL,
)
from src.feature_engineering.scripts.rag_demo import MOCKED_USERS

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    logging.basicConfig(
        format=LOG_FORMAT,
        level=LOG_LEVEL,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("rag_demo.log"),
        ],
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Initializing API resources")

    try:
        app.state.vectorstore = load_vectorstore(
            persist_directory=str(CHROMA_DB_PATH),
            collection_name=CHROMA_COLLECTION_NAME,
        )
        app.state.checkpointer = InMemorySaver()
        logger.info("Vector store and checkpointer loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load vectorstore during startup: {e}")
        raise RuntimeError("Failed to initialize vectorstore") from e
    try:
        yield
    finally:
        if hasattr(app.state, "vectorstore"):
            del app.state.vectorstore
        if hasattr(app.state, "checkpointer"):
            del app.state.checkpointer


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.post("/chat")
def ask_question_post(question: Question, thread_id: int) -> Answer:
    logger.info("POST request: /ask with body: %s", question.question)
    vectorstore = getattr(app.state, "vectorstore", None)
    if vectorstore is None:
        raise HTTPException(status_code=500, detail="Vectorstore not initialized")
    checkpointer = getattr(app.state, "checkpointer", None)
    if checkpointer is None:
        raise HTTPException(status_code=500, detail="Checkpointer not initialized")

    return ask_question_agent(
        question.question,
        vectorstore,
        current_user=MOCKED_USERS[0],
        checkpointer=checkpointer,
        thread_id=thread_id
    )
