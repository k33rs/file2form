import logging
from os import getenv
from app.logging.filters import RequestContextFilter


def setup_logging():
    """
    Set up logging configuration with context filters and log levels.
    """
    filter_ = RequestContextFilter()

    log_level = getenv('LOG_LEVEL', 'info').upper()
    log_level_int = getattr(logging, log_level, logging.INFO)

    logger = logging.getLogger("uvicorn.error")
    logger.setLevel(log_level_int)
    logger.info(f"uvicorn.error: log level set to {log_level}")

    log_level_access = getenv('LOG_LEVEL_ACCESS', log_level).upper()
    log_level_int_access = getattr(logging, log_level_access, logging.INFO)

    access_logger = logging.getLogger("uvicorn.access")
    access_logger.setLevel(log_level_int_access)
    access_logger.addFilter(filter_)
    access_logger.info(f"uvicorn.access: log level set to {log_level_access}")