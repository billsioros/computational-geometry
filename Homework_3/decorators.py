
import logging
from functools import wraps
from time import time

from click import echo, style


def safe(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Exception as e:
            name = method.__name__.replace('_', ' ').title()
            echo(style(f'{name}: ', bold=True) + str(e))
            exit(1)

    return wrapper


def benchmark(method):
    logger = logging.getLogger(method.__name__.replace("_", " ").upper())

    logging.basicConfig(
        format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    def wrapper(*args, **kwargs):
        ts = time()
        result = method(*args, **kwargs)
        te = time()

        logger.info('%09.4f ms elapsed' % ((te - ts) * 1000,))

        return result

    return wrapper
