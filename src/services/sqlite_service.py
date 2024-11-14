import sqlite3
from typing import List, Dict, Any


class Database:
    def __init__(self, db_path: str):
        """Initialize a connection to the SQLite database and set up a reusable connection."""
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = (
            sqlite3.Row
        )  # Enables dict-like row access by column name

    def __del__(self):
        """Close the database connection when the instance is destroyed."""
        self.connection.close()

    # -------- Methods for the Diary Table --------

    def filter_diary_entries(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filter diary entries by any combination of fields.

        Args:
            filters (dict): A dictionary of field-value pairs to filter by.

        Returns:
            list: A list of dictionaries representing matching diary entries.
        """
        where_clause = " AND ".join([f"{key} = ?" for key in filters.keys()])
        query = f"SELECT * FROM diary WHERE {where_clause}"

        cursor = self.connection.cursor()
        cursor.execute(query, tuple(filters.values()))

        return [dict(row) for row in cursor.fetchall()]

    # -------- Methods for the Reviews Table --------

    def filter_reviews(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filter reviews by any combination of fields.

        Args:
            filters (dict): A dictionary of field-value pairs to filter by.

        Returns:
            list: A list of dictionaries representing matching reviews.
        """
        where_clause = " AND ".join([f"{key} = ?" for key in filters.keys()])
        query = f"SELECT * FROM reviews WHERE {where_clause}"

        cursor = self.connection.cursor()
        cursor.execute(query, tuple(filters.values()))

        return [dict(row) for row in cursor.fetchall()]
