import tempfile
from pathlib import Path

from services.letterboxd_store import LetterboxdStore

DIARY_HEADER = (
    "Date,Name,Year,Letterboxd URI,Rating,Rewatch,Tags,Watched Date\n"
)
REVIEWS_HEADER = "Date,Name,Review\n"


def _write_export(directory: Path, diary_rows: str, review_rows: str) -> tuple[Path, Path]:
    diary = directory / "diary.csv"
    reviews = directory / "reviews.csv"
    diary.write_text(DIARY_HEADER + diary_rows, encoding="utf-8")
    reviews.write_text(REVIEWS_HEADER + review_rows, encoding="utf-8")
    return diary, reviews


def _store() -> tuple[LetterboxdStore, Path, Path, Path]:
    tmp = Path(tempfile.mkdtemp())
    db = tmp / "letterboxd.db"
    diary, reviews = _write_export(
        tmp,
        "2024-01-15,Heat,1995,https://letterboxd.com/film/heat/,5,Yes,,2024-01-15\n"
        "2023-06-01,Heat,1995,https://letterboxd.com/film/heat/,4.5,,,2023-06-01\n"
        "2024-03-02,Sicario,2015,https://letterboxd.com/film/sicario/,3.5,,,2024-03-02\n",
        "2024-01-15,Heat,Cops and robbers.\n",
    )
    store = LetterboxdStore(db)
    store.ingest(diary, reviews, "tester")
    return store, db, diary, reviews


def test_ingest_links_review_and_username() -> None:
    store, _, _, _ = _store()
    heat = store.filter_diary(name="Heat", year=1995, from_watched_date="2024-01-01")
    assert len(heat) == 1
    assert heat[0]["username"] == "tester"
    assert heat[0]["review_id"] is not None
    reviews = store.filter_reviews(review_id=heat[0]["review_id"])
    assert reviews[0]["review"] == "Cops and robbers."


def test_replace_does_not_duplicate() -> None:
    store, _, diary, reviews = _store()
    store.ingest(diary, reviews, "tester")
    rows = store.filter_diary()
    assert len(rows) == 3
    assert len(store.filter_reviews()) == 1


def test_named_diary_queries() -> None:
    store, _, _, _ = _store()
    assert [row["name"] for row in store.filter_diary(rewatch="Yes")] == ["Heat"]
    ranged = store.filter_diary(
        from_watched_date="2024-01-01", to_watched_date="2024-12-31"
    )
    assert {row["name"] for row in ranged} == {"Heat", "Sicario"}
    rated = store.filter_diary(from_rating=4.5, to_rating=5)
    assert all(row["rating"] >= 4.5 for row in rated)
    assert store.filter_diary(year=2015)[0]["name"] == "Sicario"


def test_filter_reviews_by_name() -> None:
    store, _, _, _ = _store()
    found = store.filter_reviews(name="Heat")
    assert len(found) == 1
    assert "Cops" in found[0]["review"]


def test_on_this_day() -> None:
    store, _, _, _ = _store()
    hits = store.on_this_day("-01-15")
    assert len(hits) == 1
    assert hits[0]["name"] == "Heat"
    lows = store.on_this_day("-03-02")
    assert lows == []


def test_missing_csv_column_raises() -> None:
    tmp = Path(tempfile.mkdtemp())
    db = tmp / "letterboxd.db"
    diary, reviews = _write_export(tmp, "2024-01-01,Heat,1995,https://x,5,,,2024-01-01\n", "")
    reviews.write_text("Date,Name\n2024-01-01,Heat\n", encoding="utf-8")
    store = LetterboxdStore(db)
    try:
        store.ingest(diary, reviews, "tester")
    except ValueError as exc:
        assert "Review" in str(exc)
        return
    raise AssertionError("expected ValueError")


if __name__ == "__main__":
    test_ingest_links_review_and_username()
    test_replace_does_not_duplicate()
    test_named_diary_queries()
    test_filter_reviews_by_name()
    test_on_this_day()
    test_missing_csv_column_raises()
    print("ok")
