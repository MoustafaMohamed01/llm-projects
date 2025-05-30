import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
import google.generativeai as genai

from api_key import GEMINI_API_KEY

def configure_gemini():
    """Configures the Gemini API and returns the GenerativeModel."""
    api_key = GEMINI_API_KEY 
    
    if not api_key:
        st.error("API key is missing. Please check your `api_key.py` file and ensure it contains `GEMINI_API_KEY='your_api_key_here'`.")
        return None
    if not api_key.startswith("AIzaSy"):
        st.error("Invalid API key. Gemini API keys usually start with 'AIzaSy'.")
        return None
    if api_key.strip() != api_key:
        st.error("Extra spaces detected around your API key. Please remove them.")
        return None
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash')

model = configure_gemini()

class Website:
    """Represents a website and handles scraping its content."""
    def __init__(self, url: str):
        self.url = url
        self.title = "No title found"
        self.text = ""
        self._scrape_website()

    def _scrape_website(self):
        """Scrapes the website content, extracting title and main text."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            self.title = soup.title.string if soup.title else self.title
            
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            
            self.text = soup.body.get_text(separator="\n", strip=True) if soup.body else self.text
        except requests.RequestException as e:
            st.error(f"Failed to retrieve the website: {e}")
            self.text = ""
        except Exception as e:
            st.error(f"An error occurred while parsing the website: {e}")
            self.text = ""

SYSTEM_PROMPT = "You are an assistant that summarizes website content, focusing on key information while ignoring navigation elements. Respond in markdown format."

def generate_user_prompt(website):
    """Generates the user prompt for the Gemini model."""
    if not website.text:
        return ""
    user_prompt = f"You are looking at this website titled: {website.title}\n\n"
    user_prompt += "The contents of this website are as follows. Please provide a short summary in markdown. "
    user_prompt += "If it includes news or announcements, summarize these too.\n\n"
    user_prompt += f"{website.text}"
    return user_prompt

def summarize_website(url):
    """Summarizes the content of a given URL using the Gemini model."""
    if not model:
        return "Gemini API is not configured. Cannot summarize.", None
    
    website = Website(url)
    if not website.text:
        return "Could not retrieve website content to summarize.", None

    user_prompt = generate_user_prompt(website)
    if not user_prompt:
        return "No content to summarize.", None
        
    try:
        with st.spinner("Generating summary..."):
            response = model.generate_content(user_prompt)
        return response.text, website.title
    except Exception as e:
        st.error(f"An error occurred while generating the summary: {e}")
        return "Failed to generate summary.", None

st.set_page_config(page_title="Website Summarizer")

st.title("Website Summarizer with Gemini")
st.markdown("""Enter a website URL below, and I'll provide a concise summary of its content...""")

url = st.text_input("Enter website URL", placeholder="e.g., https://www.example.com")

if 'summary_text' not in st.session_state:
    st.session_state.summary_text = None
if 'website_title' not in st.session_state:
    st.session_state.website_title = None

if st.button("Summarize"):
    if url:
        if not (url.startswith("http://") or url.startswith("https://")):
            st.warning("Please enter a valid URL starting with 'http://' or 'https://'.")
            st.session_state.summary_text = None
            st.session_state.website_title = None
        else:
            summary, title = summarize_website(url)
            st.session_state.summary_text = summary
            st.session_state.website_title = title if title else "summary"
    else:
        st.warning("Please enter a URL to summarize.")
        st.session_state.summary_text = None
        st.session_state.website_title = None

if st.session_state.summary_text:
    st.subheader("Summary:")
    st.markdown(st.session_state.summary_text)

    download_filename = "".join(c for c in st.session_state.website_title if c.isalnum() or c in (' ', '.', '_')).rstrip()
    download_filename = download_filename.replace(' ', '_').lower()
    if not download_filename:
        download_filename = "website_summary"
    download_filename += ".md"

    st.download_button(
        label="Download Summary as Markdown",
        data=st.session_state.summary_text,
        file_name=download_filename,
        mime="text/markdown"
    )
