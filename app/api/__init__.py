from app.api.extract import router as extract_router
from app.api.health import router as health_router
from app.api.lifespan import lifespan
from app.api.middleware import log_context_middleware