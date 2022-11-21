import logging

from utils import *

_logger = None

class _CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s - %(message)s" # %(name)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def _initialize_logger():
    """
    Inicializa el logger en caso de no estarlo ya.
    :return:
    """

    # Única instancia del logger
    global _logger

    # Creamos el logger
    _logger = logging.getLogger(APP_NAME)
    _logger.setLevel(APP_MODE)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(APP_MODE)
    ch.setFormatter(_CustomFormatter())
    _logger.addHandler(ch)

    return _logger


Logger = _initialize_logger() if _logger is None else _logger
