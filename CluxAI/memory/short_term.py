from pathlib import Path

from CluxAI.config import config
from CluxAI.llm.factory import get_llm
from CluxAI.observability.logger import get_logger
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langchain.agents.middleware import SummarizationMiddleware

logger = get_logger(__name__)


def get_checkpointer_db_path() -> str:
    """Ensure the parent directory exists and return the SQLite database path."""
    db_path = config["memory"]["db_path"]
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Using SQLite checkpointer at {db_path}")
    return db_path


def get_checkpointer() -> AsyncSqliteSaver:
    """Initialize and return an AsyncSqliteSaver checkpointer for persistence."""
    db_path = get_checkpointer_db_path()
    return AsyncSqliteSaver.from_conn_string(db_path)


def get_summarization_middleware() -> SummarizationMiddleware:
    """Initialize and return summarization middleware configured via token thresholds."""
    return SummarizationMiddleware(
        model=get_llm(),
        trigger=("tokens", config["memory"]["summarize_at_tokens"]),
        keep=("messages", config["memory"]["keep_last_messages"]),
    )