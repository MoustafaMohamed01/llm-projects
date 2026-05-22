def format_elapsed_time(seconds: float) -> str:
   
    if seconds < 60:
        return f"{seconds:.2f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"


def format_token_usage(usage: dict) -> str:
    
    if not usage:
        return ""

    prompt = usage.get("prompt_tokens", 0)
    completion = usage.get("completion_tokens", 0)
    total = usage.get("total_tokens", prompt + completion)

    if total == 0:
        return ""

    return f"↑{prompt:,} ↓{completion:,} tokens"


def truncate_text(text: str, max_length: int = 100) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "…"


def count_words(text: str) -> int:
    return len(text.split())


def sanitize_for_display(text: str) -> str:
    return text.strip() if text else ""


def get_model_short_name(full_name: str) -> str:
    for i, ch in enumerate(full_name):
        if ch.isalnum():
            return full_name[i:].strip()
    return full_name.strip()
