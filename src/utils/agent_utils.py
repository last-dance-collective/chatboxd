import pandas as pd
import json

from utils.logger_utils import logger


def get_df(event):
    if event["data"]["output"]["messages"]:
        if not event["data"]["output"]["messages"][-2].content:
            return None
        try:
            message = json.loads(event["data"]["output"]["messages"][-2].content)[
                "messages"
            ]
            if message.get("obj_type", None) == "dict":
                return pd.DataFrame(message.get("movies", {}))
        except Exception as e:
            logger.warning(f"The message does not conain data to build a df: {e}")
            return None
    return None


def extract_image_data(event):
    message = json.loads(event["data"]["output"].content)
    if message[1].get("movies", None):
        return message[1].get("movies", {})
    else:
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
    del response["Plot"]
    del response["imdbRating"]
    del response["Production"]
    del response["Ratings"]

    return str(response)
