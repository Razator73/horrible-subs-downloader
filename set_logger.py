import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def define_logger(name):
    logger = logging.Logger(name)
    logger.setLevel(logging.INFO)
    try:
        log_path = Path(__file__).parent / 'script-logs' / 'download.log'
    except NameError:
        log_path = Path('script-logs') / 'download.log'
    handler = RotatingFileHandler(log_path, maxBytes=1048576, backupCount=5)
    formatter = logging.Formatter('\n%(asctime)s - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
