from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Embedding provider wrapper."""

    def __init__(self, model_name: str) -> None:
        self._model = SentenceTransformer(model_name)

    @property
    def vector_size(self) -> int:
        return int(self._model.get_sentence_embedding_dimension())

    def encode_one(self, text: str) -> list[float]:
        vector = self._model.encode(text)
        return vector.tolist()

    def encode_many(self, texts: list[str]) -> list[list[float]]:
        vectors = self._model.encode(texts, show_progress_bar=False)
        return [v.tolist() for v in vectors]