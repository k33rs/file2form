from contextlib import asynccontextmanager
from fastapi import FastAPI
from os import getenv
from app.logging import setup_logging
from app.services import RedisClient
from app.api.dependencies import get_error_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    setup_logging()
    app.state.redis = RedisClient(
        host=(redis_host := getenv('REDIS_HOST', 'localhost')),
        port=(redis_port := int(getenv('REDIS_PORT', '6379'))),
        db=0,
        decode_responses=True,
    )
    get_error_logger().info(f"Connected to Redis at {redis_host}:{redis_port}")
    yield
    # Shutdown actions
    app.state.redis.close()
    get_error_logger().info("Redis connection closed")