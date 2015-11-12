import logging
import sys


def get_logger():
    logger = logging.getLogger('console')
    handler_console = logging.StreamHandler(sys.stdout)
    handler_console.setLevel(logging.INFO)

    # red bold font
    formatter = logging.Formatter(
        '\x1b[31;1m%(levelname)s: %(message)s\n\x1b[0m')

    handler_console.setFormatter(formatter)
    logger.addHandler(handler_console)
    return logger
