"""Small local smoke test for a running app on localhost:8000.

Usage:
  1) Start app in another shell:
       python scripts/localhost.py --reload
  2) Run:
       python scripts/local_smoke_test.py
"""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

BASE_URL = "http://127.0.0.1:8000"


def get_json(path: str) -> dict:
    with urlopen(f"{BASE_URL}{path}", timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    health = get_json("/health")
    if health.get("status") != "ok":
        raise SystemExit(f"Health check failed: {health}")

    results = get_json("/api/search?q=prayer&limit=3")
    if "query" not in results or "results" not in results:
        raise SystemExit(f"Search response shape unexpected: {results}")

    print("Smoke test passed ✅")
    print(f"Health: {health}")
    print(f"Top result count: {len(results.get('results', []))}")


if __name__ == "__main__":
    try:
        main()
    except HTTPError as exc:
        raise SystemExit(f"HTTP error: {exc}") from exc
    except URLError as exc:
        raise SystemExit(
            "Cannot connect to local app. Start it first with: python scripts/localhost.py --reload"
        ) from exc
