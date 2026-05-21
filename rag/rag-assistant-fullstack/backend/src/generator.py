import time
import logging
import google.generativeai as genai
from src.config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are a helpful AI assistant that answers questions based on provided document context.

Rules:
- Base answers on the retrieved context below.
- If context is insufficient, say so clearly — do not make things up.
- Maintain conversation continuity with recent history.
- Be concise, accurate, and helpful."""


def build_prompt(context_chunks, history_text, question):
    parts = []
    parts.append(SYSTEM_PROMPT)

    if context_chunks:
        parts.append("\n\n=== DOCUMENT CONTEXT ===")
        for i, r in enumerate(context_chunks, 1):
            source = r["chunk"].get("source", "unknown")
            parts.append(f"\n[{i}] Source: {source}\n{r['chunk']['text']}")

    if history_text:
        parts.append(f"\n\n=== RECENT CONVERSATION ===\n{history_text}")

    parts.append(f"\n\n=== QUESTION ===\n{question}")
    parts.append("\n\n=== ANSWER ===")
    return "".join(parts)


def generate_answer(context_chunks, history_text, question, temperature=0.3):
    prompt = build_prompt(context_chunks, history_text, question)
    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        generation_config=genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=1024,
        ),
    )
    start = time.time()
    try:
        response = model.generate_content(prompt)
        elapsed = time.time() - start
        if not response.candidates:
            return " Response was blocked. Please rephrase your question.", elapsed
        answer = response.text.strip()
        return answer if answer else " Empty response received.", elapsed
    except Exception as e:
        elapsed = time.time() - start
        err = str(e)
        if "quota" in err.lower() or "429" in err:
            return " API quota exceeded. Please wait and retry.", elapsed
        if "api_key" in err.lower() or "401" in err or "403" in err:
            return " Invalid API key. Check GEMINI_API_KEY in backend/src/config.py.", elapsed
        return f" Gemini error: {err}", elapsed
