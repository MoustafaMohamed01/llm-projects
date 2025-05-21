# AI CSV Assistant – No Embeddings

This project provides a **lightweight AI-powered data assistant** built with **Streamlit** that lets you upload CSV files and ask natural language questions about your data. It supports **Google Gemini** and **LLaMA 3.2 via Ollama**, making it easy to analyze datasets locally or through the cloud without requiring embeddings or vector databases.

---

## Project Structure

```
ai-data-analyzer/
├── api_key.py             # Contains your Gemini API key (keep it secret!)
├── gemini_app.py          # Streamlit app using Google Gemini 2.0 Flash
├── llama_app.py           # Streamlit app using local Ollama LLaMA 3.2
├── requirements.txt       # Python dependencies
└── README.md
```

---

## ⚙️ Features

* Upload and preview CSV datasets
* Ask questions about your data using:

  * **Google Gemini 2.0 Flash**
  * **LLaMA 3.2 (via Ollama)**
* Remembers your question and answer history per session
* No embeddings or vector DBs required
* Simple, fast, and extensible

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/MoustafaMohamed01/llm-projects.git
cd llm-projects/ai-data-analyzer
```

### 2. Install dependencies

We recommend using a virtual environment.

```bash
pip install -r requirements.txt
```
**or:**
```bash
pip install pandas google-generativeai streamlit requests json
```

### 3. Choose a backend

#### Option A: Run with Gemini (Cloud)

1. Set your Gemini API key inside `api_key.py`:

   ```python
   GEMINI_API_KEY = "your-google-api-key"
   ```

2. Run the app:

   ```bash
   streamlit run gemini_app.py
   ```

#### Option B: Run with LLaMA (Local via Ollama)

1. Ensure [Ollama](https://ollama.com/) is installed and running:

   ```bash
   ollama run llama3
   ```

2. Run the app:

   ```bash
   streamlit run llama_app.py
   ```

---

## How It Works

* Parses uploaded CSV into a Pandas DataFrame
* Converts sample data and column names into a natural language prompt
* Sends prompt to the selected LLM (Gemini or LLaMA)
* Displays the model's answer with session-based chat history

---

## Example Use Cases

* "What is the average salary in this dataset?"
* "How many unique departments are listed?"
* "Which product has the highest sales?"
* "Are there any missing values?"

---

## Requirements

* Python 3.8+
* [Streamlit](https://streamlit.io/)
* [Google Generative AI Python SDK](https://pypi.org/project/google-generativeai/)
* [Ollama (for local LLaMA models)](https://ollama.com/)

---

## Contributing

Feel free to open issues or pull requests. Suggestions and improvements are welcome!
