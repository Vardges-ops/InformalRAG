from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from core.config import LOG_FORMAT, LOG_LEVEL

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def get_console_handler() -> logging.StreamHandler:
    """Creates and returns a console handler for logging.
    Returns:
        logging.StreamHandler: A configured console handler for logging.
    """
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return handler


def get_file_handler(filename: str) -> RotatingFileHandler:
    """Creates and returns a file handler for logging with rotation.
    Args:
        filename (str): The name of the log file to write to.
    Returns:
        logging.handlers.RotatingFileHandler: A configured file handler for logging with rotation.
    """
    file_path = LOG_DIR / filename

    handler = RotatingFileHandler(
        file_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return handler


def get_logger(name: str, filename: str) -> logging.Logger:
    """Creates and returns a logger with the specified name and file handler.
    Args:
        name (str): The name of the logger to create.
        filename (str): The name of the log file to write to.
    Returns:
        logging.Logger: A configured logger with the specified name and file handler.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler(filename))

    logger.propagate = False

    return logger
