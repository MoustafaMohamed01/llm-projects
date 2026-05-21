from dataclasses import dataclass, field
from typing import Literal


@dataclass
class Message:
    
    role: Literal["user", "assistant"]
    content: str


def add_message(history: list[Message], role: str, content: str) -> list[Message]:
    
    history.append(Message(role=role, content=content))
    return history


def get_recent_history(history: list[Message], max_exchanges: int = 4) -> list[Message]:
    
    max_messages = max_exchanges * 2
    return history[-max_messages:] if len(history) > max_messages else history[:]


def format_history_for_prompt(history: list[Message]) -> str:
    
    if not history:
        return ""

    lines = []
    for msg in history:
        role_label = "User" if msg.role == "user" else "Assistant"
        lines.append(f"{role_label}: {msg.content}")

    return "\n".join(lines)


def clear_history() -> list[Message]:
    return []
