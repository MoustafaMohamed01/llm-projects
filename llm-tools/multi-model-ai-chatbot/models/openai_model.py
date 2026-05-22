from typing import Generator, Any
from openai import OpenAI

OPENAI_API_KEY = "your_openai_api_key"


class OpenAIModel:

    MODEL_ID = "gpt-4o-mini"

    def __init__(self, temperature: float = 0.7, max_tokens: int = 2048):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def _build_messages(self, messages: list[dict], system_prompt: str) -> list[dict]:
        
        built = []
        if system_prompt:
            built.append({"role": "system", "content": system_prompt})
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
                stream_options={"include_usage": True},
            )

            usage = {}
            for chunk in stream:
                if chunk.usage:
                    usage = {
                        "prompt_tokens": chunk.usage.prompt_tokens,
                        "completion_tokens": chunk.usage.completion_tokens,
                        "total_tokens": chunk.usage.total_tokens,
                    }

                delta = chunk.choices[0].delta if chunk.choices else None
                if delta and delta.content:
                    yield delta.content

            yield {"usage": usage}

        except Exception as e:
            yield f"OpenAI error: {str(e)}"
            yield {"usage": {}}
