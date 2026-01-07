from pydantic import ValidationError
from typing import Dict, Any
from app.models import LlmExtractionResult, EnrichedLlmExtractionResult
from app.services.llm_client import LLMClient
from app.services.prompt_manager import PromptManager
from app.services.post_process import post_process


class PromptRunner:
    def __init__(self):
        self.manager = PromptManager()
        self.llm_client = LLMClient()

    def run(
        self,
        prompt_id: str,
        version: str,
        variables: Dict[str, Any],
    ) -> Dict[str, Any]:

        prompt = self.manager.load(prompt_id, version)
        user_content = prompt.user.format(**variables)

        messages = [
            {"role": "system", "content": prompt.system},
            {"role": "user", "content": user_content},
        ]

        response = self.llm_client.chat(dict(
            model=prompt.model["name"],
            temperature=prompt.model["temperature"],
            max_completion_tokens=prompt.model["max_tokens"],
            messages=messages,
            response_format=prompt.response_format,
        ))

        try:
            LlmExtractionResult(**response)
        except ValidationError as e:
            raise ValueError(f"LLM response validation error:\n{e.errors()}") from e

        # post-process and enrich response
        enriched = post_process(response)

        try:
            EnrichedLlmExtractionResult(**enriched)
        except ValidationError as e:
            raise ValueError(f"Enriched LLM response validation error:\n{e.errors()}") from e

        return {
            "data": enriched,
            "prompt_id": prompt.id,
            "prompt_version": prompt.version,
            "prompt_hash": prompt.hash,
            "model": prompt.model["name"],
        }
