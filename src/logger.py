import logging
import os
from datetime import datetime

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True) # if it doesn't exist then create it

LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime("%Y-%m-%d")}.log") # log_2025-08-03.log

logging.basicConfig(
    filename=LOG_FILE,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s', # time - level - message
    level=logging.INFO, # only info and levels above info will be shown
)

def get_logger(name: str) -> logging.Logger:
    """Function to get a logger instance with a specific name."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger