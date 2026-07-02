from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


class QdrantService:
    """Qdrant operations."""

    def __init__(self, qdrant_url: str, collection_name: str) -> None:
        self._client = QdrantClient(url=qdrant_url)
        self._collection_name = collection_name

    def ensure_collection(self, vector_size: int) -> None:
        exists = self._client.collection_exists(self._collection_name)
        if not exists:
            self._client.create_collection(
                collection_name=self._collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
            return

        info = self._client.get_collection(self._collection_name)
        current_size = info.config.params.vectors.size
        if current_size != vector_size:
            self._client.delete_collection(self._collection_name)
            self._client.create_collection(
                collection_name=self._collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )

    def upsert_one(self, point_id: int, vector: list[float], payload: dict) -> None:
        self._client.upsert(
            collection_name=self._collection_name,
            points=[PointStruct(id=point_id, vector=vector, payload=payload)],
        )

    def upsert_many(self, points: list[PointStruct]) -> None:
        if not points:
            return
        self._client.upsert(collection_name=self._collection_name, points=points)

    def search(self, query_vector: list[float], limit: int) -> list:
        result = self._client.query_points(
            collection_name=self._collection_name,
            query=query_vector,
            limit=limit,
        )
        return result.points