from pydantic import BaseModel, Field


class AddTitleRequest(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., min_length=1)
    wiki_id: str | None = None
    url: str | None = None


class SearchRequest(BaseModel):
    text: str = Field(..., min_length=1)
    limit: int = Field(5, ge=1, le=50)


class SearchResultItem(BaseModel):
    id: int | str
    score: float
    payload: dict


class SearchResponse(BaseModel):
    results: list[SearchResultItem]