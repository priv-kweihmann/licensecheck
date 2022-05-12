import logging
import sys


def setup(name, stream=sys.stdout, level=logging.INFO, format='%(levelname)s %(message)s'):
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter(format))
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
