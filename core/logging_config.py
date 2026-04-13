from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from core.config import LOG_FORMAT, LOG_LEVEL

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)



def get_console_handler():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return handler


def get_file_handler(filename: str):
    file_path = LOG_DIR / filename

    handler = RotatingFileHandler(
        file_path,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return handler


def get_logger(name: str, filename: str):
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler(filename))

    logger.propagate = False

    return logger