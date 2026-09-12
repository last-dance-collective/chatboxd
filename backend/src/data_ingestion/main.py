from pathlib import Path

from data_ingestion.export_archive import username_from_profile
from paths import DB_PATH as RESOLVED_DB_PATH, USER_DATA_DIR
from services.letterboxd_store import LetterboxdStore
from utils.logger_utils import logger

DIARY_FILE = "diary.csv"
REVIEWS_FILE = "reviews.csv"
PROFILE_FILE = "profile.csv"


def main() -> None:
    logger.info(f"Database path: {Path(RESOLVED_DB_PATH).resolve()}")
    profile = USER_DATA_DIR / PROFILE_FILE
    if not profile.is_file():
        raise SystemExit(
            f"Missing {profile}. Copy profile.csv from the Letterboxd export into user_data/."
        )
    username = username_from_profile(profile.read_text(encoding="utf-8"))
    store = LetterboxdStore(RESOLVED_DB_PATH)
    store.ingest(
        USER_DATA_DIR / DIARY_FILE,
        USER_DATA_DIR / REVIEWS_FILE,
        username,
    )


if __name__ == "__main__":
    main()
