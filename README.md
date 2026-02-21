# Christian Search Engine (Improved MVP)

This repository now includes a stronger MVP for Christian-focused search:

- Structured corpus format for Bible passages and notable Christian thinkers.
- SQLite + FTS5 indexing with idempotent upserts.
- Hybrid ranking: keyword score + semantic overlap + source authority boost.
- Query expansion with Christian-term synonyms.
- Optional filters (`source_type`, `book`) from API and UI.
- FastAPI backend and simple web interface.

## Reality check about competing with Google

Google-scale relevance requires crawler infrastructure, massive distributed indexing, anti-spam systems, multilingual NLP, and learning-to-rank from huge behavioral datasets. This codebase is a practical **foundation**, not a Google replacement yet.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/reindex.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000`.

## API

- `GET /health`
- `GET /api/search?q=prayer&limit=10`
- `GET /api/search?q=salvation&source_type=bible&book=John`

## Retrieval details

1. User query is tokenized.
2. Query terms are expanded with curated Christian synonyms.
3. FTS query runs over title/content/tags.
4. Final score = weighted combination of keyword, semantic overlap, and source-type authority.
5. Results are sorted by final score.

## Suggested next steps

1. Replace semantic overlap with embeddings + vector retrieval.
2. Add phrase matching + typo correction.
3. Add doctrinal/topic taxonomy and faceted navigation.
4. Add ingestion pipelines for trusted Christian sources.
5. Add analytics + relevance feedback loop.

## Push to GitHub (`AI_Engine`)

If remote is not configured in your local clone:

```bash
git remote add origin https://github.com/Prasad-PingFederate/AI_Engine.git
git branch -M main
git push -u origin main
```

If using branch `work`:

```bash
git push -u origin work
```
