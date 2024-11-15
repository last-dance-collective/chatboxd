import pandas as pd

from services.sqlite_service import Database, Operator


def saludar() -> str:
    """Obtiene el saludo correcto al usuario"""
    return "El usuario se llama Mávila, saludale cortesmente!"


def get_films(date_from: str, date_to: str) -> str:
    """Obtiene las películas del usuario que vio en el rango de fechas
    Args:
        date_from (str): fecha de inicio
        date_to (str): fecha de fin
    Returns:
        str: la tabla de películas
    """
    db = Database("letterboxd.db")
    last_month_entries = db.filter_diary_entries(
        [
            {
                "column": "watched_date",
                "operator": Operator.GREATER_THAN_EQUAL,
                "value": date_from,
            },
            {
                "column": "watched_date",
                "operator": Operator.LESS_THAN_EQUAL,
                "value": date_to,
            },
        ]
    )
    df = pd.DataFrame(last_month_entries)
    df_str = df.to_markdown(index=False) + "\n"
    return f"Las películas que ha visto el usuario entre las fechas {date_from} y {date_to} son:\n\n{df_str}"
