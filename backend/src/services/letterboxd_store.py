from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from sqlalchemy import Column, Float, ForeignKey, Integer, Text, and_, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from utils.logger_utils import logger

Base = declarative_base()

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


class LetterboxdStore:
    def __init__(self, db_path: str | Path):
        self.engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def ingest(self, diary_csv: Path, reviews_csv: Path, username: str) -> None:
        _require_columns(reviews_csv, REQUIRED_REVIEWS_COLUMNS)
        _require_columns(diary_csv, REQUIRED_DIARY_COLUMNS)
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        session = self.Session()
        try:
            with reviews_csv.open(encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    session.add(
                        Review(
                            date=row["Date"],
                            name=row["Name"],
                            review=row["Review"],
                        )
                    )
            session.flush()
            with diary_csv.open(encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    linked = (
                        session.query(Review)
                        .filter_by(name=row["Name"], date=row["Date"])
                        .first()
                    )
                    session.add(
                        Diary(
                            date=row["Date"],
                            name=row["Name"],
                            year=int(row["Year"]),
                            letterboxd_uri=row["Letterboxd URI"],
                            rating=float(row["Rating"]) if row["Rating"] else None,
                            rewatch=row["Rewatch"],
                            tags=row["Tags"],
                            watched_date=row["Watched Date"],
                            username=username,
                            review_id=linked.id if linked else None,
                        )
                    )
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
        logger.info("Letterboxd export loaded")

    def owner_username(self) -> str:
        session = self.Session()
        try:
            value = session.query(Diary.username).limit(1).scalar()
            return value or ""
        finally:
            session.close()

    def filter_diary(
        self,
        *,
        name: str | None = None,
        from_watched_date: str | None = None,
        to_watched_date: str | None = None,
        from_rating: float | None = None,
        to_rating: float | None = None,
        rewatch: str | None = None,
        year: int | None = None,
    ) -> list[dict[str, Any]]:
        session = self.Session()
        try:
            query = session.query(Diary)
            if name:
                query = query.filter(Diary.name.like(f"%{name}%"))
            query = _apply_range(
                query, Diary.watched_date, from_watched_date, to_watched_date
            )
            query = _apply_range(query, Diary.rating, from_rating, to_rating)
            if rewatch:
                query = query.filter(Diary.rewatch == rewatch)
            if year is not None:
                query = query.filter(Diary.year == year)
            return [_as_dict(entry) for entry in query.all()]
        except Exception as exc:
            logger.error("Error retrieving results from Diary: %s", exc)
            return []
        finally:
            session.close()

    def filter_reviews(
        self,
        *,
        name: str | None = None,
        review_id: str | int | None = None,
    ) -> list[dict[str, Any]]:
        session = self.Session()
        try:
            query = session.query(Review)
            if review_id is not None and review_id != "":
                query = query.filter(Review.id == int(review_id))
            elif name:
                query = query.filter(Review.name.like(f"%{name}%"))
            return [_as_dict(entry) for entry in query.all()]
        except Exception as exc:
            logger.error("Error retrieving results from Review: %s", exc)
            return []
        finally:
            session.close()

    def on_this_day(
        self,
        month_day: str,
        *,
        min_rating: float = 4.0,
        max_rating: float = 5.0,
    ) -> list[dict[str, Any]]:
        session = self.Session()
        try:
            query = session.query(Diary).filter(
                and_(
                    Diary.watched_date.like(f"%{month_day}"),
                    Diary.rating.between(min_rating, max_rating),
                )
            )
            return [_as_dict(entry) for entry in query.all()]
        except Exception as exc:
            logger.error("Error retrieving on-this-day Diary: %s", exc)
            return []
        finally:
            session.close()


def _apply_range(query, column, from_value, to_value):
    if from_value is not None and to_value is not None:
        return query.filter(column.between(from_value, to_value))
    if from_value is not None:
        return query.filter(column >= from_value)
    if to_value is not None:
        return query.filter(column <= to_value)
    return query


def _as_dict(model) -> dict[str, Any]:
    return {
        column.name: getattr(model, column.name) for column in model.__table__.columns
    }


def _require_columns(path: Path, required: list[str]) -> None:
    with path.open(encoding="utf-8") as handle:
        fieldnames = csv.DictReader(handle).fieldnames or []
    missing = [column for column in required if column not in fieldnames]
    if missing:
        raise ValueError(
            f"Missing required column '{missing[0]}' in {path.name}"
        )
