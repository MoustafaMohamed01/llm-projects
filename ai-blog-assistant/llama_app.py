import streamlit as st
import requests
import json

OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"

st.set_page_config(layout="wide")
st.title('📝 Blog AI Assistant (Ollama)')
st.subheader('Now you can craft perfect blogs with the help of Llama AI via Ollama')

with st.sidebar:
    st.title('📋 Blog Configuration')
    st.subheader('Enter details of the blog you want to generate')

    blog_title = st.text_input('Blog Title')
    keywords = st.text_input('Keywords (comma-separated)')
    num_words = st.slider('Number of words', min_value=200, max_value=2500, step=250)

    prompt = f"""
    Generate a well-structured and engaging blog post with the title: "{blog_title}".
    Incorporate the following keywords naturally throughout the content: "{keywords}".
    The blog post should aim for a professional yet accessible tone, suitable for a broad audience interested in this topic.
    Organize the blog post with clear headings and subheadings where appropriate to enhance readability.
    The approximate word count should be {num_words} words.
    Please ensure the introduction is captivating, the body paragraphs are informative and well-supported, and the conclusion provides a concise summary or call to action (if relevant to the topic).
    """
    submit_button = st.button('Generate Blog')

if submit_button:
    with st.spinner('Generating blog post...'):
        try:
            payload = json.dumps({
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,  # Set to False for a single response
                "options": {
                    "num_predict": num_words, # Ollama parameter for max tokens
                    # Add other Ollama parameters as needed (e.g., temperature, top_p)
                }
            })

            response = requests.post(OLLAMA_API, headers=HEADERS, data=payload, stream=False)
            response.raise_for_status()
            response_json = response.json()
            generated_text = response_json['message']['content']

            st.subheader("Generated Blog Post:")
            st.markdown(generated_text)

            if generated_text:
                st.download_button(
                    label="Download as Markdown",
                    data=generated_text,
                    file_name=f"{blog_title.replace(' ', '_')}.md",
                    mime="text/markdown",
                )
        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with Ollama API: {e}")
        except (KeyError, json.JSONDecodeError) as e:
            st.error(f"Error processing Ollama API response: {e}")