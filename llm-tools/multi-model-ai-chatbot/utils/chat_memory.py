import streamlit as st
from datetime import datetime


def init_session_state() -> None:
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if "system_prompt" not in st.session_state:
        st.session_state["system_prompt"] = ""

    if "chat_start_time" not in st.session_state:
        st.session_state["chat_start_time"] = datetime.now()

    if "total_messages" not in st.session_state:
        st.session_state["total_messages"] = 0


def add_message(
    role: str,
    content: str,
    metadata: dict | None = None,
) -> None:
    
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata or {},
    }
    st.session_state["messages"].append(message)
    st.session_state["total_messages"] += 1


def get_messages() -> list[dict]:
    return st.session_state.get("messages", [])


def get_last_n_messages(n: int = 20) -> list[dict]:
    messages = get_messages()
    return messages[-n:] if len(messages) > n else messages


def clear_chat() -> None:
    st.session_state["messages"] = []
    st.session_state["total_messages"] = 0
    st.session_state["chat_start_time"] = datetime.now()


def get_system_prompt() -> str:
    return st.session_state.get("system_prompt", "")


def get_message_count() -> int:
    return st.session_state.get("total_messages", 0)
