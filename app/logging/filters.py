import logging
from .context import (
    request_id_ctx, path_ctx, method_ctx,
)


class RequestContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Inject request context (request ID, path, method) into log records.

        Args:
            record (logging.LogRecord): The log record to modify.
        Returns:
            bool: Always returns True to indicate the record should be logged.
        """
        record.request_id = request_id_ctx.get()
        record.path = path_ctx.get()
        record.method = method_ctx.get()
        return True