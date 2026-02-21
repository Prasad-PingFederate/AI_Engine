from app.config import DB_PATH, DOCS_PATH
from core.data_loader import load_documents
from core.indexer import init_db, upsert_documents
from core.search import HybridSearcher


def test_search_returns_results_for_salvation() -> None:
    init_db(DB_PATH)
    docs = load_documents(DOCS_PATH)
    upsert_documents(DB_PATH, docs)

    searcher = HybridSearcher(DB_PATH)
    response = searcher.search("salvation", limit=5)

    assert response.total >= 1
    assert any("John 3:16" in hit.title for hit in response.hits)
