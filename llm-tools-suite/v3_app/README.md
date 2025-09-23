# LLM Tools Suite – Flutter App (v3)

A **cross-platform mobile app** version of the LLM Tools Suite, built with **Flutter** and powered by the **Google Gemini API**. This app provides a modern, mobile-first experience for interacting with AI-powered productivity tools.

---

## Features

* 🧠 **AI Assistant** – Chat with an AI assistant in real time.
* 📝 **Blog AI Assistant** – Generate blog posts from a title, keywords, and word count.
* 📊 **CSV Analyzer** – Upload and analyze CSV files (in progress).
* 💻 **SQL Query Generator** – Convert natural language into SQL queries.
* 🔍 **Code Explainer** – Understand code snippets with AI explanations.
* 📄 **Document Summarizer** – (Coming soon).
* 🌐 **Website Summarizer** – (Coming soon).

---

## Project Structure

```
lib/
├── main.dart                   # App entry point
├── theme/
│   └── app_theme.dart          # Dark theme configuration
├── models/
│   └── tool_model.dart         # Data models
├── services/
│   ├── chat_service.dart       # Local storage with SharedPreferences
│   ├── document_processor.dart
│   └── gemini_service.dart     # Gemini API integration
├── widgets/
│   ├── sidebar_widget.dart     # Navigation sidebar
│   ├── tool_content_widget.dart# Tool router
│   └── loading_animation.dart  # Custom loading animation
└── screens/
    ├── home_screen.dart        # Main layout
    ├── ai_assistant_screen.dart
    ├── blog_assistant_screen.dart
    ├── csv_analyzer_screen.dart
    ├── sql_generator_screen.dart
    ├── code_explainer_screen.dart
    ├── document_summarizer_screen.dart  # Placeholder
    └── website_summarizer_screen.dart   # Placeholder

pubspec.yaml
```

---

## Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/MoustafaMohamed01/llm-projects.git
   cd llm-projects/llm-tools-suite/v3_app
   ```

2. **Install dependencies**

   ```bash
   flutter pub get
   ```

3. **Set your API key**

   * Open `services/gemini_service.dart`
   * Replace the placeholder with your **Google Gemini API key**

4. **Run the app**

   ```bash
   flutter run
   ```

---

## Screenshots

<div align="center">

| AI Assistant | Blog Generator | Code Explainer |
|--------------|----------------|----------------|
| <img src="Screenshots/ai_assistant.jpg" width="250"/> | <img src="Screenshots/blog_ai_assistant.jpg" width="250"/> | <img src="Screenshots/code_explainer.jpg" width="250"/> |

| CSV Analyzer | SQL Generator | Document Summarizer |
|--------------|---------------|----------------------|
| <img src="Screenshots/csv_analyzer.jpg" width="250"/> | <img src="Screenshots/sql_query_generator.jpg" width="250"/> | <img src="Screenshots/dowument_summarizer.jpg" width="250"/> |

| Website Summarizer |
|--------------------|
| <img src="Screenshots/website_summarizer.jpg" width="250"/> |

</div>

---

## Built With

* **Flutter** – Cross-platform mobile framework
* **Dart** – Core language
* **Google Gemini API** – Large Language Model backend
* **SharedPreferences** – Local storage for chat history
* **Custom Widgets** – Sidebar navigation, loading animations, tool routing

---

## Author

**Moustafa Mohamed** – AI Developer
[GitHub](https://github.com/MoustafaMohamed01) • [LinkedIn](https://linkedin.com/in/moustafamohamed01) • [Kaggle](https://kaggle.com/moustafamohamed01)
