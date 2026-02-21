from __future__ import annotations

import re
from collections import Counter

SYNONYMS: dict[str, tuple[str, ...]] = {
    "love": ("charity", "beloved"),
    "salvation": ("saved", "redeem", "redemption"),
    "prayer": ("pray", "intercession", "supplication"),
    "faith": ("belief", "trust"),
    "jesus": ("christ", "messiah"),
}


WORD_RE = re.compile(r"[a-zA-Z0-9']+")


def tokenize(text: str) -> list[str]:
    return [m.group(0).lower() for m in WORD_RE.finditer(text)]


def expand_terms(terms: list[str]) -> list[str]:
    expanded: list[str] = []
    for term in terms:
        expanded.append(term)
        expanded.extend(SYNONYMS.get(term, ()))
    seen: set[str] = set()
    deduped: list[str] = []
    for t in expanded:
        if t not in seen:
            seen.add(t)
            deduped.append(t)
    return deduped


def cosine_overlap(query: str, text: str) -> float:
    q = Counter(tokenize(query))
    d = Counter(tokenize(text))
    if not q or not d:
        return 0.0
    common = set(q).intersection(d)
    dot = sum(q[t] * d[t] for t in common)
    q_norm = sum(v * v for v in q.values()) ** 0.5
    d_norm = sum(v * v for v in d.values()) ** 0.5
    if q_norm == 0 or d_norm == 0:
        return 0.0
    return dot / (q_norm * d_norm)


def build_fts_query(user_query: str) -> str:
    base_terms = tokenize(user_query)
    if not base_terms:
        return ""
    expanded = expand_terms(base_terms)
    return " OR ".join(f'"{term}"' for term in expanded)
