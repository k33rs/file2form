from fastapi import FastAPI
from app.api import (
    lifespan, log_context_middleware, health_router, extract_router,
)


app = FastAPI(title="File2Form API", lifespan=lifespan)
app.middleware("http")(log_context_middleware)
app.include_router(health_router)
app.include_router(extract_router)
