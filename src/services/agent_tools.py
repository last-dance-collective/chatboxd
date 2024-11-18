from typing import Optional, Dict, Any

from services.sqlite_service import Database, Operator


def get_movies(
    name: str = None,
    from_watched_date: str = None,
    to_watched_date: str = None,
    from_rating: float = None,
    to_rating: float = None,
    rewatch: int = None,
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
        rewatch (str): flag que indica si la película se había visto anteriormente o no.
        year (int): año en el que se estrenó la película.

    Returns:
        str: Descripción de las películas filtrados.
    """

    filters = [
      create_watched_date_filter(from_watched_date, to_watched_date),
      create_rating_filter(from_rating, to_rating),
      {
        "column": "name", "operator": Operator.EQUAL, "value": name
      },
      {
        "column": "rewatch", "operator": Operator.EQUAL, "value": rewatch
      },
      {
        "column": "year", "operator": Operator.EQUAL, "value": year
      }
    ]
    
    filters = [filter for filter in filters if filter["value"] is not None]
    db = Database("letterboxd.db")
    movies = db.filter_diary_entries(filters=filters)

    return {
        "messages": movies,
    }
    
def create_watched_date_filter(from_watched_date: Optional[str], to_watched_date: Optional[str]) -> Dict[str, Any]:
    if from_watched_date and to_watched_date:
        return {"column": "watched_date", "operator": Operator.BETWEEN, "value": [from_watched_date, to_watched_date]}
    elif from_watched_date:
        return {"column": "watched_date", "operator": Operator.GREATER_THAN_EQUAL, "value": from_watched_date}
    elif to_watched_date:
        return {"column": "watched_date", "operator": Operator.LESS_THAN_EQUAL, "value": to_watched_date}
    else:
        return {"column": "watched_date", "operator": Operator.LESS_THAN_EQUAL, "value": None}

def create_rating_filter(from_rating: Optional[float], to_rating: Optional[float]) -> Dict[str, Any]:
    if from_rating and to_rating:
        return {"column": "rating", "operator": Operator.BETWEEN, "value": [from_rating, to_rating]}
    elif from_rating:
        return {"column": "rating", "operator": Operator.GREATER_THAN_EQUAL, "value": from_rating}
    elif to_rating:
        return {"column": "rating", "operator": Operator.LESS_THAN_EQUAL, "value": to_rating}
    else:
        return {"column": "rating", "operator": Operator.LESS_THAN_EQUAL, "value": None}