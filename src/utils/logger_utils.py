import logging


def initialize_logger(name="chatboxd", level=logging.INFO):
    logging.getLogger("py4j.clientserver").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.basicConfig(
        level=level,
        format="%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    return logging.getLogger(name)


logger = initialize_logger()