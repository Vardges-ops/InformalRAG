from qdrant_client import QdrantClient
from core.config import QDRANT_URL

_client = None

def get_client():
    global _client
    if _client is None:
        _client = QdrantClient(url=QDRANT_URL)
    return _client