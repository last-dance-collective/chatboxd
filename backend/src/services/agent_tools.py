from __future__ import annotations

import json
import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal

from api.schemas import MovieCard
from catalog.translations import TOOL_RESPONSES, TRANSLATIONS
from paths import DB_PATH
from services.graph_services import GRAPH_TYPES
from services.movies_data_service import get_letterboxd_data, get_omdb_data
from services.sqlite_service import Database, Operator
from utils.logger_utils import logger


@dataclass(frozen=True)
class GraphArtifact:
    data: list[float]


ToolArtifact = MovieCard | GraphArtifact


@dataclass(frozen=True)
class ToolBundle:
    tool: Callable[..., Any]
    status_from_args: Callable[[dict[str, Any], str], str | None] | None = None
    artifacts_from_result: Callable[[Any], ToolArtifact | None] | None = None

    @property
    def name(self) -> str:
        return self.tool.__name__


def get_reviews(
    name: str = None,
    review_id: str = None,
) -> str:
    """Retrieve reviews from movies watched by the user, searching by movie name or by review id.
    Before calling this tool, it is necessary to retrieve the registry of watched movies.

    Params:
        name (str): movie title (in English).
        review_id (str): movie review_id

    Returns:
        str: Description of retrieved reviews.
    """
    db = Database(str(DB_PATH))
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
) -> str:
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
    db = Database(str(DB_PATH))
    movies = db.filter_diary_entries(filters=filters)

    return TOOL_RESPONSES["EN"]["get_movies_response"] + str(movies)


def get_movie_details_extended(title: str, letterboxd_url: str) -> tuple[str, dict]:
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
            movie_detail=str(omdb_data)
        )
    ), {"movies": data}


def get_movie_details(letterboxd_url: str) -> tuple[str, dict]:
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


def get_graph(movies: list[dict[str, Any]]) -> dict[str, Any]:
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


def create_two_params_filter(
    param_name: str, from_param: Any, to_param: Any
) -> dict[str, Any]:
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


def _texts_for(language: str) -> dict[str, Any]:
    return TRANSLATIONS.get(language, TRANSLATIONS["EN"])


def _title_info(tool_args: dict[str, Any], texts: dict[str, Any]) -> str:
    name = tool_args.get("name")
    return texts["title_filter"].format(name=name) if name else ""


def _review_id_info(tool_args: dict[str, Any], texts: dict[str, Any]) -> str:
    review_id = tool_args.get("review_id")
    return texts["title_filter"].format(name=review_id) if review_id else ""


def _watched_date_info(tool_args: dict[str, Any], texts: dict[str, Any]) -> str:
    from_date = tool_args.get("from_watched_date")
    to_date = tool_args.get("to_watched_date")
    if not from_date and not to_date:
        return ""
    to_date = to_date or "hoy"
    if from_date:
        return texts["date_range_filter"].format(from_date=from_date, to_date=to_date)
    return texts["date_to_filter"].format(to_date=to_date)


def _rating_info(tool_args: dict[str, Any], texts: dict[str, Any]) -> str:
    from_rating = tool_args.get("from_rating")
    to_rating = tool_args.get("to_rating")
    if from_rating is None and to_rating is None:
        return ""
    from_rating = from_rating if from_rating is not None else 0
    to_rating = to_rating if to_rating is not None else 5
    if from_rating != to_rating:
        return texts["rating_range_filter"].format(
            from_rating=from_rating, to_rating=to_rating
        )
    return texts["rating_filter"].format(from_rating=from_rating)


def _release_year_info(tool_args: dict[str, Any], texts: dict[str, Any]) -> str:
    year = tool_args.get("year")
    return texts["year_filter"].format(year=year) if year else ""


def _rewatch_info(tool_args: dict[str, Any], texts: dict[str, Any]) -> str:
    return texts["rewatch"] if tool_args.get("rewatch") else ""


def _reviews_status(tool_args: dict[str, Any], language: str) -> str | None:
    texts = _texts_for(language)
    filter_str = _title_info(tool_args, texts)
    filter_str += _review_id_info(tool_args, texts)
    initial = texts["reviews_filter_loading"] if filter_str else texts["reviews_loading"]
    return initial + filter_str


def _movies_status(tool_args: dict[str, Any], language: str) -> str | None:
    texts = _texts_for(language)
    filter_str = _title_info(tool_args, texts)
    filter_str += _watched_date_info(tool_args, texts)
    filter_str += _rating_info(tool_args, texts)
    filter_str += _release_year_info(tool_args, texts)
    filter_str += _rewatch_info(tool_args, texts)
    initial = texts["film_filter_loading"] if filter_str else texts["film_loading"]
    return initial + filter_str


def _parse_jsonish(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return value
    if hasattr(value, "content"):
        return _parse_jsonish(value.content)
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _movie_card_from_result(output: Any) -> MovieCard | None:
    parsed = _parse_jsonish(output)
    payload: Any = parsed
    if isinstance(parsed, (list, tuple)) and len(parsed) >= 2:
        payload = parsed[1]
    if isinstance(payload, dict) and "movies" in payload:
        payload = payload["movies"]
    if not isinstance(payload, dict):
        return None
    title = payload.get("title")
    url = payload.get("url")
    image_url = payload.get("image_url")
    if not title or not url or not image_url:
        return None
    ratings = payload.get("ratings") or []
    if not isinstance(ratings, list):
        ratings = []
    return MovieCard(
        title=str(title),
        url=str(url),
        image_url=str(image_url),
        plot=str(payload.get("plot") or ""),
        ratings=ratings,
    )


def _graph_from_result(output: Any) -> GraphArtifact | None:
    parsed = _parse_jsonish(output)
    if isinstance(parsed, dict) and parsed.get("obj_type") == "graph":
        data = parsed.get("data") or []
        try:
            return GraphArtifact(data=[float(v) for v in data])
        except (TypeError, ValueError):
            return None
    return None


REVIEWS_BUNDLE = ToolBundle(tool=get_reviews, status_from_args=_reviews_status)
MOVIES_BUNDLE = ToolBundle(tool=get_movies, status_from_args=_movies_status)
GRAPH_BUNDLE = ToolBundle(tool=get_graph, artifacts_from_result=_graph_from_result)
MOVIE_DETAILS_BUNDLE = ToolBundle(
    tool=get_movie_details, artifacts_from_result=_movie_card_from_result
)
MOVIE_DETAILS_EXTENDED_BUNDLE = ToolBundle(
    tool=get_movie_details_extended, artifacts_from_result=_movie_card_from_result
)

BUNDLES: tuple[ToolBundle, ...] = (
    MOVIES_BUNDLE,
    REVIEWS_BUNDLE,
    GRAPH_BUNDLE,
    MOVIE_DETAILS_BUNDLE,
    MOVIE_DETAILS_EXTENDED_BUNDLE,
)


def bundle_for(name: str) -> ToolBundle | None:
    for bundle in BUNDLES:
        if bundle.name == name:
            return bundle
    return None


def agent_bundles() -> tuple[ToolBundle, ...]:
    if os.environ.get("OMDB_API_KEY"):
        logger.info("OMDB key is present, get details tool extended enabled")
        details = MOVIE_DETAILS_EXTENDED_BUNDLE
    else:
        logger.info("OMDB key is NOT present, get details tool extended disabled")
        details = MOVIE_DETAILS_BUNDLE
    return (MOVIES_BUNDLE, REVIEWS_BUNDLE, GRAPH_BUNDLE, details)
