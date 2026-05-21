import os
import google.generativeai as genai

_API_KEY = "Your_API_KEY"

genai.configure(api_key=_API_KEY)

_GEMINI_MODEL = "gemini-2.5-flash"


_PROMPT_TEMPLATE = """\
Answer the question based only on the context below. \
If the answer is not in the context, say 'I don't know'.

Context:
{context}

Question: {question}"""


def generate_answer(question: str, retrieved_chunks: list[str]) -> str:
    """
    Build the RAG prompt and call Gemini to produce an answer.

    Args:
        question:         The user's original question.
        retrieved_chunks: Top-k text chunks from the retriever.

    Returns:
        The model's answer as a plain string.
    """
    context = "\n\n---\n\n".join(retrieved_chunks)

    prompt = _PROMPT_TEMPLATE.format(context=context, question=question)

    model = genai.GenerativeModel(_GEMINI_MODEL)
    response = model.generate_content(prompt)

    return response.text
