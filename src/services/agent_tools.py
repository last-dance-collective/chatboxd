from typing import Dict, Any, Literal

from services.sqlite_service import Database, Operator
from services.movies_data_service import (
    get_omdb_data,
    get_letterboxd_data,
)
from utils.logger_utils import logger


def get_reviews(
    name: str = None,
    review_id: str = None,
):
    """Obtiene las reviews de las películas que el usuario ha visto, ya sea por nombre o por review_id de la película
     obtenida de una petición anterior del usuario.
      Antes de llamar a esta función es necesario obtener los registros de películas del usuario

    Params:
        name (str): nombre de la película en inglés.
        review_id (str): review_id de la película

    Returns:
        str: Descripción de las reviews.
    """
    db = Database("letterboxd.db")
    if review_id:
        filter = [{"column": "id", "operator": Operator.EQUAL, "value": review_id}]
    else:
        filter = [{"column": "name", "operator": Operator.LIKE, "value": name}]

    logger.info(f"🔍 Filters: {filter}")
    reviews = db.filter_reviews(filter)

    return (
        "El usuario ha hecho las siguientes reviews de las películas que ha visto:\n"
        + str(reviews)
    )


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

    return (
        "De acuerdo a los filtros que me has dado, el usuario ha visto las siguiente películas:\n"
        + str(movies)
    )


def get_movie_details(title: str, letterboxd_url: str):
    """Obtiene los detalles de una película mediante el titulo en inglés y el uso de una API externa.
        Esta función es la única manera de conseguir el detalle de la película.
        Antes de llamar a esta función es necesario obtener los registros de películas del usuario

    Params:
        title (str): nombre de la película en inglés.
        letterboxd_url (str): url de la película en letterboxd.

    Returns:
        str: Descripción de la película.
    """
    omdb_data = get_omdb_data(title)
    letterboxd_data = get_letterboxd_data(letterboxd_url)

    if omdb_data == {} or letterboxd_data == {}:
        return "No se encontraron detalles de la película"

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
        "🎬 Los detalles de la película son (Añade emojis para que visualmente se vea mejor):\n"
        + str(omdb_data)
        + "\n\n  En ningún caso debes mostrar una imagen ni la sinopsis, ni los Ratings. El diccionario que viene a continuación es irrelevante para ti, no lo hagas caso. "
    ), {"movies": data}


def get_letterboxd_film_details(url: str):
    """
    Obtiene los detalles de una película desde Letterboxd.

    Params:
        url (str): La url de la película en Letterboxd.

    Returns:
        str: Un elemento html con una tarjeta para ser mostrada en el frontal
    """
    data = get_letterboxd_data(url)
    return {
        "obj_type": "movie_detail",
        "movies": data,
        "indicaciones": "no se tiene que mostrar la imagen, solo los detalles de la pelicula",
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
