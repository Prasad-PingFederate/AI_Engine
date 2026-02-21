from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import DB_PATH, DOCS_PATH
from core.data_loader import load_documents
from core.indexer import init_db, upsert_documents


def main() -> None:
    init_db(DB_PATH)
    docs = load_documents(DOCS_PATH)
    count = upsert_documents(DB_PATH, docs)
    print(f"Indexed {count} document(s) into {DB_PATH}")


if __name__ == "__main__":
    main()
