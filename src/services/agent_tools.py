from typing import Dict, Any, Literal

from services.sqlite_service import Database, Operator

from utils.logger_utils import logger


def get_movies(
    name: str = None,
    from_watched_date: str = None,
    to_watched_date: str = None,
    from_rating: float = None,
    to_rating: float = None,
    rewatch: Literal["Yes"] = None,
    year: int = None,
):
    """Filtra las películas registradas del usuario de acuerdo a los parámetros
     identificados en la petición del usuario y obtiene la información relacionada con ella

    Params:
        name (str): nombre de la película en inglés.
        from_watched_date (str): fecha desde la que se inicia el abanico de búsqueda de cuando se vio la película.
        to_watched_date (str): fecha que cierra el abanico de búsqueda de cuando se vio la película.
        from_rating (float): nota que puso el usuario a la película desde la que se inicia el abanico de búsqueda.
        to_rating (float): nota que puso el usuario a la película que cierra el abanico de búsqueda.
        rewatch (str): flag para obtener unicamente las segundas o más vistas de una película.
        year (int): año en el que se estrenó la película.

    Returns:
        str: Descripción de las películas filtrados.
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

    return {
        "messages": movies,
    }


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
