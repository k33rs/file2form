from fastapi import (
    APIRouter, File, UploadFile, Depends,
)
from logging import Logger
from os import getenv
from typing import Annotated
from app.models import ExtractHttpResponse, ParsedData
from app.services import (
    RedisClient, read_and_hash, parse, PromptRunner,
)
from app.api.dependencies import (
    get_redis, get_access_logger, get_prompt_runner,
)
from app.exceptions import (
    ReadError, ParseError, LLMError,
)


router = APIRouter()


@router.post("/extract/")
async def extract(
    file: Annotated[UploadFile, File()],
    redis: RedisClient = Depends(get_redis),
    access_logger: Logger = Depends(get_access_logger),
    runner: PromptRunner = Depends(get_prompt_runner),
) -> ExtractHttpResponse:

    try: # 1. read and hash
        hash, raw = await read_and_hash(file)
    except Exception as e:
        read_error = ReadError()
        access_logger.error(f"{read_error}: {e}")
        raise read_error.to_http() from e
    else:
        access_logger.debug(f"File SHA256 <{hash}> computed.")

    try: # 2. cache lookup and parsing
        if redis.exists(hash):
            access_logger.debug(f"File SHA256 <{hash}> available: retrieving from Redis...")
            parsed = redis.get_dict(hash)
        else:
            access_logger.debug(f"File SHA256 <{hash}> not found in Redis: parsing raw text...")
            parsed = parse(raw)
            redis.set_dict(hash, parsed)

        ParsedData(**parsed)

    except Exception as e:
        parse_error = ParseError()
        access_logger.error(f"{parse_error}: {e}")
        raise parse_error.to_http() from e
    else:
        access_logger.debug(f"File SHA256 <{hash}> processed.")

    try: # 3. invoke LLM
        result = runner.run(
            prompt_id=getenv('PROMPT_ID', 'openai'),
            version=getenv('PROMPT_VERSION', 'v1'),
            variables=dict(
                content=parsed['content'],
                metadata=parsed['metadata'],
            ),
        )
    except Exception as e:
        llm_error = LLMError()
        access_logger.error(f"{llm_error}: {e}")
        raise llm_error.to_http() from e
    else: # 4. output JSON
        access_logger.debug(f"File SHA256 <{hash}> LLM processing completed.")
        return ExtractHttpResponse(**result)