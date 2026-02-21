from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str
    title: str
    content: str
    source_type: str
    author: Optional[str] = None
    book: Optional[str] = None
    chapter: Optional[int] = None
    verse: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    url: Optional[str] = None
    published_at: Optional[datetime] = None


class SearchHit(BaseModel):
    id: str
    title: str
    snippet: str
    source_type: str
    author: Optional[str] = None
    score: float
    keyword_score: float
    semantic_score: float
    tags: list[str] = Field(default_factory=list)


class SearchResponse(BaseModel):
    query: str
    total: int
    took_ms: float
    hits: list[SearchHit]
