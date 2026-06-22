from sentence_transformers import SentenceTransformer

_model = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-mpnet-base-v2")
    return _model


def generate_embedding(text: str) -> list[float]:
    """
    Generates a 768-dimensional embedding vector for the given text
    using a local Sentence Transformers model.
    """
    model = _get_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()