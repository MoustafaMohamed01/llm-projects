# LLM Projects Collection

Welcome to the **LLM Projects** repository — a growing collection of hands-on applications powered by **Large Language Models (LLMs)** like **Google Gemini 2.0 Flash** and **Meta's LLaMA 3.2**. This repo showcases real-world use cases built with **Streamlit**, focused on automating content creation and enhancing productivity with AI.

Whether you're a student, developer, or AI enthusiast, these projects demonstrate how to integrate cutting-edge LLMs into useful tools like blog generators, SQL query builders, and data analysis assistants.

---

## Projects Included

### 1. [AI Blog Assistant](./ai-blog-assistant)

Generate SEO-friendly blog posts with just a title and keywords. Built using **Gemini 2.0 Flash** and optionally powered by **LLaMA 3.2** for experimentation with open-source models.

**Features:**

* Input-based article generation
* Multi-model support (Gemini & LLaMA)
* SEO keyword handling
* Markdown export
* Beautiful, responsive UI

[View README](./ai-blog-assistant/README.md)

---

### 2. [AI SQL Query Generator](./ai-sql-query-generator)

Turn plain English into fully-formed SQL queries! This tool supports schema context, dialect customization, and offers AI-generated explanations and sample outputs.

**Features:**

* Converts natural language to SQL queries
* Supports Gemini 2.0 and LLaMA 3.2
* Accepts optional DB schema and dialect
* Returns SQL, explanation, and sample output
* Clean Streamlit interface

[View README](./ai-sql-query-generator/README.md)

---

### 3. [AI CSV Assistant](./ai-data-analyzer)

Upload a CSV file and interact with your dataset through natural language questions using either **Google Gemini** or **LLaMA 3.2** via **Ollama**. No embeddings or external databases required.

**Features:**

* Upload and preview CSV files
* Ask questions about your data
* Gemini or local LLaMA backend support
* No vector store needed
* Session-based Q&A memory

[View README](./ai-data-analyzer/README.md)

---

### 4. [Website Summarizer](./ai-web-summarizer)

Extract and summarize website content using **Google Gemini API** or **LLaMA 3.2** (via Ollama). Scrapes raw text, removes unnecessary elements, and outputs clean markdown summaries.

**Features:**

* Extracts title and main text from a URL
* Removes scripts, styles, and irrelevant tags
* Summarizes using Gemini or LLaMA 3.2
* Works with Jupyter or standalone scripts
* No need for embeddings or RAG setup

[View README](./ai-web-summarizer/README.md)

---

### 5. [AI Document Summarizer](./ai-document-summarizer)

Summarize content from uploaded **PDF** and **Word** documents in seconds using **Google Gemini 1.5 Flash** and **LangChain**. The app creates a vector-based knowledge base and queries the content for an intelligent summary.

**Features:**

* Upload `.pdf` or `.docx` files
* Automatically extracts and cleans text
* Uses FAISS and LangChain for context-aware summarization
* Gemini 1.5 Flash as the LLM backend
* Clean and responsive Streamlit interface

[View README](./ai-document-summarizer/README.md)

---

### 6. [AI Assistant Pro](./ai-assistant-pro)

A professional chatbot interface built with **Gemini 2.0 Flash**, designed for business, academic, and formal communication. It features context-aware chat, markdown formatting, and exportable transcripts.

**Features:**

* Powered by Gemini 2.0 Flash
* Formal, accurate, and solution-focused replies
* Persistent session memory
* Chat export to `.txt` format
* Sleek UI with Streamlit

[View README](./ai-assistant-pro/README.md)

---

## [LLM Tools Suite](https://github.com/MoustafaMohamed01/llm-tools-suite)

An integrated collection of AI-powered tools designed to enhance productivity and streamline various tasks using advanced Large Language Models. This suite offers a unified interface to access powerful features for content generation, data analysis, query creation, and document summarization.

**Features:**

- 🏠 Overview: A welcoming home screen providing an introduction and quick overview of all available tools.  
- 📝 Blog AI Assistant: Generate high-quality blog content using AI based on title, keywords, and desired word count.  
- 📊 AI CSV Analyzer: Upload your CSV files and analyze them intelligently using LLM-powered queries.  
- 💻 SQL Query Generator: Transform plain English into SQL queries with the help of AI.  
- 📄 Document Summarizer: Upload a PDF or Word document and get a concise summary in seconds.

[View README](./llm-tools-suite/README.md)

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/MoustafaMohamed01/llm-projects.git
cd llm-projects
````

### 2. Navigate to Any Subproject

For example, to use the AI SQL Generator:

```bash
cd ai-sql-query-generator
pip install -r requirements.txt
```

### 3. Set Your API Key (for Gemini-powered apps)

Create a file named `api_key.py` inside the subproject folder:

```python
GEMINI_API_KEY = "your_google_gemini_api_key"
```

---

## Requirements

Each app has its own `requirements.txt`, but common dependencies include:

* `streamlit`
* `google-generativeai`
* `pandas`
* `requests`
* `json`

Install them globally or per-project as needed.

---

## Gallery

<table>
  <tr>
    <td><img src="ai-blog-assistant/images/Streamlit_app.jpg" alt="Blog Assistant UI" width="400"/></td>
    <td><img src="ai-sql-query-generator/images/streamlit_app.jpg" alt="SQL Generator UI" width="400"/></td>
  </tr>
  <tr>
    <td><img src="ai-data-analyzer/images/streamlit_app.jpg" alt="CSV Assistant UI" width="400"/></td>
    <td><img src="ai-document-summarizer/images/streamlit_app.jpg" alt="Document Summarizer UI" width="400"/></td>
  </tr>
  <tr>
    <td><img src="ai-web-summarizer/images/streamlit_app.png" alt="Web Summarizer UI" width="400"/></td>
    <td><img src="llm-tools-suite/images/overview.png" alt="LLM Tools Suite Overview" width="400"/></td>
  </tr>
  <tr>
    <td><img src="ai-assistant-pro/images/screenshot.jpg" alt="AI Assistant Pro UI" width="400"/></td>
  </tr>
</table>

---

## Author

Created by **Moustafa Mohamed** - feel free to reach out!

* **GitHub**: [MoustafaMohamed01](https://github.com/MoustafaMohamed01)
* **Linkedin**: [Moustafa Mohamed](https://www.linkedin.com/in/moustafamohamed01/)
* **Kaggle**: [moustafamohamed01](https://www.kaggle.com/moustafamohamed01)
* **Portfolio**: [moustafamohamed](https://moustafamohamed.netlify.app/)

---
