import logging
import time

import google.generativeai as genai

logger = logging.getLogger(__name__)


MODEL_NAME = "gemini-2.5-flash"

GOOGLE_API_KEY = "your_gemini_api_key"


def configure_gemini():
    
    genai.configure(api_key=GOOGLE_API_KEY)
    logger.info("Gemini API configured successfully.")



SYSTEM_PROMPT = """You are a helpful AI assistant that answers questions based on the provided document context.

Guidelines:
- Base your answers primarily on the retrieved context below.
- If the context doesn't contain enough information, clearly say so — do NOT make things up.
- Maintain continuity with the recent conversation history when relevant.
- Be concise, accurate, and helpful.
- If asked about something outside the documents, politely explain that your knowledge is limited to the provided documents."""


def build_prompt(
    context_chunks: list[dict],
    conversation_history_text: str,
    question: str,
) -> str:
    
    context_parts = []
    for i, result in enumerate(context_chunks, start=1):
        chunk_text = result["chunk"]["text"]
        source = result["chunk"].get("source", "unknown")
        context_parts.append(f"[Chunk {i} | Source: {source}]\n{chunk_text}")

    context_block = "\n\n---\n\n".join(context_parts)

    prompt_parts = [
        SYSTEM_PROMPT,
        "\n\n=== RETRIEVED CONTEXT ===\n",
        context_block,
    ]

    if conversation_history_text:
        prompt_parts.append("\n\n=== RECENT CONVERSATION ===\n")
        prompt_parts.append(conversation_history_text)

    prompt_parts.append(f"\n\n=== CURRENT QUESTION ===\n{question}")
    prompt_parts.append("\n\n=== YOUR ANSWER ===")

    return "".join(prompt_parts)



def generate_answer(
    context_chunks: list[dict],
    conversation_history_text: str,
    question: str,
    temperature: float = 0.3,
) -> tuple[str, float]:
   
    prompt = build_prompt(context_chunks, conversation_history_text, question)

    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config=genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=1024,
        ),
    )

    start_time = time.time()

    try:
        response = model.generate_content(prompt)
        elapsed = time.time() - start_time

        if not response.candidates:
            return (
                "The response was blocked or empty. Please rephrase your question.",
                elapsed,
            )

        answer = response.text.strip()

        if not answer:
            return (
                "Received an empty response from Gemini. Please try again.",
                elapsed,
            )

        logger.info(f"Answer generated in {elapsed:.2f}s | {len(answer)} characters")
        return answer, elapsed

    except Exception as e:
        elapsed = time.time() - start_time
        error_str = str(e)

        if "quota" in error_str.lower() or "429" in error_str:
            msg = "API quota exceeded. Please wait a moment and try again."
        elif "api_key" in error_str.lower() or "401" in error_str or "403" in error_str:
            msg = "Invalid API key. Check the GOOGLE_API_KEY value in src/generator.py."
        elif "deadline" in error_str.lower() or "timeout" in error_str.lower():
            msg = "Request timed out. Please try again."
        else:
            msg = f"Gemini API error: {error_str}"

        logger.error(f"Gemini error: {error_str}")
        return msg, elapsed