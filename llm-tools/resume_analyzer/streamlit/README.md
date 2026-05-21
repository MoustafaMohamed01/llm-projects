## AI Resume Analyzer

### Overview

The **AI Resume Analyzer** is a Streamlit-based web application designed to analyze resumes using Google’s Generative AI models. It extracts, interprets, and evaluates the content of uploaded resumes (PDF or DOCX) to provide meaningful insights such as skill summaries, professional tone feedback, and improvement suggestions.

This tool helps job seekers enhance their resumes by leveraging the power of AI for personalized analysis and optimization.

---

### Features

* **AI-Powered Resume Analysis** – Uses Google Gemini (Generative AI) to extract and analyze key sections of resumes.
* **Multi-format Support** – Accepts both PDF and DOCX files.
* **Smart Insights** – Generates feedback on clarity, structure, and skill alignment.
* **Streamlit Web Interface** – Simple, interactive, and accessible in the browser.
* **Local Execution** – Runs directly on your machine without external backend requirements.

---

### Technologies Used

* **Python 3.12+**
* **Streamlit** – For building the web UI
* **Google Generative AI (Gemini)** – For text understanding and evaluation
* **PyPDF2** – For PDF text extraction
* **python-docx** – For DOCX file handling

---

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/MoustafaMohamed01/resume_analyzer.git
   cd resume_analyzer
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment**
   Create a `.env` file or set your API key directly:

   ```bash
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

---

### File Structure

```
resume_analyzer/
│
├── app.py                # Main Streamlit app
├── requirements.txt      # Dependencies
├── examples/             # Sample resumes
└── README.md             # Project documentation
```

---

### Usage

1. Launch the app using `streamlit run app.py`.
2. Upload a resume file (PDF or DOCX).
3. The AI model will process the text and generate insights.
4. View structured feedback directly in the web interface.

---

### Example Insights

* Summary of strengths and technical skills
* Suggested rewording for improved clarity
* Section balance and keyword optimization feedback
* Suitability for specific job roles

---

### Future Improvements

* Integration with LinkedIn for profile comparison
* Multi-language support
* Resume scoring system based on job descriptions
* Exporting results as a formatted PDF report

---

**Moustafa Mohamed**
Aspiring AI Developer | Specialized in Machine Learning, Deep Learning, and LLM Engineering

* GitHub: [MoustafaMohamed01](https://github.com/MoustafaMohamed01)
* Kaggle: [moustafamohamed01](https://www.kaggle.com/moustafamohamed01)
* LinkedIn: [Moustafa Mohamed](https://www.linkedin.com/in/moustafamohamed01/)

