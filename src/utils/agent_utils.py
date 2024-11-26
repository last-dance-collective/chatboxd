import json

from utils.logger_utils import logger
from services.graph_services import display_rating_graph


def display_graph(event):
    if event["data"]["output"]["messages"]:
        if not event["data"]["output"]["messages"][-2].content:
            return None
        try:
            message = json.loads(event["data"]["output"]["messages"][-2].content)
            if message.get("obj_type", None) == "graph":
                display_rating_graph(message.get("data", None))
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
