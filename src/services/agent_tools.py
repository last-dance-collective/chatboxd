from typing import Dict, List, Any, Literal

from services.graph_services import GRAPH_TYPES
from services.sqlite_service import Database, Operator
from services.movies_data_service import (
    get_omdb_data,
    get_letterboxd_data,
)
from utils.logger_utils import logger
from catalog.translations import TOOL_RESPONSES


def get_reviews(
    name: str = None,
    review_id: str = None,
):
    """Retrieve reviews from movies watched by the user, searching by movie name or by review id.
    Before calling this tool, it is necessary to retrieve the registry of watched movies.

    Params:
        name (str): movie title (in English).
        review_id (str): movie review_id

    Returns:
        str: Description of retrieved reviews.
    """
    db = Database("letterboxd.db")
    if review_id:
        filter = [{"column": "id", "operator": Operator.EQUAL, "value": review_id}]
    else:
        filter = [{"column": "name", "operator": Operator.LIKE, "value": name}]

    logger.info(f"🔍 Filters: {filter}")
    reviews = db.filter_reviews(filter)

    return TOOL_RESPONSES["EN"]["get_reviews_response"] + str(reviews)


def get_movies(
    name: str = None,
    from_watched_date: str = None,
    to_watched_date: str = None,
    from_rating: float = None,
    to_rating: float = None,
    rewatch: Literal["Yes"] = None,
    year: int = None,
):
    """Filters the user movie registry according to the search parameters identified in the user query,
    then retrieves the search result.

    Params:
        name (str): movie title (in English).
        from_watched_date (str): start of the watched date range.
        to_watched_date (str): end of the watched date range.
        from_rating (float): minimum user rating (out of 5 stars).
        to_rating (float): maximum user rating (out of 5 stars).
        rewatch (str): flag to retrieve only rewatches (movies that were already watched).
        year (int): year in which the movie was released.

    Returns:
        str: Description of retrieved movies.
    """
    filters = [
        create_two_params_filter("watched_date", from_watched_date, to_watched_date),
        create_two_params_filter("rating", from_rating, to_rating),
        {"column": "name", "operator": Operator.LIKE, "value": name},
        {"column": "rewatch", "operator": Operator.EQUAL, "value": rewatch},
        {"column": "year", "operator": Operator.EQUAL, "value": year},
    ]

    filters = [filter for filter in filters if filter["value"] is not None]
    logger.info(f"🔍 Filters: {filters}")
    db = Database("letterboxd.db")
    movies = db.filter_diary_entries(filters=filters)

    return TOOL_RESPONSES["EN"]["get_movies_response"] + str(movies)


def get_movie_details_extended(title: str, letterboxd_url: str):
    """Retrieves the detail of a movie by its title (in English) and its Letterboxd URL. This tool
    is the only way to obtain the detail of any movie. Before calling this tool, it is necessary to
    obtain the registry of watched movies.

    Params:
        title (str): movie title (in English).
        letterboxd_url (str): Letterboxd URL for the movie.

    Returns:
        str: Detailed description of the movie.
    """
    omdb_data = get_omdb_data(title)
    letterboxd_data = get_letterboxd_data(letterboxd_url)

    if omdb_data == {} or letterboxd_data == {}:
        return TOOL_RESPONSES["EN"]["movie_details_not_found"]

    data = {
        "title": letterboxd_data["title"],
        "url": letterboxd_url,
        "image_url": letterboxd_data["image_url"],
        "plot": omdb_data["Plot"],
        "ratings": omdb_data["Ratings"],
    }

    del omdb_data["Plot"]
    del omdb_data["Ratings"]

    return (
        TOOL_RESPONSES["EN"]["get_movie_details_response"].format(
            {"movie_detail": str(omdb_data)}
        )
    ), {"movies": data}


def get_movie_details(letterboxd_url: str):
    """Retrieves the detail of a movie by its Letterboxd URL. This tool is the
    only way to obtain the detail of any movie. Before calling this tool, it is
    necessary to obtain the registry of watched movies.

    Params:
        letterboxd_url (str): Letterboxd URL for the movie.

    Returns:
        str: Detailed description of the movie.
    """
    letterboxd_data = get_letterboxd_data(letterboxd_url)

    if letterboxd_data == {}:
        return TOOL_RESPONSES["EN"]["movie_details_not_found"]

    data = {
        "title": letterboxd_data["title"],
        "url": letterboxd_url,
        "image_url": letterboxd_data["image_url"],
    }
    return TOOL_RESPONSES["EN"]["get_movie_details_response"].format(
        {"movie_detail": str(data)}
    ), {"movies": data}


def get_graph(movies: List[Dict[str, Any]]):
    """
    Generates and displays a graph based upon the provided list of movies.

    Params:
        movies (List[Dict[str, Any]]): a list of movies to be included in the graph.

    Returns:
        dict: A dictionary including the graph type and the information to be displayed.
    """
    ratings = [movie["rating"] for movie in movies]
    return {
        "obj_type": "graph",
        "graph_type": GRAPH_TYPES.RATING_DISTRIBUTION.value,
        "data": ratings,
        "indicaciones": TOOL_RESPONSES["EN"]["get_graph_response"],
    }


# Aux mehtods


def create_two_params_filter(
    param_name: str, from_param: Any, to_param: Any
) -> Dict[str, Any]:
    if from_param and to_param:
        return {
            "column": param_name,
            "operator": Operator.BETWEEN,
            "value": [from_param, to_param],
        }
    elif from_param:
        return {
            "column": param_name,
            "operator": Operator.GREATER_THAN_EQUAL,
            "value": from_param,
        }
    elif to_param:
        return {
            "column": param_name,
            "operator": Operator.LESS_THAN_EQUAL,
            "value": to_param,
        }
    else:
        return {
            "column": param_name,
            "operator": Operator.LESS_THAN_EQUAL,
            "value": None,
        }
