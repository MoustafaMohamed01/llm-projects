import streamlit as st
import os
import google.generativeai as genai
from api_key import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

professional_persona_instruction = """
You are an AI assistant designed to provide professional, and accurate information.
Your responses should be:
- **Formal and Respectful:** Maintain a polite and courteous tone at all times.
- **Objective and Factual:** Focus on verifiable information and avoid personal opinions or emotional language.
- **Grammatically Correct:** Ensure flawless grammar, spelling, and punctuation.
- **Solution-Oriented:** When appropriate, offer practical advice or solutions based on the query.
- **Avoid Ambiguity:** Provide definitive answers where possible. If uncertainty exists, state it clearly.
- **Maintain Confidentiality:** Do not ask for or provide sensitive personal information.
- **Neutral and Unbiased:** Present information without prejudice or favoritism.
"""

if 'chat_session' not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[
        {"role": "user", "parts": [professional_persona_instruction]},
        {"role": "model", "parts": ["Understood. I will adhere to these guidelines for all interactions. How may I assist you?"]}
    ])
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I am an AI assistant designed to provide professional, concise, and accurate information. How may I assist you today?"})


st.set_page_config(page_title='Professional AI Assistant', layout='centered')
st.title('AI Assistant')
st.markdown("""
    I'm here to provide you with professional and accurate information.
    Please feel free to ask your questions.
""")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask a professional question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Processing request..."):
        try:
            response_chunks = st.session_state.chat_session.send_message(user_input, stream=True)
            
            full_response = ""
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                for chunk in response_chunks:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌") 
                message_placeholder.markdown(full_response) 

            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"An error occurred: {e}. Please try again.")


def get_chat_history_as_text():
    history_text = ""
    for message in st.session_state.messages:
        role = "You" if message["role"] == "user" else "Assistant"
        history_text += f"{role}: {message['content']}\n\n"
    return history_text

if st.session_state.messages:
    st.download_button(
        label="Download Conversation",
        data=get_chat_history_as_text(),
        file_name="chatbot_conversation.txt",
        mime="text/plain",
        help="Click to download the current conversation history."
    )
