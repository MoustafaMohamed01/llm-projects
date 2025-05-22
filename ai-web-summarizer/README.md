# Website Summarizer

This project provides an AI-powered website summarization tool that extracts and summarizes website content using two different AI models: **Google Gemini API** and **LLaMA 3.2**. It scrapes the text from a given URL, removes irrelevant elements, and generates a concise summary in markdown format.

---

## Features

- **Web Scraping**: Extracts the title and main text content from a website.
- **Content Cleaning**: Removes unnecessary HTML elements (e.g., scripts, styles, images) to keep only the relevant content.
- **AI Summarization**:
  - Uses the **Gemini API** to generate summaries in `web_summarizer_ai.py` and `web_summarizer_ai.ipynb`.
  - Uses **LLaMA 3.2** (via Ollama API) to generate summaries in `web_summarizer_llama.py` and `web_summarizer_llama.ipynb`.
- **IPython Support**: Displays the summary in markdown format for easy readability in Jupyter notebooks or IPython environments.

---

## Setup

### Prerequisites

- Python 3.7 or higher.
- Either a **Gemini API key** (for Google AI) or **LLaMA 3.2 API** (for local inference via Ollama).

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MoustafaMohamed01/web-summarizer-ai.git
   cd web-summarizer-ai
   ```

2. Install the required dependencies:
   ```bash
   pip install requests beautifulsoup4 python-dotenv google-generativeai IPython
   ```

3. Set up your environment variables:
   - Create a `.env` file in the project root directory:
     
     ```bash
     cp .env.example .env
     ```
   - Open the `.env` file and add your Gemini API key:
     
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

For LLaMA 3.2 support, ensure you have **Ollama** installed and running locally:
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
```

---

## Usage

### 1. Summarizing Websites with Gemini API

Run the Python script:
```bash
python web_summarizer_ai.py
```

Or use the interactive Jupyter Notebook:
```bash
jupyter notebook web_summarizer_ai.ipynb
```

### 2. Summarizing Websites with LLaMA 3.2 (Ollama)

Run the LLaMA-based summarizer script:
```bash
python web_summarizer_llama.py
```

Or open and run the Jupyter Notebook:
```bash
jupyter notebook web_summarizer_llama.ipynb
```

---

## File Structure

- `web_summarizer_ai.py`: Python script that scrapes a website and generates a summary using the **Gemini API**.
- `web_summarizer_ai.ipynb`: Jupyter Notebook version for interactive summarization using **Gemini API**.
- `web_summarizer_llama.py`: Python script that scrapes a website and generates a summary using **LLaMA 3.2**.
- `web_summarizer_llama.ipynb`: Jupyter Notebook version for interactive summarization using **LLaMA 3.2**.
- `.env.example`: Template file for storing API keys.

---

## Dependencies

The project relies on the following Python packages:
- `requests`: For making HTTP requests to fetch website content.
- `beautifulsoup4`: For parsing HTML and extracting relevant content.
- `python-dotenv`: For loading API keys from a `.env` file.
- `google-generativeai`: For interacting with the **Gemini API**.
- `IPython`: For displaying markdown summaries in Jupyter notebooks.
- `Ollama`: For running **LLaMA 3.2** locally (required only for `web_summarizer_llama.py` and `web_summarizer_llama.ipynb`).

---

## Contributing

Contributions are welcome! If you’d like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Submit a pull request.

---

## Acknowledgments

- [Google AI Studio](https://makersuite.google.com/)
- [LLM Engineering: Master AI, Large Language Models & Agents](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models/?couponCode=KEEPLEARNING)
- [Ollama](https://ollama.com/)

