# Christian Search Engine (MVP)

This is a starter Christian search engine codebase with:

- Dataset format for Bible passages + great Christian persons quotes.
- Indexing pipeline into SQLite + FTS5.
- Hybrid search scorer (keyword + semantic token-overlap baseline).
- FastAPI endpoints for search.
- Simple web UI.

## Important note on "compete with Google"

A production engine that competes with Google requires distributed crawling, massive indexing, ranking learning systems, abuse/spam control, multilingual retrieval, and very large infrastructure.

This project is a **strong MVP foundation** you can evolve toward that direction.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/reindex.py
python scripts/localhost.py --reload
```

Open: `http://localhost:8000`

## API

- `GET /health`
- `GET /api/search?q=prayer&limit=10`

## Next scaling steps

1. Replace semantic overlap with transformer embeddings + vector DB.
2. Add synonym expansion and spell correction.
3. Add source authority scoring and freshness ranking.
4. Add user feedback loops and learning-to-rank.
5. Add crawler + ingestion workflows for trusted Christian sources.


### Quick local test

After installation, run:

```bash
python scripts/localhost.py --reload
```

Then open `http://localhost:8000` in your browser.


### Local-first workflow (before git push)

Use this flow so you can verify locally first, then commit/push:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/reindex.py
python scripts/localhost.py --reload
```

In another terminal (with the same venv active), run a quick smoke test:

```bash
python scripts/local_smoke_test.py
```

If smoke test passes, then you can commit/push your changes.

Optional custom host/port:

```bash
python scripts/localhost.py --host 127.0.0.1 --port 8000 --reload
```
