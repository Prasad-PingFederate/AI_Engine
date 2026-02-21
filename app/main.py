from __future__ import annotations

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import APP_NAME, DB_PATH, DOCS_PATH
from core.data_loader import load_documents
from core.indexer import init_db, upsert_documents
from core.search import HybridSearcher

app = FastAPI(title=APP_NAME)
app.mount("/static", StaticFiles(directory="web"), name="static")
templates = Jinja2Templates(directory="web")


@app.on_event("startup")
def startup_event() -> None:
    init_db(DB_PATH)
    docs = load_documents(DOCS_PATH)
    upsert_documents(DB_PATH, docs)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/search")
def search_api(q: str = Query(..., min_length=2), limit: int = Query(10, ge=1, le=50)):
    searcher = HybridSearcher(DB_PATH)
    return searcher.search(q, limit)


@app.get("/", response_class=HTMLResponse)
def home(request: Request, q: str | None = None):
    result = None
    if q:
        searcher = HybridSearcher(DB_PATH)
        result = searcher.search(q, 10)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": APP_NAME,
            "query": q or "",
            "result": result,
        },
    )
