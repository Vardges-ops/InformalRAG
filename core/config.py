import configparser
from pathlib import Path

config = configparser.ConfigParser()
config.read(Path(__file__).parent.parent / "config.cfg")

QDRANT_URL = config["QDRANT"]["url"]
COLLECTION_NAME = config["QDRANT"]["collection_name"]

EMBEDDING_MODEL = config["MODELS"]["embedding_model"]
RERANKER_PATH = config["MODELS"]["reranker_path"]

CACHE_SIZE = int(config["CACHE"]["cache_max_size"])
CACHE_EXPIRATION_SECONDS = int(config["CACHE"]["cache_expiration_seconds"])

LLM_URL = config["LLM"]["url"]
LLM_MODEL_NAME = config["LLM"]["model_name"]
