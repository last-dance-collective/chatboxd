from datetime import datetime
from typing import Any, Dict, List

from catalog.translations import TRANSLATIONS
from paths import DB_PATH
from services.sqlite_service import Database, Operator


def get_daily_message(language: str = "EN") -> str | None:
    now = datetime.now().strftime("%Y-%m-%d")
    entries = find_diary_entry(now)
    return compose_message(entries, language)


def find_diary_entry(date: str) -> List[Dict[str, Any]]:
    db = Database(str(DB_PATH))
    filters = [
        {
            "column": "watched_date",
            "operator": Operator.LIKE,
            "value": date[4:10],
        },
        {
            "column": "rating",
            "operator": Operator.BETWEEN,
            "value": [4.0, 5.0],
        },
    ]
    return db.filter_diary_entries(filters=filters)


def compose_message(entries: List[Dict[str, Any]], language: str) -> str | None:
    number_of_entries = len(entries)
    if number_of_entries == 1:
        return compose_message_for_one_movie(entries[0], language)
    if number_of_entries > 1:
        return compose_message_more_than_one_movie(entries, language)
    return None


def _texts(language: str) -> dict[str, Any]:
    return TRANSLATIONS.get(language, TRANSLATIONS["EN"])


def compose_message_for_one_movie(movie: Dict[str, Any], language: str) -> str:
    texts = _texts(language)
    return texts["one_movie_daily_msg"].format(
        year=movie["date"][:4],
        m_name=movie["name"],
        m_year=movie["year"],
        m_uri=movie["letterboxd_uri"],
        m_rating=movie["rating"],
    )


def compose_message_more_than_one_movie(
    movies: List[Dict[str, Any]], language: str
) -> str:
    texts = _texts(language)
    content = "\n".join(
        texts["many_movies_daily_msg"].format(
            year=movie["date"][:4], name=movie["name"], m_year=movie["year"]
        )
        for movie in movies
    )
    return f"{texts['daly_msg_start']}{content}"
