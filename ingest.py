from app.config import AppConfig
from app.dataset_ingestor import DatasetIngestor
from app.embedding_service import EmbeddingService
from app.qdrant_service import QdrantService


def main() -> None:
    config = AppConfig()
    embedding_service = EmbeddingService(config.model_name)
    qdrant_service = QdrantService(config.qdrant_url, config.collection_name)
    qdrant_service.ensure_collection(embedding_service.vector_size)

    ingestor = DatasetIngestor(
        embedding_service=embedding_service,
        qdrant_service=qdrant_service,
        batch_size=config.batch_size,
        max_rows=config.max_rows,
    )
    count = ingestor.ingest_titles()
    print(f"✓ inserted: {count}")


if __name__ == "__main__":
    main()