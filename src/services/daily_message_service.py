import sqlite3
from datetime import datetime

# Define el nombre del archivo de la base de datos y el nombre de usuario
db_file = "letterboxd.db"
username = "mavilam"


# Función principal para obtener el mensaje diario
def get_daily_message():
    now = datetime.now().strftime("%Y-%m-%d")
    entries = find_diary_entry(now)
    return compose_message(entries)


# Función para buscar entradas del diario
def find_diary_entry(date):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    query = "SELECT * FROM diary WHERE watched_date LIKE ? AND username = ? AND rating >= 4.0"
    cursor.execute(query, (f"%{date[4:]}", username))
    entries = cursor.fetchall()
    connection.close()
    return entries


# Función para componer el mensaje
def compose_message(entries):
    number_of_entries = len(entries)
    if number_of_entries == 1:
        return compose_message_for_one_movie(entries[0])
    elif number_of_entries > 1:
        return compose_message_more_than_one_movie(entries)


# Función para componer un mensaje cuando hay una película
def compose_message_for_one_movie(movie):
    watched_date, name, letterboxd_uri, rating, *_ = movie
    return f"Tal día como hoy en {watched_date[:4]} viste {name} ({letterboxd_uri}). Le pusiste un {rating}"


# Función para componer un mensaje cuando hay varias películas
def compose_message_more_than_one_movie(movies):
    start_message = "Tal día como hoy viste varias películas de peso: \n"
    content = "\n".join(
        f"* En {movie[1][:4]} viste {movie[2]} ({movie[3]})." for movie in movies
    )
    return f"{start_message}{content}"


# Ejemplo de uso
if __name__ == "__main__":
    message = get_daily_message()
    print(message)
