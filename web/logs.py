import logging

logger = logging.getLogger("debug")
logger.setLevel(logging.DEBUG)
log_handler = logging.FileHandler('debug.log')
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_format)
logger.addHandler(log_handler)