# src/utils/logger.py
import logging
from src.config.settings import LOG_DIR

def get_logger():
    logger = logging.getLogger("financial_chatbot")
    logger.setLevel(logging.DEBUG)  # Capture all levels

    # Ensure log directory exists
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # File handler (rotate if needed)
    file_handler = logging.FileHandler(LOG_DIR / "app.log")
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Show INFO+ on console
    console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger