from __future__ import annotations

import sqlite3
import time
from pathlib import Path

from core.models import SearchHit, SearchResponse
from core.query_utils import build_fts_query, cosine_overlap


SOURCE_TYPE_BOOST = {
    "bible": 1.0,
    "person": 0.92,
    "article": 0.85,
    "sermon": 0.84,
    "qa": 0.8,
}


class HybridSearcher:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def search(
        self,
        query: str,
        limit: int = 10,
        source_type: str | None = None,
        book: str | None = None,
    ) -> SearchResponse:
        start = time.perf_counter()
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        filters: list[str] = []
        params: list[object] = []
        if source_type:
            filters.append("d.source_type = ?")
            params.append(source_type)
        if book:
            filters.append("d.book = ?")
            params.append(book)

        where_suffix = f" AND {' AND '.join(filters)}" if filters else ""
        fts_query = build_fts_query(query)

        try:
            if fts_query:
                rows = conn.execute(
                    f"""
                    SELECT
                        d.id, d.title, d.content, d.source_type, d.author, d.tags,
                        bm25(documents_fts, 5.0, 1.8, 1.0, 0.8) AS keyword_score
                    FROM documents_fts
                    JOIN documents d ON d.rowid = documents_fts.rowid
                    WHERE documents_fts MATCH ? {where_suffix}
                    ORDER BY keyword_score
                    LIMIT ?
                    """,
                    [fts_query, *params, limit * 4],
                ).fetchall()
            else:
                rows = []
        except sqlite3.OperationalError:
            rows = conn.execute(
                f"""
                SELECT id, title, content, source_type, author, tags, 1.0 as keyword_score
                FROM documents d
                WHERE (title LIKE ? OR content LIKE ?) {where_suffix}
                LIMIT ?
                """,
                [f"%{query}%", f"%{query}%", *params, limit * 4],
            ).fetchall()
        finally:
            conn.close()

        hits: list[SearchHit] = []
        for row in rows:
            keyword_raw = float(row["keyword_score"])
            keyword = 1 / (1 + max(keyword_raw, 0.0))
            semantic = cosine_overlap(query, f"{row['title']} {row['content']}")
            authority = SOURCE_TYPE_BOOST.get(row["source_type"], 0.75)
            score = (0.55 * keyword) + (0.35 * semantic) + (0.10 * authority)
            snippet = row["content"][:220] + ("..." if len(row["content"]) > 220 else "")
            hits.append(
                SearchHit(
                    id=row["id"],
                    title=row["title"],
                    snippet=snippet,
                    source_type=row["source_type"],
                    author=row["author"],
                    score=round(score, 4),
                    keyword_score=round(keyword, 4),
                    semantic_score=round(semantic, 4),
                    tags=(row["tags"].split(",") if row["tags"] else []),
                )
            )

        hits.sort(key=lambda h: h.score, reverse=True)
        hits = hits[:limit]
        took_ms = (time.perf_counter() - start) * 1000
        return SearchResponse(query=query, total=len(hits), took_ms=round(took_ms, 2), hits=hits)
