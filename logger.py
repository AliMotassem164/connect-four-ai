# logger.py

import logging
import os  #to create file 

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/game.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(msg):
    logging.info(msg)

def log_error(msg):
    logging.error(msg)
