import sqlite3
from typing import List, Dict, Any, Tuple
from enum import Enum

class Operator(Enum):
    EQUAL = "="
    LESS_THAN_EQUAL = "<="
    GREATER_THAN_EQUAL = ">="
    BETWEEN = "BETWEEN"

OPERATOR_VALUES = [op.value for op in Operator]


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

    def _parse_filters(self, filters: List[Dict[str, Any]]) -> Tuple[str, List[Any]]:
        """
        Helper method to create the WHERE clause and values list from filter conditions.

        Args:
            filters (list): A list of dictionaries where each dictionary has "column", "operator", and "value".

        Returns:
            tuple: A WHERE clause string and a list of values for SQL query execution.
        """
        where_clause = []
        values = []
        
        for filter_item in filters:
            column = filter_item["column"]
            operator = filter_item["operator"]
            value = filter_item["value"]

            where_clause_part, value_list = self._build_where_clause_part(column, operator, value)
            where_clause.append(where_clause_part)
            values.extend(value_list)

        return " AND ".join(where_clause), values

    def _build_where_clause_part(self, column: str, operator: str, value: Any) -> Tuple[str, List[Any]]:
        """
        Helper method to build a part of the WHERE clause and corresponding values.

        Args:
            column (str): The column name.
            operator (str): The operator to use for filtering.
            value (Any): The value to filter by.

        Returns:
            tuple: A part of the WHERE clause and a list of values.
        """
        if operator.value not in OPERATOR_VALUES:
            raise ValueError(f"Unsupported operator: {operator}")

        if operator == Operator.BETWEEN.value:
            if not isinstance(value, list) or len(value) != 2:
                raise ValueError("BETWEEN operator requires a list of two values.")
            return f"{column} {operator} ? AND ?", value
        else:
            return f"{column} {operator.value} ?", [value]
        
    # -------- Methods for the Diary Table --------
    
    def filter_diary_entries(self, filters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter diary entries by any combination of fields with specified operators.
        
        Args:
            filters (list): A list of dictionaries, each containing "column", "operator", and "value".

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
            filters (list): A list of dictionaries, each containing "column", "operator", and "value".

        Returns:
            list: A list of dictionaries representing matching reviews.
        """
        where_clause, values = self._parse_filters(filters)
        query = f"SELECT * FROM reviews WHERE {where_clause}"

        cursor = self.connection.cursor()
        cursor.execute(query, tuple(values))

        return [dict(row) for row in cursor.fetchall()]
