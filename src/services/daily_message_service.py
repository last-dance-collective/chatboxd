from datetime import datetime

from services.sqlite_service import Database, Operator

db = Database("letterboxd.db")


def get_daily_message():
    now = datetime.now().strftime("%Y-%m-%d")
    entries = find_diary_entry(now)
    return compose_message(entries)


def find_diary_entry(date):
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


def compose_message(entries):
    number_of_entries = len(entries)
    if number_of_entries == 1:
        return compose_message_for_one_movie(entries[0])
    elif number_of_entries > 1:
        return compose_message_more_than_one_movie(entries)


def compose_message_for_one_movie(movie):
    return f"Tal día como hoy en {movie["date"][:4]} viste [{movie["name"]} ({movie["year"]})]({movie["letterboxd_uri"]}). Le pusiste un {movie["rating"]}."


def compose_message_more_than_one_movie(movies):
    start_message = "Tal día como hoy viste varias películas de peso: \n"
    content = "\n".join(
        f"* En {movie["date"][:4]} viste {movie["name"]} ({movie["year"]})."
        for movie in movies
    )
    return f"{start_message}{content}"
