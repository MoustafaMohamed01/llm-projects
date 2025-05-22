import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display

OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"

class Website:
    url:str
    title:str
    text:str

    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)


system_prompt = "You are an assistant that summarizes website content, focusing on key information while ignoring navigation elements. Respond in markdown format."

def user_prompt_for(website):
    user_prompt = f"You are looking of this webssite titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
    Please provide a short summary of this website in markdown. \
    If it includes news or announcements, then summerize these too. \n\n"
    user_prompt += website.text
    return user_prompt

def messages_for(website):
    return [{"role": "user", "content": user_prompt_for(website)}]

def summarize(url):
    website = Website(url)
    messages = messages_for(website)
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }
    response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
    response_json = response.json()
    return response_json["message"]["content"]

def display_summary(url):
    summary = summarize(url)
    display(Markdown(summary))
    return summary

print(display_summary("https://moustafamohamed.netlify.app/"))