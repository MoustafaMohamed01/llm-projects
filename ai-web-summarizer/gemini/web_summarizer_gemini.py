import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
import google.generativeai as genai

load_dotenv(override=True)

def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("API key is missing. Please check your `.env` file and ensure it contains `GEMINI_API_KEY=your_api_key_here`.")
        return None
    if not api_key.startswith("AIzaSy"):
        print("Invalid API key. Gemini API keys usually start with 'AIzaSy'.")
        return None
    if api_key.strip() != api_key:
        print("Extra spaces detected around your API key. Please remove them.")
        return None
    print("Great! Your API key looks valid and ready to use.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash')

model = configure_gemini()

if model:
    response = model.generate_content("Hello Gemini, This is my first ever message to you.")
    print(response.text)

class Website:
    def __init__(self, url: str):
        self.url = url
        self.title = "No title found"
        self.text = ""
        self._scrape_website()

    def _scrape_website(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            self.title = soup.title.string if soup.title else self.title
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True) if soup.body else self.text
        except requests.RequestException as e:
            print(f"Failed to retrieve the website: {e}")
        except Exception as e:
            print(f"An error occurred while parsing the website: {e}")

SYSTEM_PROMPT = "You are an assistant that summarizes website content, focusing on key information while ignoring navigation elements. Respond in markdown format."

def generate_user_prompt(website):
    user_prompt = f"You are looking at this website titled: {website.title}\n\n"
    user_prompt += "The contents of this website are as follows. Please provide a short summary in markdown. "
    user_prompt += "If it includes news or announcements, summarize these too.\n\n"
    user_prompt += f"{website.text}"
    return user_prompt

def generate_messages(website):
    return [
        {"role": "system", "parts": [SYSTEM_PROMPT]},
        {"role": "user", "parts": [generate_user_prompt(website)]}
    ]

def summarize_website(url):
    if not model:
        return "Gemini API is not configured. Cannot summarize."
    website = Website(url)
    user_prompt = generate_user_prompt(website)
    response = model.generate_content(user_prompt)
    return response.text

def display_summary(url):
    summary = summarize_website(url)
    display(Markdown(summary))

display_summary("website url")
