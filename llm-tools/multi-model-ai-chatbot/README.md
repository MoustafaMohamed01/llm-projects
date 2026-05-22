# MultiMind AI

MultiMind AI is a production-style multi-model chatbot built with Python and Streamlit.  
It provides a unified interface for interacting with multiple AI providers, including Google Gemini, OpenAI, xAI Grok, and DeepSeek.

## Features

- Multi-model AI support
  - Gemini 2.5 Flash
  - GPT-4o Mini
  - Grok
  - DeepSeek Chat

- Real-time streaming responses
- Persistent multi-turn chat memory
- Model switching during conversations
- Adjustable temperature and max tokens
- Custom system prompts
- Markdown and code rendering
- Token usage and response timing
- Modern dark-themed interface
- Modular and extensible architecture
- Error handling and retry support

---

## Project Structure

```bash
multi-ai-chatbot/
│
├── app.py
├── requirements.txt
├── README.md
│
├── models/
│   ├── gemini_model.py
│   ├── openai_model.py
│   ├── grok_model.py
│   └── deepseek_model.py
│
└── utils/
    ├── ui.py
    ├── chat_memory.py
    └── helpers.py


````

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MoustafaMohamed01/llm-projects.git
cd llm-projects/llm-tools/multi-model-ai-chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## API Keys

Add your API keys directly inside the model files.

Example:

```python
OPENAI_API_KEY = "your_openai_key"
GEMINI_API_KEY = "your_gemini_key"
GROK_API_KEY = "your_grok_key"
DEEPSEEK_API_KEY = "your_deepseek_key"
```

### API Providers

| Provider      | API Key Platform                                               |
| ------------- | -------------------------------------------------------------- |
| Google Gemini | [https://aistudio.google.com](https://aistudio.google.com)     |
| OpenAI        | [https://platform.openai.com](https://platform.openai.com)     |
| xAI Grok      | [https://console.x.ai](https://console.x.ai)                   |
| DeepSeek      | [https://platform.deepseek.com](https://platform.deepseek.com) |

---

## Running the Application

```bash
streamlit run app.py
```

---

### Session Management

The application uses `st.session_state` to preserve:

* Conversation history
* System prompts
* Selected model
* Generation settings
* UI state across reruns

---

## Adding a New Model

1. Create a new file inside `models/`
2. Implement a streaming chat class
3. Register the model in `app.py`
4. Add the provider SDK to `requirements.txt`

