from sentence_transformers import CrossEncoder
from core.config import RERANKER_PATH

_reranker = None


def get_reranker() -> CrossEncoder:
    """Lazily loads and returns the CrossEncoder model instance.
    Returns:
        CrossEncoder: The loaded CrossEncoder model instance.
    """
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(RERANKER_PATH)
    return _reranker
