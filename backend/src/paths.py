from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = Path(__file__).resolve().parent
DB_PATH = ROOT_DIR / "letterboxd.db"
SECRETS_PATH = ROOT_DIR / "secrets.env"
USER_DATA_DIR = SRC_DIR / "data_ingestion" / "user_data"
