import io
import tempfile
import zipfile
from pathlib import Path

from fastapi.testclient import TestClient

from api import app as appmod
from services.letterboxd_store import LetterboxdStore

DIARY = (
    "Date,Name,Year,Letterboxd URI,Rating,Rewatch,Tags,Watched Date\n"
    "2024-01-15,Heat,1995,https://letterboxd.com/film/heat/,5,,,2024-01-15\n"
)
REVIEWS = "Date,Name,Review\n2024-01-15,Heat,Cops and robbers.\n"


def _zip_bytes() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("letterboxd-user/diary.csv", DIARY)
        archive.writestr("letterboxd-user/reviews.csv", REVIEWS)
        archive.writestr("letterboxd-user/profile.csv", "Date Joined,Username\n2024-11-20,Botij0\n")
        archive.writestr(
            "deleted/diary.csv",
            "Date,Name,Year,Letterboxd URI,Rating,Rewatch,Tags,Watched Date\n"
            "1999-01-01,Deleted,1999,https://x,1,,,1999-01-01\n",
        )
    return buffer.getvalue()


def test_ingest_zip_loads_live_csv() -> None:
    tmp = Path(tempfile.mkdtemp())
    appmod.DB_PATH = tmp / "letterboxd.db"
    appmod.USER_DATA_DIR = tmp / "user_data"
    client = TestClient(appmod.app, raise_server_exceptions=False)
    response = client.post(
        "/api/ingest",
        files={"export": ("letterboxd.zip", _zip_bytes(), "application/zip")},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["ok"] is True
    assert body["db_exists"] is True
    rows = LetterboxdStore(appmod.DB_PATH).filter_diary()
    assert [row["name"] for row in rows] == ["Heat"]
    assert rows[0]["username"] == "Botij0"


def test_ingest_rejects_plain_text() -> None:
    tmp = Path(tempfile.mkdtemp())
    appmod.DB_PATH = tmp / "letterboxd.db"
    appmod.USER_DATA_DIR = tmp / "user_data"
    client = TestClient(appmod.app, raise_server_exceptions=False)
    response = client.post(
        "/api/ingest",
        files={"export": ("notes.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 400
    assert "zip" in response.json()["detail"].lower()


if __name__ == "__main__":
    test_ingest_zip_loads_live_csv()
    test_ingest_rejects_plain_text()
    print("ok")
