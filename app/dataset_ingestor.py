from datasets import load_dataset
from qdrant_client.models import PointStruct

from app.embedding_service import EmbeddingService
from app.qdrant_service import QdrantService


class DatasetIngestor:
    """Loads dataset and inserts title embeddings into Qdrant."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        qdrant_service: QdrantService,
        batch_size: int = 128,
        max_rows: int = 5000,
    ) -> None:
        self._embedding_service = embedding_service
        self._qdrant_service = qdrant_service
        self._batch_size = batch_size
        self._max_rows = max_rows

    def ingest_titles(self) -> int:
        dataset = load_dataset("MaralGPT/persian-wikipedia", split="train")
        buffer_rows: list[dict] = []
        inserted_count = 0

        for index, row in enumerate(dataset):
            title = (row.get("title") or "").strip()
            if not title:
                continue

            buffer_rows.append(
                {
                    "point_id": index + 1,
                    "title": title,
                    "wiki_id": row.get("id"),
                    "url": row.get("url"),
                }
            )

            if len(buffer_rows) >= self._batch_size:
                inserted_count += self._flush(buffer_rows)
                buffer_rows = []

            if inserted_count >= self._max_rows:
                break

        if buffer_rows and inserted_count < self._max_rows:
            inserted_count += self._flush(buffer_rows)

        return inserted_count

    def _flush(self, rows: list[dict]) -> int:
        titles = [item["title"] for item in rows]
        vectors = self._embedding_service.encode_many(titles)

        points: list[PointStruct] = []
        for item, vector in zip(rows, vectors):
            points.append(
                PointStruct(
                    id=item["point_id"],
                    vector=vector,
                    payload={
                        "title": item["title"],
                        "wiki_id": item["wiki_id"],
                        "url": item["url"],
                    },
                )
            )

        self._qdrant_service.upsert_many(points)
        return len(points)