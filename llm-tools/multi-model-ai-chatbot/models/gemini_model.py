from typing import Generator, Any
import google.generativeai as genai

GEMINI_API_KEY = "your_gemini_api_key"


class GeminiModel:

    MODEL_ID = "gemini-2.5-flash"

    def __init__(self, temperature: float = 0.7, max_tokens: int = 2048):
        self.temperature = temperature
        self.max_tokens = max_tokens
        genai.configure(api_key=GEMINI_API_KEY)

    def _convert_messages(self, messages: list[dict]) -> list[dict]:
        
        history = []
        for msg in messages:
            role = msg["role"]
            if role == "system":
                continue 
            gemini_role = "model" if role == "assistant" else "user"
            history.append({"role": gemini_role, "parts": [msg["content"]]})
        return history

    def stream_chat(
        self, messages: list[dict], system_prompt: str = ""
    ) -> Generator[Any, None, None]:
       
        try:
            generation_config = genai.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
            )

            model_kwargs = {"generation_config": generation_config}
            if system_prompt:
                model_kwargs["system_instruction"] = system_prompt

            model = genai.GenerativeModel(self.MODEL_ID, **model_kwargs)

            history = self._convert_messages(messages[:-1]) if messages else []
            last_user_msg = messages[-1]["content"] if messages else ""

            chat = model.start_chat(history=history)

            response = chat.send_message(last_user_msg, stream=True)

            full_text = ""
            for chunk in response:
                if chunk.text:
                    full_text += chunk.text
                    yield chunk.text

            usage = {}
            try:
                usage = {
                    "prompt_tokens": response.usage_metadata.prompt_token_count,
                    "completion_tokens": response.usage_metadata.candidates_token_count,
                    "total_tokens": response.usage_metadata.total_token_count,
                }
            except Exception:
                pass

            yield {"usage": usage, "full_response": full_text}

        except Exception as e:
            yield f"Gemini error: {str(e)}"
            yield {"usage": {}, "full_response": ""}
