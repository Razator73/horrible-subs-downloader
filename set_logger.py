import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def define_logger(name, level=logging.INFO, file_name='download.log'):
    logger = logging.Logger(name)
    logger.setLevel(level)
    try:
        log_path = Path(__file__).parent / 'script-logs' / 'download.log'
    except NameError:
        log_path = Path('script-logs') / file_name
    handler = RotatingFileHandler(log_path, maxBytes=1048576, backupCount=5)
    formatter = logging.Formatter('\n%(asctime)s - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
