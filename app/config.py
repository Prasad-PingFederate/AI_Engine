from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Christian Search Engine")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "search.db"
DOCS_PATH = BASE_DIR / "data" / "documents.jsonl"
