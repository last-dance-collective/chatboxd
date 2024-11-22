from typing import List, Dict, Any, Tuple
from sqlalchemy import create_engine, Column, Integer, Text, Float, ForeignKey, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import operators
from enum import Enum

from utils.logger_utils import logger

Base = declarative_base()

class Operator(Enum):
    EQUAL = operators.eq
    LESS_THAN_EQUAL = operators.le
    GREATER_THAN_EQUAL = operators.ge
    BETWEEN = "between"
    LIKE = "like"


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    review = Column(Text, nullable=False)


class Diary(Base):
    __tablename__ = "diary"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    year = Column(Integer, nullable=False)
    letterboxd_uri = Column(Text, nullable=False)
    rating = Column(Float)
    rewatch = Column(Text)
    tags = Column(Text)
    watched_date = Column(Text, nullable=False)
    username = Column(Text, nullable=False)
    review_id = Column(Integer, ForeignKey("reviews.id"))


class Database:
    def __init__(self, db_path: str):
        """Initialize a connection to the SQLite database using SQLAlchemy."""
        self.engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    # -------- Helper Method --------

    def _parse_filters(self, table: Diary|Review, filters: List[Dict[str, Any]]) -> List[Any]:
        """
        Convert filter definitions into SQLAlchemy expressions.

        Args:
            filters (list): A list of dictionaries where each dictionary has "column", "operator", and "value".

        Returns:
            list: A list of SQLAlchemy filter conditions.
        """
        conditions = []

        for filter_item in filters:
            column = getattr(table, filter_item["column"], None)
            if not column:
                raise ValueError(f"Column {filter_item['column']} does not exist.")

            operator = filter_item["operator"]
            value = filter_item["value"]

            if operator == Operator.BETWEEN:
                if not isinstance(value, list) or len(value) != 2:
                    raise ValueError("BETWEEN operator requires a list of two values.")
                conditions.append(column.between(value[0], value[1]))
            elif operator == Operator.LIKE:
                conditions.append(column.like(f"%{value}%"))
            elif operator in [Operator.EQUAL, Operator.LESS_THAN_EQUAL, Operator.GREATER_THAN_EQUAL]:
                conditions.append(operator.value(column, value))
            else:
                raise ValueError(f"Unsupported operator: {operator}")

        return conditions

    # -------- Methods for the Diary Table --------

    def filter_diary_entries(self, filters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter diary entries by any combination of fields with specified operators.

        Args:
            filters (list): A list of dictionaries, each containing "column", "operator", and "value".

        Returns:
            list: A list of dictionaries representing matching diary entries.
        """
        session = self.Session()
        try:
            conditions = self._parse_filters(Diary, filters)
            query = session.query(Diary).filter(and_(*conditions))
            return [entry.__dict__ for entry in query.all()]
        except Exception as e:
            logger.error("Error retrieving results from Diary: ", e)
            return []
        finally:
            session.close()

    # -------- Methods for the Reviews Table --------

    def filter_reviews(self, filters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter reviews by any combination of fields with specified operators.

        Args:
            filters (list): A list of dictionaries, each containing "column", "operator", and "value".

        Returns:
            list: A list of dictionaries representing matching reviews.
        """
        session = self.Session()
        try:
            conditions = self._parse_filters(Review, filters)
            query = session.query(Review).filter(and_(*conditions))
            return [review.__dict__ for review in query.all()]
        except Exception as e:
            logger.error("Error retrieving results from Review: ", e)
            return []
        finally:
            session.close()
