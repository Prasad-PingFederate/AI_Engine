from __future__ import annotations

import math
import sqlite3
import time
from collections import Counter
from pathlib import Path

from core.models import SearchHit, SearchResponse


class HybridSearcher:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
        return [tok for tok in cleaned.split() if tok]

    def _semantic_overlap(self, query: str, text: str) -> float:
        q = Counter(self._tokenize(query))
        d = Counter(self._tokenize(text))
        if not q or not d:
            return 0.0

        common = set(q).intersection(d)
        dot = sum(q[t] * d[t] for t in common)
        q_norm = math.sqrt(sum(v * v for v in q.values()))
        d_norm = math.sqrt(sum(v * v for v in d.values()))
        if q_norm == 0 or d_norm == 0:
            return 0.0
        return dot / (q_norm * d_norm)

    def search(self, query: str, limit: int = 10) -> SearchResponse:
        start = time.perf_counter()
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            rows = conn.execute(
                """
                SELECT
                    d.id, d.title, d.content, d.source_type, d.author, d.tags,
                    bm25(documents_fts, 4.0, 1.5, 1.0, 0.8) AS keyword_score
                FROM documents_fts
                JOIN documents d ON d.rowid = documents_fts.rowid
                WHERE documents_fts MATCH ?
                ORDER BY keyword_score
                LIMIT ?
                """,
                (query, limit * 3),
            ).fetchall()
        except sqlite3.OperationalError:
            rows = conn.execute(
                """
                SELECT id, title, content, source_type, author, tags, 1.0 as keyword_score
                FROM documents
                WHERE title LIKE ? OR content LIKE ?
                LIMIT ?
                """,
                (f"%{query}%", f"%{query}%", limit * 3),
            ).fetchall()
        finally:
            conn.close()

        hits: list[SearchHit] = []
        for row in rows:
            keyword = 1 / (1 + max(float(row["keyword_score"]), 0.0))
            semantic = self._semantic_overlap(query, f"{row['title']} {row['content']}")
            score = (0.65 * keyword) + (0.35 * semantic)
            snippet = row["content"][:180] + ("..." if len(row["content"]) > 180 else "")
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
