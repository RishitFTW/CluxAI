import sqlite3
from pathlib import Path

from CluxAI.config import config
from CluxAI.observability.logger import get_logger
from langgraph.checkpoint.sqlite import SqliteSaver

logger = get_logger(__name__)


def get_checkpointer() -> SqliteSaver:
    """Initialize and return a SQLite checkpointer for persistence."""
    db_path = config["memory"]["db_path"]
    Path(db_path).parent.mkdir(exist_ok=True)
    logger.info(f"Using SQLite checkpointer at {db_path}")

    conn = sqlite3.connect(db_path, check_same_thread=False)
    return SqliteSaver(conn)