from typing import Dict, Any, Literal
import requests
from bs4 import BeautifulSoup

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
        "messages": {"obj_type": "dict", "movies": movies},
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

def get_letterboxd_film_details(url: str):
    """
    Obtiene los detalles de una película desde Letterboxd.

    Params:
        url (str): La url de la película en Letterboxd.

    Returns:
        str: Un elemento html con una tarjeta para ser mostrada en el frontal
    """
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    
    og_title = soup.find("meta", property="og:title")["content"]
    og_image = soup.find("meta", property="og:image")["content"]
    
    data = {
        "title": og_title,
        "url": url,
        "image_url": og_image
    }
    return {
        "messages": {"obj_type": "movie_detail", "movies": data, "indicaciones": "no se tiene que mostrar la imagen, solo los detalles de la pelicula"},
    }
