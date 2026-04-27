from sentence_transformers import SentenceTransformer
from core.config import EMBEDDING_MODEL

_model = None


def get_model() -> SentenceTransformer:
    """Lazily loads and returns the SentenceTransformer model instance.
    Returns:
        SentenceTransformer: The loaded SentenceTransformer model instance.
    """
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model
