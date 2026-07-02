from fastapi import APIRouter, HTTPException

from app.embedding_service import EmbeddingService
from app.models import AddTitleRequest, SearchRequest, SearchResponse, SearchResultItem
from app.qdrant_service import QdrantService


class ApiController:
    """Builds API router."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        qdrant_service: QdrantService,
    ) -> None:
        self._embedding_service = embedding_service
        self._qdrant_service = qdrant_service
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route("/", self.health_check, methods=["GET"])
        self.router.add_api_route("/add-title", self.add_title, methods=["POST"])
        self.router.add_api_route("/search", self.search, methods=["POST"], response_model=SearchResponse)

    def health_check(self) -> dict:
        return {"status": "ok"}

    def add_title(self, request: AddTitleRequest) -> dict:
        try:
            vector = self._embedding_service.encode_one(request.title)
            self._qdrant_service.upsert_one(
                point_id=request.id,
                vector=vector,
                payload={
                    "title": request.title,
                    "wiki_id": request.wiki_id,
                    "url": request.url,
                },
            )
            return {"status": "ok"}
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"insert_failed: {exc}")

    def search(self, request: SearchRequest) -> SearchResponse:
        try:
            query_vector = self._embedding_service.encode_one(request.text)
            points = self._qdrant_service.search(query_vector, request.limit)
            items = [
                SearchResultItem(id=point.id, score=point.score, payload=point.payload)
                for point in points
            ]
            return SearchResponse(results=items)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"search_failed: {exc}")