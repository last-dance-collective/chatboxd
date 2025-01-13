import sqlite3
import csv
from pathlib import Path
from utils.sqlite_utils import run_query, run_insert

USER_NAME = "mavilam"  # Change this to your username or the username you want to use
DB_PATH = "../letterboxd.db"


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
    parser = create_file_parser("reviews.csv")
    query = """
        INSERT INTO reviews (date, name, review)
        VALUES (?, ?, ?)
    """
    for row in parser:
        params = (row["Date"], row["Name"], row["Review"])
        run_insert(db, query, params)
    print("Reviews entries read successfully.")


def insert_diary_entries(db):
    parser = create_file_parser("diary.csv")
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
    print("Diary entries read successfully.")


def main():
    db = sqlite3.connect(DB_PATH)
    try:
        create_tables(db)
        insert_reviews_entries(db)
        insert_diary_entries(db)
    except Exception as err:
        print("Error in main:", err)
    finally:
        db.close()


if __name__ == "__main__":
    main()
