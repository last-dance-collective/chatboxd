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

    # -------- Helper Method --------

    def _parse_filters(self, filters: List[Dict[str, Any]]) -> (str, List[Any]):
        """
        Helper method to create the WHERE clause and values list from filter conditions.

        Args:
            filters (list): A list of dictionaries where each dictionary has "key", "operator", and "value".

        Returns:
            tuple: A WHERE clause string and a list of values for SQL query execution.
        """
        where_clause = []
        values = []
        
        for filter_item in filters:
            key = filter_item["key"]
            operator = filter_item["operator"]
            value = filter_item["value"]

            # Validate operator
            if operator not in ["=", "<=", ">="]:
                raise ValueError(f"Unsupported operator: {operator}")

            where_clause.append(f"{key} {operator} ?")
            values.append(value)
        
        return " AND ".join(where_clause), values

    # -------- Methods for the Diary Table --------
    
    def filter_diary_entries(self, filters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter diary entries by any combination of fields with specified operators.
        
        Args:
            filters (list): A list of dictionaries, each containing "key", "operator", and "value".

        Returns:
            list: A list of dictionaries representing matching diary entries.
        """
        where_clause, values = self._parse_filters(filters)
        query = f"SELECT * FROM diary WHERE {where_clause}"

        cursor = self.connection.cursor()
        cursor.execute(query, values)
        
        return [dict(row) for row in cursor.fetchall()]

    # -------- Methods for the Reviews Table --------

    def filter_reviews(self, filters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter reviews by any combination of fields with specified operators.
        
        Args:
            filters (list): A list of dictionaries, each containing "key", "operator", and "value".

        Returns:
            list: A list of dictionaries representing matching reviews.
        """
        where_clause, values = self._parse_filters(filters)
        query = f"SELECT * FROM reviews WHERE {where_clause}"

        cursor = self.connection.cursor()
        cursor.execute(query, values)
        
        return [dict(row) for row in cursor.fetchall()]
