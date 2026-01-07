from pydantic import BaseModel, Field


class Metadata(BaseModel):
    content_type: str = Field(..., description="Content type of the parsed file")
    encoding: str | None = Field(None, description="Encoding of the parsed file")
    language: str = Field(..., description="Language of the parsed file")


class ParsedData(BaseModel):
    content: str = Field(..., description="Extracted text content from the file")
    metadata: Metadata = Field(..., description="Metadata associated with the parsed file")