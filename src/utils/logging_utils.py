import logging

def setup_logger(name: str) -> logging.Logger:
    """Setting up a logger with pre-defined and consistent formats."""
    logger = logging.getLogger(name=name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level=logging.INFO)
    
    return logger