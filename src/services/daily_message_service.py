from datetime import datetime
from typing import Any, Dict, List

from services.sqlite_service import Database, Operator
from utils.session_utils import get_session_val


def get_daily_message():
    now = datetime.now().strftime("%Y-%m-%d")
    entries = find_diary_entry(now)
    return compose_message(entries)


def find_diary_entry(date: str) -> List[Dict[str, Any]]:
    db = Database("letterboxd.db")

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
    entries = db.filter_diary_entries(filters=filters)
    return entries


def compose_message(entries: List[Dict[str, Any]]) -> str:
    number_of_entries = len(entries)
    if number_of_entries == 1:
        return compose_message_for_one_movie(entries[0])
    elif number_of_entries > 1:
        return compose_message_more_than_one_movie(entries)


def compose_message_for_one_movie(movie: Dict[str, Any]) -> str:
    texts = get_session_val("texts")
    return texts["one_movie_daily_msg"].format(
        year=movie["date"][:4],
        m_name=movie["name"],
        m_year=movie["year"],
        m_uri=movie["letterboxd_uri"],
        m_rating=movie["rating"],
    )


def compose_message_more_than_one_movie(movies: List[Dict[str, Any]]) -> str:
    texts = get_session_val("texts")

    content = "\n".join(
        texts["many_movies_daily_msg"].format(
            year=movie["date"][:4], name=movie["name"], m_year=movie["year"]
        )
        for movie in movies
    )
    return f"{texts['daly_msg_start']}{content}"
