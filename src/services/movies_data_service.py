import requests
from bs4 import BeautifulSoup
import os

from utils.logger_utils import logger

BASE_OMDB_URL = "http://www.omdbapi.com/?apikey={api_key}&t={title}"


def get_letterboxd_data(letterboxd_url: str) -> dict:
    try:
        response_lb = requests.get(
            letterboxd_url, headers={"User-Agent": "Mozilla/5.0"}
        )
        soup = BeautifulSoup(response_lb.text, "html.parser")

        og_title = soup.find("meta", property="og:title")["content"]
        og_image = soup.find("meta", property="og:image")["content"]
        return {"title": og_title, "url": letterboxd_url, "image_url": og_image}
    except Exception as e:
        logger.error(f"Error getting OG data from Letterboxd: {e}")
        return {}


def get_omdb_data(title: str) -> dict:
    url = BASE_OMDB_URL.format(api_key=os.environ["OMDB_API_KEY"], title=title)
    try:
        response = requests.get(url)
        return clean_omdb_response(response.json())
    except Exception as e:
        logger.error(f"Error getting data from OMDB: {e}")
        return {}


def clean_omdb_response(response: dict) -> dict:
    params_to_delete = [
        "Rated",
        "Year",
        "Language",
        "Poster",
        "Type",
        "Website",
        "Response",
        "DVD",
        "imdbVotes",
        "Metascore",
        "imdbID",
        "imdbRating",
        "Production",
    ]
    for param in params_to_delete:
        del response[param]

    return response
