import yaml
import json
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict


PROMPT_ROOT = Path("app/prompts")


@dataclass(frozen=True)
class Prompt:
    id: str
    version: str
    model: Dict[str, Any]
    system: str
    user: str
    response_format: Dict[str, Any]
    raw: Dict[str, Any]
    hash: str


class PromptManager:
    def load(self, prompt_id: str, version: str) -> Prompt:
        """
        Load a prompt by its ID and version.
        
        :param prompt_id: Identifier of the prompt.
        :type prompt_id: str
        :param version: Version of the prompt.
        :type version: str
        :return: Loaded Prompt object.
        :rtype: Prompt
        """
        path = PROMPT_ROOT / f"{prompt_id}_{version}.yml"
        if not path.exists():
            raise FileNotFoundError(f"Prompt not found: {path}")

        raw = yaml.safe_load(path.read_text())
        prompt_hash = hashlib.sha256(
            json.dumps(raw, sort_keys=True).encode()
        ).hexdigest()

        return Prompt(
            id=raw["id"],
            version=raw["version"],
            model=raw["model"],
            system=raw["system"],
            user=raw["user"],
            response_format=raw.get("response_format"),
            raw=raw,
            hash=prompt_hash,
        )
