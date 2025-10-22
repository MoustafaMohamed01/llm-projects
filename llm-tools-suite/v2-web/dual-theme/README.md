# LLM Tools Suite

A comprehensive AI-powered productivity toolkit with **Dark/Light Theme Toggle**.

## Features

- **7 AI-Powered Tools**:
  - AI Assistant
  - Blog Generator
  - CSV Data Analyzer
  - SQL Query Generator
  - Document Summarizer
  - Website Summarizer
  - Code Explainer

- **Theme System**:
  - 🌙 Dark Mode (Default)
  - ☀️ Light Mode with Blue Accent
  - Persistent theme preference
  - Smooth transitions

## Project Structure
```
LLM-Tools-Suite/
│
├── index.html          # Main HTML file
├── style.css           # Styles with theme variables
├── script.js           # JavaScript with theme logic
│
└── images/
    └── logo.png        # Your logo (place here)
```

## ⚙️ Setup Instructions

### 1. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key

### 2. Configure API Key

Open `script.js` and replace:
```javascript
const CONFIG = {
  GEMINI_API_KEY: "YOUR_GEMINI_API_KEY_HERE", // ← Replace with your key
  ...
};
```

### 3. Add Your Logo

1. Create an `images/` folder in your project directory
2. Place your logo as `logo.png` inside
3. Logo will automatically appear with theme-aware effects

### 4. Run the Project

Simply open `index.html` in a modern web browser (Chrome, Firefox, Edge, Safari).

### Theme Toggle Button

The theme toggle button is fixed in the top-right corner:
- **Dark Mode**: Shows ☀️
- **Light Mode**: Shows 🌙
- Preference is saved to localStorage

## How Theme System Works

1. **CSS Variables**: All colors use CSS custom properties
2. **Data Attribute**: `<body data-theme="dark">` controls which variables apply
3. **LocalStorage**: Theme preference persists across sessions
4. **JavaScript**: `toggleTheme()` function switches themes

## Browser Support

- Chrome/Edge
- Firefox
- Safari
- Mobile browsers

## Notes

- **Document/Website Summarizers**: Require server-side implementation for full functionality
- **CSV Analyzer**: Works with standard CSV format
- **All features**: Powered by Google's Gemini 2.5 Flash AI

## Features Highlights

### Dark Theme (Default)
- Sleek black/purple gradient
- Purple accents (#6366f1)
- Glowing effects on logo and buttons

### Light Theme
- Bright white/blue background (#f5faff)
- Google Blue accents (#1a73e8)
- Clean, modern design
- Professional appearance

## Security

- API key is client-side (for demo purposes)
- For production, use server-side API calls
- Never commit API keys to public repositories
