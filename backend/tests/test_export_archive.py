import io
import tempfile
import zipfile
from pathlib import Path

from data_ingestion.export_archive import ExportError, materialize_export

DIARY = "Date,Name,Year,Letterboxd URI,Rating,Rewatch,Tags,Watched Date\n"
REVIEWS = "Date,Name,Review\n"
LIVE_DIARY = DIARY + "2024-01-15,Heat,1995,https://letterboxd.com/film/heat/,5,,,2024-01-15\n"
LIVE_REVIEWS = REVIEWS + "2024-01-15,Heat,Cops and robbers.\n"
NESTED_DIARY = DIARY + "1999-01-01,Deleted,1999,https://x,1,,,1999-01-01\n"
PROFILE = "Date Joined,Username\n2024-11-20,Botij0\n"


def _zip_bytes(entries: dict[str, str]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for name, content in entries.items():
            archive.writestr(name, content)
    return buffer.getvalue()


def test_picks_live_files_over_nested_copies() -> None:
    dest = Path(tempfile.mkdtemp())
    source = _zip_bytes(
        {
            "letterboxd-user/diary.csv": LIVE_DIARY,
            "letterboxd-user/reviews.csv": LIVE_REVIEWS,
            "letterboxd-user/profile.csv": PROFILE,
            "letterboxd-user/watched.csv": "Date,Name,Year,Letterboxd URI\n",
            "deleted/diary.csv": NESTED_DIARY,
            "orphaned/diary.csv": NESTED_DIARY,
            "orphaned/reviews.csv": REVIEWS,
            "likes/reviews.csv": REVIEWS,
        }
    )
    export = materialize_export(source, dest)
    assert export.diary_csv.read_text(encoding="utf-8") == LIVE_DIARY
    assert export.reviews_csv.read_text(encoding="utf-8") == LIVE_REVIEWS
    assert export.username == "Botij0"
    assert sorted(path.name for path in dest.iterdir()) == ["diary.csv", "reviews.csv"]


def test_empty_diary_uses_watched_and_ratings() -> None:
    dest = Path(tempfile.mkdtemp())
    source = _zip_bytes(
        {
            "diary.csv": DIARY,
            "reviews.csv": REVIEWS,
            "profile.csv": PROFILE,
            "watched.csv": "Date,Name,Year,Letterboxd URI\n"
            "2024-11-20,Zoolander,2001,https://boxd.it/1YMA\n"
            "2024-11-21,Heat,1995,https://letterboxd.com/film/heat/\n",
            "ratings.csv": "Date,Name,Year,Letterboxd URI,Rating\n"
            "2024-11-20,Zoolander,2001,https://boxd.it/1YMA,5\n",
            "deleted/diary.csv": NESTED_DIARY,
        }
    )
    export = materialize_export(source, dest)
    from services.letterboxd_store import LetterboxdStore

    store = LetterboxdStore(dest / "letterboxd.db")
    store.ingest(export.diary_csv, export.reviews_csv, export.username)
    rows = {row["name"]: row for row in store.filter_diary()}
    assert set(rows) == {"Zoolander", "Heat"}
    assert rows["Zoolander"]["username"] == "Botij0"
    assert rows["Zoolander"]["rating"] == 5.0
    assert rows["Zoolander"]["watched_date"] == "2024-11-20"
    assert rows["Heat"]["rating"] is None


def test_nonempty_diary_ignores_watched() -> None:
    dest = Path(tempfile.mkdtemp())
    source = _zip_bytes(
        {
            "diary.csv": LIVE_DIARY,
            "reviews.csv": LIVE_REVIEWS,
            "profile.csv": PROFILE,
            "watched.csv": "Date,Name,Year,Letterboxd URI\n2024-11-20,Zoolander,2001,https://boxd.it/1YMA\n",
        }
    )
    export = materialize_export(source, dest)
    assert export.diary_csv.read_text(encoding="utf-8") == LIVE_DIARY
    assert export.username == "Botij0"


def test_missing_profile_raises() -> None:
    dest = Path(tempfile.mkdtemp())
    source = _zip_bytes({"diary.csv": LIVE_DIARY, "reviews.csv": LIVE_REVIEWS})
    try:
        materialize_export(source, dest)
    except ExportError as exc:
        assert "profile.csv" in str(exc)
        return
    raise AssertionError("expected ExportError")


def test_missing_diary_raises() -> None:
    dest = Path(tempfile.mkdtemp())
    source = _zip_bytes({"reviews.csv": LIVE_REVIEWS})
    try:
        materialize_export(source, dest)
    except ExportError as exc:
        assert "diary.csv" in str(exc)
        return
    raise AssertionError("expected ExportError")


def test_rejects_zip_slip() -> None:
    dest = Path(tempfile.mkdtemp())
    source = _zip_bytes({"../diary.csv": LIVE_DIARY, "reviews.csv": LIVE_REVIEWS})
    try:
        materialize_export(source, dest)
    except ExportError as exc:
        assert "unsafe" in str(exc)
        return
    raise AssertionError("expected ExportError")


def test_rejects_non_zip() -> None:
    dest = Path(tempfile.mkdtemp())
    try:
        materialize_export(b"not a zip", dest)
    except ExportError as exc:
        assert "zip" in str(exc).lower()
        return
    raise AssertionError("expected ExportError")


if __name__ == "__main__":
    test_picks_live_files_over_nested_copies()
    test_empty_diary_uses_watched_and_ratings()
    test_nonempty_diary_ignores_watched()
    test_missing_profile_raises()
    test_missing_diary_raises()
    test_rejects_zip_slip()
    test_rejects_non_zip()
    print("ok")
