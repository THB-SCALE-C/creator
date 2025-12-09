import logging
from logging import Logger
from pathlib import Path

def setup_logger(name: str = "app") -> Logger:
    """
    Creates a logger that logs both to console and to an automatically created
    .logs/ folder. Log file will be named <name>.log.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False 

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        f"\n\n{100*"*"}\n"+
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))

    # Only add handlers if none have been added (avoid duplicate handlers)
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger