from typing import Generator, Any
from openai import OpenAI

DEEPSEEK_API_KEY = "your_deepseek_api_key"

# DeepSeek API base URL (OpenAI-compatible)
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"


class DeepSeekModel:
    
    MODEL_ID = "deepseek-chat"

    def __init__(self, temperature: float = 0.7, max_tokens: int = 2048):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
        )

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
            )

            usage = {}
            full_text = ""

            for chunk in stream:
                if hasattr(chunk, "usage") and chunk.usage:
                    usage = {
                        "prompt_tokens": chunk.usage.prompt_tokens,
                        "completion_tokens": chunk.usage.completion_tokens,
                        "total_tokens": chunk.usage.total_tokens,
                    }

                delta = chunk.choices[0].delta if chunk.choices else None
                if delta and delta.content:
                    full_text += delta.content
                    yield delta.content

            yield {"usage": usage, "full_response": full_text}

        except Exception as e:
            yield f"DeepSeek error: {str(e)}"
            yield {"usage": {}}
