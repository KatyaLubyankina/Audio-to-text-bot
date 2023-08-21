import functools
import sys

from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    colorize=False,
    format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>",
    level="DEBUG",
)


def logger_wraps(*, entry=True, exit=True, level="DEBUG"):
    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(**kwargs):
            logger_ = logger.opt(depth=1)
            if entry:
                logger_.log(level, "Entering '{}' (kwargs={})", name, kwargs)
            result = func(**kwargs)
            if exit:
                logger_.log(level, "Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    return wrapper
