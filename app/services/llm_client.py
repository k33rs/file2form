import json
from groq import Groq
from openai import OpenAI
from os import getenv


class LLMClient:
    def __init__(self):
        provider = getenv('LLM_PROVIDER', '')
        if provider == 'openai':
            self.client = OpenAI()
        elif provider == 'groq':
            self.client = Groq()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def chat(self, model_params: dict) -> dict:
        response = self.client.chat.completions.create(**model_params)
        return json.loads(response.choices[0].message.content)
