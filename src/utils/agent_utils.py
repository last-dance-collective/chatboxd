import pandas as pd
import json

from utils.logger_utils import logger

def get_df(event):
    if event["data"]["output"]["messages"]:
        if not event["data"]["output"]["messages"][-2].content:
            return None
        try:
            message = json.loads(event["data"]["output"]["messages"][-2].content)["messages"]
            if (message.get("obj_type", None) == "dict"):
                return pd.DataFrame(
                   message.get("movies", {})
                )
        except Exception as e:
            logger.warning(f"The message does not conain data to build a df: {e}")
            return None
    return None

def extract_image_data(event):
    message = json.loads(event["data"]["output"].content)["messages"]
    if (message.get("obj_type", None) == "movie_detail"):
        return message.get("movies", {})
    else:
        return {}