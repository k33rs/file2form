from enum import Enum


class ErrorCode(str, Enum):
    READ_ERROR = "read_error"
    PARSE_ERROR = "parse_error"
    LLM_ERROR = "llm_error"


ERROR_MESSAGES = {
    ErrorCode.READ_ERROR: "Error reading-hashing file",
    ErrorCode.PARSE_ERROR: "Error parsing-caching text",
    ErrorCode.LLM_ERROR: "Error LLM processing",
}
