from contextvars import ContextVar


request_id_ctx = ContextVar("request_id", default=None)
path_ctx = ContextVar("path", default=None)
method_ctx = ContextVar("method", default=None)