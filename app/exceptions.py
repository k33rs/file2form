from fastapi import HTTPException
from app.errors import ErrorCode, ERROR_MESSAGES


class ExtractError(Exception):
    code: ErrorCode
    status_code: int

    def __str__(self):
        return ERROR_MESSAGES[self.code]

    def to_http(self):
        return HTTPException(
            status_code=self.status_code,
            detail={
                "code": self.code,
                "message": ERROR_MESSAGES[self.code],
            },
        )


class ReadError(ExtractError):
    code = ErrorCode.READ_ERROR
    status_code = 400


class ParseError(ExtractError):
    code = ErrorCode.PARSE_ERROR
    status_code = 500


class LLMError(ExtractError):
    code = ErrorCode.LLM_ERROR
    status_code = 500