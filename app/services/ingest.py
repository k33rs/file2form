import hashlib
from fastapi import UploadFile
from tika import parser
from langdetect import detect


async def read_and_hash(file: UploadFile) -> tuple[str, bytes]:
    """
    Read an UploadFile in chunks, compute its sha256 hash, and return both
    the hash and the raw bytes.
    
    :param file: Description
    :type file: UploadFile
    :return: sha256 hash and raw bytes
    :rtype: tuple[str, bytes]
    """
    hasher = hashlib.sha256()
    chunks = []

    while chunk := await file.read(8192):
        hasher.update(chunk)
        chunks.append(chunk)

    await file.seek(0)  # IMPORTANT: rewind for later use
    return hasher.hexdigest(), b"".join(chunks)


def parse(raw: bytes) -> dict:
    """
    Extract text and metadata from raw bytes using Tika.

    :param raw: Raw bytes from a file
    :type raw: bytes
    :return: Extracted text and metadata
    :rtype: dict
    """
    parsed = parser.from_buffer(raw)
    metadata = parsed.get("metadata", {})

    # extract language, enconding, content type
    content_type = metadata.get("Content-Type")
    encoding = metadata.get("Content-Encoding") or metadata.get("charset")
    lang = metadata.get("language", "unknown")
    if lang == "unknown" and parsed["content"].strip():
        lang = detect(parsed["content"])

    return {
        "content": parsed.get("content", ""),
        "metadata": {
            "content_type": content_type,
            "encoding": encoding,
            "language": lang,
        },
    }
