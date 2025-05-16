# 📝 AI Blog Assistant

**AI Blog Assistant** is a sleek, Streamlit-powered application that enables effortless blog generation using **Google's Gemini 2.0 Flash LLM**. Whether you're a content marketer, technical writer, or blogger, this tool helps you craft high-quality, keyword-rich blog posts in seconds — just input a title, a few keywords, and your desired word count.

Additionally, this project includes an **experimental LLaMA-powered blog writer** using Meta’s LLaMA 3.2, showcasing multi-model support and flexibility.

![Blog AI Assistant Screenshot](images/Streamlit_app.jpg)

---

## Features

* Gemini 2.0 Flash: fast, reliable blog generation with SEO keyword focus
* LLaMA 3.2 Model (Experimental): alternative blog generator with open LLMs
* Generates well-structured articles with headings and keyword integration
* Interactive Streamlit UI
* Download results in Markdown
* API key-based integration
* Modular and easy to extend

---

## Project Structure

```
ai-blog-assistant/
│
├── api_key.py               # Contains your Gemini API key
├── gemini_app.py                   # Main app using Gemini LLM
├── llama_app.py             # Alternative blog generator using Meta's LLaMA
├── requirements.txt         # Python dependencies
├── images/
│   └── Streamlit_app.jpg    # UI screenshot
└── README.md                # Project documentation
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/MoustafaMohamed01/ai-blog-assistant.git
cd ai-blog-assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit google-generativeai
```

> If using the LLaMA script (`llama_app.py`), make sure you also install:
>
> ```bash
> pip install streamlit requests json
> ```

### 3. Set Up API Key

For Gemini, create a file `api_key.py`:

```python
GEMINI_API_KEY = "your_google_gemini_api_key"
```

---

## Run the Apps

### Run Gemini-Powered Blog Assistant

```bash
streamlit run gemini_app.py
```

### Run LLaMA-Based Blog Generator

```bash
streamlit run llama_app.py
```

> Make sure your LLaMA model is downloaded and available locally or configured via `transformers`.

---

## Example Use Case

1. **Input Blog Title** — e.g., *"The Role of AI in Climate Solutions"*
2. **Add Keywords** — e.g., *"AI, climate change, sustainability"*
3. **Choose Word Count** — from 200 to 2500
4. **Click Generate Blog**
5. **Copy or Download** the generated Markdown post

---

## LLaMA Integration

The `llama_app.py` file showcases how Meta’s **LLaMA 3.2** can be used to generate blog-style content using open-source models via `transformers`.

You can modify the generation prompt, model size, or tokenizer to customize behavior. Great for offline and open-weight deployments!

---

## Requirements

* `streamlit`
* `google-generativeai`
* `requests`
* `json`

---

## Author

**Moustafa Mohamed**
[LinkedIn](https://www.linkedin.com/in/moustafamohamed01/) • [GitHub](https://github.com/MoustafaMohamed01) • [Kaggle](https://www.kaggle.com/moustafamohamed01)
