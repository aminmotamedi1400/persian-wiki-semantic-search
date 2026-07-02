from fastapi import FastAPI

from app.api import ApiController
from app.config import AppConfig
from app.embedding_service import EmbeddingService
from app.qdrant_service import QdrantService

config = AppConfig()

embedding_service = EmbeddingService(model_name=config.model_name)
qdrant_service = QdrantService(
    qdrant_url=config.qdrant_url,
    collection_name=config.collection_name,
)

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    try:
        qdrant_service.ensure_collection(vector_size=embedding_service.vector_size)
        print("✓ startup_ok")
    except Exception as exc:
        print(f"✗ startup_failed: {exc}")
        raise


api_controller = ApiController(
    embedding_service=embedding_service,
    qdrant_service=qdrant_service,
)
app.include_router(api_controller.router)