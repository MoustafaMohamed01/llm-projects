# Interview Trainer

**Interview Trainer** is an AI-powered interactive platform designed to help candidates prepare for professional interviews.
It dynamically generates interview questions, evaluates answers, and provides structured feedback using **Google Gemini API** — offering a realistic, data-driven interview experience.

---

## Features

* **Automated Question Generation**
  Creates customized technical and behavioral questions based on the provided job title, company, and job description.

* **AI-Powered Evaluation**
  Uses Gemini’s advanced language models to assess each answer for relevance, depth, and clarity. Generates a score from 1 to 10 with concise feedback.

* **Interactive Practice Flow**
  Real-time scoring, navigation between questions, and performance visualization.

* **Comprehensive Summary Report**
  Provides a final professional evaluation covering performance, strengths, and improvement areas.

* **Modern Dark-Themed UI**
  A sleek, accessible design built with Streamlit for an engaging user experience.

---

## Tech Stack

* **Frontend:** Streamlit
* **Backend:** Google Gemini (via `google-generativeai`)
* **Language:** Python 3.9+
* **Libraries:**

  * `streamlit`
  * `google-generativeai`
  * `json`, `re`, `time`

---

## Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/MoustafaMohamed01/llm-projects.git
   cd llm-projects/interview_trainer
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Gemini API key:**
   Create a file named `api_key.py` in the root of `interview_trainer` and add:

   ```python
   api_key = "YOUR_GEMINI_API_KEY"
   ```

4. **Run the Streamlit app:**

   ```bash
   streamlit run app.py
   ```

---

## Usage

1. Enter:

   * Job Title
   * Company Name
   * Job Description

2. Select the number of questions and start the interview.

3. Type your answers; the model evaluates and scores them in real-time.

4. Review your overall score and receive detailed feedback at the end of the session.

---

## Example

**Input Example:**

* Job Title: *Machine Learning Engineer*
* Company: *TechVision AI*
* Job Description: *Building and deploying scalable ML models.*

**Generated Output:**

```
Question: Explain the difference between batch and online learning.
Score: 8/10
Feedback: Clear and relevant explanation with good understanding of scalability trade-offs.
```

**Final Summary:**
Includes a professional evaluation detailing:

* Strengths demonstrated
* Areas for improvement
* Personalized preparation recommendations

---

## Folder Structure

```
interview_trainer/
   ├── app.py
   ├── api_key.py
   ├── requirements.txt
   └── README.md
```

---

**Moustafa Mohamed**

* **LinkedIn:** [linkedin.com/in/moustafamohamed01](https://www.linkedin.com/in/moustafamohamed01/)
* **GitHub:** [github.com/MoustafaMohamed01](https://github.com/MoustafaMohamed01)
* **Kaggle:** [kaggle.com/moustafamohamed01](https://www.kaggle.com/moustafamohamed01)
