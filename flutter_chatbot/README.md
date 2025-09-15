# Flutter Chatbot

A **cross-platform AI-powered chatbot app** built with **Flutter**. This project integrates Google’s **Gemini API** for intelligent responses and supports **local storage** for chat history.

## Project Structure

```
flutter_chatbot/
├── lib/
│   ├── main.dart                   # Entry point of the app
│   ├── models/                     # Data models
│   │   ├── message.dart             # Message model
│   │   └── chat.dart                # Chat session model
│   ├── services/                   # Core services
│   │   ├── gemini_service.dart      # Handles Gemini API requests
│   │   └── storage_service.dart     # Local storage (chat history, prefs)
│   ├── screens/                    # App screens
│   │   ├── home_screen.dart         # Main/home UI
│   │   └── chat_screen.dart         # Chat interface
│   ├── widgets/                    # Reusable UI components
│   │   ├── message_bubble.dart      # Chat message widget
│   │   └── chat_input.dart          # Input field & send button
│   └── utils/                      # Helper utilities
│       └── constants.dart           # App-wide constants
├── pubspec.yaml                     # Dependencies & assets
└── android/app/src/main/AndroidManifest.xml  # Permissions
```

## Features

* 💬 **AI Chatbot** powered by **Gemini API**.
* 📝 **Persistent chat history** using local storage.
* 📱 **Clean and modern UI** built with Flutter widgets.
* 🔄 **Separation of concerns** with modular architecture.

## Getting Started

### Prerequisites

* [Flutter SDK](https://flutter.dev/docs/get-started/install) (>=3.10.0)
* A valid **Gemini API Key** from [Google AI Studio](https://makersuite.google.com/app/apikey).

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/MoustafaMohamed01/llm-projects.git
   cd llm-projects/flutter_chatbot
   ```

2. Install dependencies:

   ```bash
   flutter pub get
   ```

3. Add your **Gemini API Key** in `lib/services/gemini_service.dart`:

   ```dart
   const String geminiApiKey = "YOUR_API_KEY";
   ```

4. Run the app:

   ```bash
   flutter run
   ```

## Permissions

`AndroidManifest.xml` includes:

* **INTERNET** – Required for API requests.
* **ACCESS\_NETWORK\_STATE** – Ensures connectivity checks.

## Roadmap

* [ ] Add support for offline AI models (e.g., MiniLM TFLite).
* [ ] Multi-language support.
* [ ] Deployment on Play Store.

## Contributing

Contributions are welcome! Please fork the repo and submit a pull request.

## License

This project is licensed under the **MIT License** – see [LICENSE](LICENSE) for details.

---
