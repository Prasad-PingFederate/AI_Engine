from __future__ import annotations

import sqlite3
from pathlib import Path

from core.models import Document


SCHEMA_SQL = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    source_type TEXT NOT NULL,
    author TEXT,
    book TEXT,
    chapter INTEGER,
    verse TEXT,
    tags TEXT,
    url TEXT,
    published_at TEXT
);

CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
    id,
    title,
    content,
    tags,
    content='documents',
    content_rowid='rowid'
);

CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
  INSERT INTO documents_fts(rowid, id, title, content, tags)
  VALUES (new.rowid, new.id, new.title, new.content, new.tags);
END;

CREATE TRIGGER IF NOT EXISTS documents_ad AFTER DELETE ON documents BEGIN
  INSERT INTO documents_fts(documents_fts, rowid, id, title, content, tags)
  VALUES('delete', old.rowid, old.id, old.title, old.content, old.tags);
END;

CREATE TRIGGER IF NOT EXISTS documents_au AFTER UPDATE ON documents BEGIN
  INSERT INTO documents_fts(documents_fts, rowid, id, title, content, tags)
  VALUES('delete', old.rowid, old.id, old.title, old.content, old.tags);
  INSERT INTO documents_fts(rowid, id, title, content, tags)
  VALUES (new.rowid, new.id, new.title, new.content, new.tags);
END;
"""


def init_db(db_path: Path) -> None:
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()


def upsert_documents(db_path: Path, docs: list[Document]) -> int:
    conn = sqlite3.connect(db_path)
    try:
        conn.executemany(
            """
            INSERT INTO documents (id, title, content, source_type, author, book, chapter, verse, tags, url, published_at)
            VALUES (:id, :title, :content, :source_type, :author, :book, :chapter, :verse, :tags, :url, :published_at)
            ON CONFLICT(id) DO UPDATE SET
                title=excluded.title,
                content=excluded.content,
                source_type=excluded.source_type,
                author=excluded.author,
                book=excluded.book,
                chapter=excluded.chapter,
                verse=excluded.verse,
                tags=excluded.tags,
                url=excluded.url,
                published_at=excluded.published_at
            """,
            [
                {
                    "id": d.id,
                    "title": d.title,
                    "content": d.content,
                    "source_type": d.source_type,
                    "author": d.author,
                    "book": d.book,
                    "chapter": d.chapter,
                    "verse": d.verse,
                    "tags": ",".join(d.tags),
                    "url": d.url,
                    "published_at": d.published_at.isoformat() if d.published_at else None,
                }
                for d in docs
            ],
        )
        conn.commit()
        return len(docs)
    finally:
        conn.close()
