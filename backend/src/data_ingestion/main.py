from pathlib import Path

from config import DEFAULT_USERNAME
from paths import DB_PATH as RESOLVED_DB_PATH, USER_DATA_DIR
from services.letterboxd_store import LetterboxdStore
from utils.logger_utils import logger

DIARY_FILE = "diary.csv"
REVIEWS_FILE = "reviews.csv"


def main() -> None:
    logger.info(f"Database path: {Path(RESOLVED_DB_PATH).resolve()}")
    store = LetterboxdStore(RESOLVED_DB_PATH)
    store.ingest(
        USER_DATA_DIR / DIARY_FILE,
        USER_DATA_DIR / REVIEWS_FILE,
        DEFAULT_USERNAME,
    )


if __name__ == "__main__":
    main()
