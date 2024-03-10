import logging


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('{levelname} - {asctime} - {name} - {message}', style='{'))
    logger.addHandler(console_handler)
