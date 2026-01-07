from fastapi import Request
from logging import getLogger
from app.services import PromptRunner


def get_redis(request: Request):
    """
    Retrieve the Redis client from the FastAPI application state.
    
    :param request: The FastAPI request object.
    :type request: Request
    :return: The Redis client instance.
    :rtype: RedisClient
    """
    return request.app.state.redis


def get_error_logger():
    """
    Retrieve the error logger.
    
    :return: The error logger instance.
    :rtype: Logger
    """
    return getLogger("uvicorn.error")


def get_access_logger():
    """
    Retrieve the access logger.
    
    :return: The access logger instance.
    :rtype: Logger
    """
    return getLogger("uvicorn.access")


def get_prompt_runner():
    """
    Retrieve a PromptRunner instance.
    
    :return: A new PromptRunner instance.
    :rtype: PromptRunner
    """
    return PromptRunner()