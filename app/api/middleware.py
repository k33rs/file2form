import uuid
from fastapi import Request
from app.logging import request_id_ctx, path_ctx, method_ctx


async def log_context_middleware(request: Request, call_next):
    """
    Middleware to set logging context variables for each request.
    
    :param request: The FastAPI request object.
    :type request: Request
    :param call_next: The next middleware or route handler to call.
    :return: The HTTP response with logging context set.
    :rtype: Response
    """
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))

    token_id = request_id_ctx.set(request_id)
    token_path = path_ctx.set(request.url.path)
    token_method = method_ctx.set(request.method)

    try:
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        return response
    finally:
        request_id_ctx.reset(token_id)
        path_ctx.reset(token_path)
        method_ctx.reset(token_method)