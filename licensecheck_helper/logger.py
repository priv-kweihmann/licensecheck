import logging
import sys


def setup(name, stream=sys.stdout, level=logging.INFO, format_='%(levelname)s %(message)s'):
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter(format_))
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
