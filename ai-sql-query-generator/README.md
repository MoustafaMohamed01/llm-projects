# 🧠 AI SQL Query Generator

This project is a lightweight **AI-powered SQL Query Generator** built with **Streamlit**, supporting both **Google Gemini (via Generative AI API)** and **LLaMA 3.2 (via Ollama)**. Just describe your query in plain English, and the model will generate a SQL query, sample output, and a concise explanation.

<p align="center">
  <img src="images/streamlit_app.jpg" alt="App Screenshot" width="70%">
</p>

---

## Features

- **Natural Language to SQL**: Describe what you want in plain text.
- **Context-Aware Queries**: Optionally include your database schema or table names.
- **Multi-Model Support**: Choose between Gemini API or locally hosted LLaMA 3.2 via Ollama.
- **Sample Output**: Returns an example response from the SQL query.
- **Explanation**: Understand what the generated SQL query does.
- **Dialect Options**: Choose from Generic SQL, PostgreSQL, MySQL, or SQLite.

---

## Directory Structure

```

ai-sql-query-generator/
│
├── api\_key.py              # API key configuration for Gemini
├── gemini\_app.py           # Streamlit app using Google Gemini
├── llama\_app.py            # Streamlit app using LLaMA 3.2 via Ollama
├── requirements.txt        # Python dependencies
└── images/
└── streamlit\_app.jpg   # UI screenshot

````

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/MoustafaMohamed01/llm-projects.git
cd llm-projects/ai-sql-query-generator
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```
**or:**
```bash
pip install streamlit google-generativeai json requests
```

---

## Running the App

### A) Using **Google Gemini API**

1. Add your Gemini API key in `api_key.py`:

```python
GEMINI_API_KEY = "your-api-key-here"
```

2. Run the Streamlit app:

```bash
streamlit run gemini_app.py
```

---

### B) Using **LLaMA 3.2 via Ollama**

1. Make sure Ollama is installed and running locally:

```bash
ollama run llama3:instruct
```

2. Then run the app:

```bash
streamlit run llama_app.py
```

---

## Example Use Case

> **Description**: "Find the top 5 customers with the highest total purchase amount."
>
> **Optional context**: `customers(id, name), orders(id, customer_id, amount)`
>
> **Dialect**: PostgreSQL

The model will return:

* A **SQL query**
* A **sample result table**
* An **explanation**

---

## Tech Stack

* Python
* Streamlit
* Google Generative AI API (Gemini)
* LLaMA 3.2 via Ollama
* SQL (PostgreSQL, MySQL, SQLite, Generic)

---

## Author

**Moustafa Mohamed**
Aspiring AI Developer | [LinkedIn](https://www.linkedin.com/in/moustafamohamed01/) • [GitHub](https://github.com/MoustafaMohamed01) • [Kaggle](https://www.kaggle.com/moustafamohamed01)

---

## Show Your Support

If you find this project helpful, consider giving it a star ⭐ on GitHub to support the development of more open-source AI tools!
