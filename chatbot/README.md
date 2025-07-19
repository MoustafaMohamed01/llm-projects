# Gemini AI Chatbot 🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)

A professional AI chatbot interface powered by Google's Gemini API, featuring:
- Real-time conversational AI
- Session management
- Responsive web interface
- File upload capability
- Markdown rendering

![Chatbot Screenshot](/static/screenshot.png)

## Features

- **Natural Conversations**: Powered by Google's Gemini Pro model
- **Persistent Sessions**: Maintains conversation context
- **Modern UI**: Clean, responsive interface with dark/light modes
- **File Processing**: Upload and analyze documents
- **Secure**: API key protection and input sanitization

## Tech Stack

| Component       | Technology |
|----------------|------------|
| Backend        | FastAPI (Python) |
| Frontend       | HTML5, CSS3, JavaScript |
| AI Engine      | Google Gemini API |
| Markdown       | Marked.js |

## Installation

### Prerequisites
- Python 3.9+
- Google Gemini API key
- Node.js (for optional frontend builds)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/MoustafaMohamed01/llm-projects.git
   cd llm-projects/chatbot
   ```

2. Set up environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```
   ```bash
   pip install -r requirements.txt
   ```

3. Configure `.env`:
   ```ini
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

1. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

2. Access the chatbot:
   ```
   http://localhost:8000
   ```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Process chat messages |
| `/api/upload` | POST | Handle file uploads |
| `/api/health` | GET | Service health check |

---

## Contact

**Moustafa Mohamed**
[LinkedIn](https://www.linkedin.com/in/moustafamohamed01/) • [GitHub](https://github.com/MoustafaMohamed01) • [Kaggle](https://www.kaggle.com/moustafamohamed01) • [Portfolio](https://moustafamohamed.netlify.app/)

