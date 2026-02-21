from __future__ import annotations

import json
from pathlib import Path

from core.models import Document


def load_documents(path: Path) -> list[Document]:
    docs: list[Document] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            docs.append(Document.model_validate(json.loads(line)))
    return docs
