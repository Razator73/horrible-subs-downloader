import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def define_logger(name, level=logging.INFO, file_name='download.log', handler='file'):
    logger = logging.Logger(name)
    logger.setLevel(level)
    try:
        log_path = Path(__file__).parent / 'script-logs' / file_name
    except NameError:
        log_path = Path('script-logs') / file_name
    if handler == 'file':
        handler = RotatingFileHandler(log_path, maxBytes=1048576, backupCount=5)
    else:
        handler = logging.StreamHandler()
    formatter = logging.Formatter('\n%(asctime)s - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
