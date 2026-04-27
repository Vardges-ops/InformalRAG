from sentence_transformers import CrossEncoder
from core.config import RERANKER_PATH

_reranker = None


def get_reranker():
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(RERANKER_PATH)
    return _reranker
