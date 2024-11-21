import requests
from bs4 import BeautifulSoup
import os

from utils.logger_utils import logger

BASE_OMDB_URL = "http://www.omdbapi.com/?apikey={api_key}&t={title}"

def get_letterboxd_data(letterboxd_url):
    try:
      response_lb = requests.get(letterboxd_url, headers={"User-Agent": "Mozilla/5.0"})
      soup = BeautifulSoup(response_lb.text, "html.parser")

      og_title = soup.find("meta", property="og:title")["content"]
      og_image = soup.find("meta", property="og:image")["content"]
      return {"title": og_title, "url": letterboxd_url, "image_url": og_image}
    except Exception as e:
      logger.error(f"Error getting OG data from Letterboxd: {e}")
      return {}

def get_omdb_data(title):
    url = BASE_OMDB_URL.format(api_key=os.environ["OMDB_API_KEY"], title=title)
    try:
      response = requests.get(url)
      return clean_omdb_response(response.json())
    except Exception as e:
      logger.error(f"Error getting data from OMDB: {e}")
      return {}

def clean_omdb_response(response: dict):
    del response["Rated"]
    del response["Year"]
    del response["Language"]
    del response["Poster"]
    del response["Type"]
    del response["Website"]
    del response["Response"]
    del response["DVD"]
    del response["imdbVotes"]
    del response["Metascore"]
    del response["imdbID"]
    del response["imdbRating"]
    del response["Production"]

    return response