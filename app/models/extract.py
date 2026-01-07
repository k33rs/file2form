from pydantic import BaseModel, Field


class WorkExperience(BaseModel):
    start_date: str = Field(..., description="Start date of the experience in YYYY-MM-DD format")
    end_date: str | None = Field(None, description="End date of the experience in YYYY-MM-DD format")


class LlmExtractionResult(BaseModel):
    name: str = Field(..., description="Full name of the candidate")
    role: str = Field(..., description="Current or desired role of the candidate")
    skills: list[str] = Field(..., description="List of skills possessed by the candidate")
    language: str = Field(..., description="Language of the CV")
    birth_date: str = Field(..., description="Birth date of the candidate in YYYY-MM-DD format")
    employment_dates: list[WorkExperience] = Field(
        ...,
        description="List of employment dates (start and end) found in the CV"
    )
    age: None = Field(None, description="Computed age of the candidate")
    experience_years: None = Field(None, description="Total years of experience computed from employment dates")
    seniority: None = Field(None, description="Seniority level based on years of experience")


class EnrichedLlmExtractionResult(LlmExtractionResult):
    age: int | None = Field(None, description="Computed age of the candidate")
    experience_years: float | None = Field(None, description="Total years of experience computed from employment dates")
    seniority: str | None = Field(None, description="Seniority level based on years of experience")


class ExtractHttpResponse(BaseModel):
    data: EnrichedLlmExtractionResult = Field(..., description="The enriched extraction result data")
    prompt_id: str = Field(..., description="Identifier of the prompt used")
    prompt_version: str = Field(..., description="Version of the prompt used")
    prompt_hash: str = Field(..., description="Hash of the prompt used")
    model: str = Field(..., description="Name of the LLM model used")