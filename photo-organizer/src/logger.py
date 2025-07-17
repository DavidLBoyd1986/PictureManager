import logging

def setup_logger(log_path):
    logger = logging.getLogger("PhotoOrganizer")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_path)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

def log_progress(logger, message):
    if logger:
        logger.info(message)
    print(message)