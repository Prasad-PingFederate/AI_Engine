from core.query_utils import build_fts_query, cosine_overlap, expand_terms, tokenize


def test_tokenize_basic() -> None:
    assert tokenize("John 3:16 - God's love") == ["john", "3", "16", "god's", "love"]


def test_expand_terms_salvation() -> None:
    expanded = expand_terms(["salvation"])
    assert "salvation" in expanded
    assert "redemption" in expanded


def test_build_fts_query_nonempty() -> None:
    fts = build_fts_query("prayer")
    assert '"prayer"' in fts
    assert '"pray"' in fts


def test_cosine_overlap() -> None:
    assert cosine_overlap("faith hope", "faith and love") > 0
