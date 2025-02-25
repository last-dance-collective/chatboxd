import os
import sqlite3
import csv
from pathlib import Path
from utils.logger_utils import logger
from data_ingestion.sqlite_utils import run_query, run_insert

current_dir = os.getcwd()
os.path.join(current_dir, "src", "data_ingestion", "user_data")

USER_NAME = "mavilam"  # Change this to your username or the username you want to use
DB_PATH = os.path.join(current_dir, "letterboxd.db")

REVIEWS_FILE = "reviews.csv"
DIARY_FILE = "diary.csv"

REQUIRED_REVIEWS_COLUMNS = ["Date", "Name", "Review"]
REQUIRED_DIARY_COLUMNS = [
    "Date",
    "Name",
    "Year",
    "Letterboxd URI",
    "Rating",
    "Rewatch",
    "Tags",
    "Watched Date",
]


def create_reviews_table(db):
    run_insert(
        db,
        """
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            name TEXT NOT NULL,
            review BLOB NOT NULL
        )
    """,
    )


def create_diary_table(db):
    run_insert(
        db,
        """
        CREATE TABLE IF NOT EXISTS diary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            name TEXT NOT NULL,
            year INTEGER NOT NULL,
            letterboxd_uri TEXT NOT NULL,
            rating REAL,
            rewatch TEXT,
            tags TEXT,
            watched_date TEXT NOT NULL,
            username TEXT NOT NULL,
            review_id INTEGER,
            FOREIGN KEY(review_id) REFERENCES reviews(id)
        )
    """,
    )


def create_tables(db):
    create_reviews_table(db)
    create_diary_table(db)


def create_file_parser(file_name):
    file_path = Path(__file__).parent / f"user_data/{file_name}"
    return csv.DictReader(open(file_path, mode="r", encoding="utf-8"))


def insert_reviews_entries(db):
    parser = create_file_parser(REVIEWS_FILE)
    query = """
        INSERT INTO reviews (date, name, review)
        VALUES (?, ?, ?)
    """
    for row in parser:
        params = (row["Date"], row["Name"], row["Review"])
        run_insert(db, query, params)
    logger.info("Reviews entries read successfully.")


def insert_diary_entries(db):
    parser = create_file_parser(DIARY_FILE)
    query = """
        INSERT INTO diary (date, name, year, letterboxd_uri, rating, rewatch, tags, watched_date, username, review_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    for row in parser:
        diary_entry = run_query(
            db,
            "SELECT * FROM reviews WHERE name = ? AND date = ?",
            (row["Name"], row["Date"]),
        )
        entry_id = diary_entry[0]["id"] if diary_entry else None
        params = (
            row["Date"],
            row["Name"],
            int(row["Year"]),
            row["Letterboxd URI"],
            float(row["Rating"]) if row["Rating"] else None,
            row["Rewatch"],
            row["Tags"],
            row["Watched Date"],
            USER_NAME,
            entry_id,
        )
        run_insert(db, query, params)
    logger.info("Diary entries read successfully.")


def check_file_rows(file_name, required_columns):
    parser = create_file_parser(file_name)
    for row in parser:
        for column in required_columns:
            if column not in row:
                raise ValueError(f"Missing required column '{column}' in {file_name}")
    logger.info(f"{file_name} has the proper rows.")


def main():
    db_path = Path(DB_PATH).resolve()
    logger.info(f"Database path: {db_path}")
    db = sqlite3.connect(DB_PATH)
    try:
        check_file_rows(REVIEWS_FILE, REQUIRED_REVIEWS_COLUMNS)
        check_file_rows(
            DIARY_FILE,
            REQUIRED_DIARY_COLUMNS,
        )
        create_tables(db)
        insert_reviews_entries(db)
        insert_diary_entries(db)
    except ValueError as err:
        raise err
    except Exception as err:
        logger.error("Error in main:", err)
    finally:
        db.close()


if __name__ == "__main__":
    main()
