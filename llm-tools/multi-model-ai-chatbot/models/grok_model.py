from typing import Generator, Any
from openai import OpenAI

GROK_API_KEY = "your_grok_api_key"

GROK_BASE_URL = "https://api.x.ai/v1"


class GrokModel:

    MODEL_ID = "grok-beta"

    def __init__(self, temperature: float = 0.7, max_tokens: int = 2048):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = OpenAI(
            api_key=GROK_API_KEY,
            base_url=GROK_BASE_URL,
        )

    def _build_messages(self, messages: list[dict], system_prompt: str) -> list[dict]:
        
        built = []
        if system_prompt:
            built.append({"role": "system", "content": system_prompt})
        else:
            built.append({
                "role": "system",
                "content": (
                    "You are Grok, a witty and knowledgeable AI assistant built by xAI. "
                    "You have a touch of humor and directness. "
                    "Be helpful, accurate, and occasionally entertaining."
                ),
            })
        for msg in messages:
            if msg["role"] != "system":
                built.append({"role": msg["role"], "content": msg["content"]})
        return built

    def stream_chat(
        self, messages: list[dict], system_prompt: str = ""
    ) -> Generator[Any, None, None]:
        
        try:
            built_messages = self._build_messages(messages, system_prompt)

            stream = self.client.chat.completions.create(
                model=self.MODEL_ID,
                messages=built_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True,
            )

            for chunk in stream:
                delta = chunk.choices[0].delta if chunk.choices else None
                if delta and delta.content:
                    yield delta.content

            yield {"usage": {}}

        except Exception as e:
            yield f"Grok error: {str(e)}"
            yield {"usage": {}}
