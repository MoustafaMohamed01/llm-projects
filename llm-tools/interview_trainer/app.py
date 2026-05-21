import streamlit as st
import google.generativeai as genai
from api_key import api_key
import json
import re
import time

# Configure Gemini API
genai.configure(api_key=api_key)

# Initialize session state
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_question_idx' not in st.session_state:
    st.session_state.current_question_idx = 0
if 'results' not in st.session_state:
    st.session_state.results = []
if 'interview_complete' not in st.session_state:
    st.session_state.interview_complete = False

# Page config
st.set_page_config(
    page_title="Interview Trainer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
    
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-size: 1rem;
        color: #8b92a8;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #ffffff;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid #1f2937;
        padding-bottom: 0.5rem;
    }
    
    .score-high {
        background: linear-gradient(135deg, #1e3a2e 0%, #243b31 100%);
        border-left: 4px solid #10b981;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .score-medium {
        background: linear-gradient(135deg, #3d3020 0%, #443526 100%);
        border-left: 4px solid #f59e0b;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .score-low {
        background: linear-gradient(135deg, #3d1f1f 0%, #442626 100%);
        border-left: 4px solid #ef4444;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .question-card {
        background-color: #1f2937;
        padding: 2rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border: 1px solid #374151;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
    }
    
    .metric-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #475569;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 700;
        color: #3b82f6;
        margin: 0;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #94a3b8;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stProgress > div > div > div > div {
        background-color: #3b82f6;
    }
    
    hr {
        border-color: #374151;
        margin: 2rem 0;
    }
    
    .tag-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        background-color: #374151;
        color: #9ca3af;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .question-text {
        font-size: 1.3rem;
        color: #e5e7eb;
        font-weight: 500;
        line-height: 1.6;
        margin: 1rem 0;
    }
    
    .stTextInput input, .stTextArea textarea {
        background-color: #1f2937 !important;
        color: #e5e7eb !important;
        border: 1px solid #374151 !important;
    }
    
    .streamlit-expanderHeader {
        background-color: #1f2937 !important;
        color: #e5e7eb !important;
        border-radius: 8px !important;
    }
    
    .stButton button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

def clean_json_response(text):
    """Clean and extract JSON from response text"""
    text = text.strip()
    # Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    text = text.strip()
    return text

def generate_questions(job_title, company_name, job_description, num_questions):
    """Generate interview questions using Gemini with retry logic"""
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    prompt = f"""You are a professional technical interviewer for {job_title} at {company_name}.

Job Description:
{job_description}

Generate exactly {num_questions} interview questions for this role.
- Include both technical and behavioral questions
- Start with easier questions and gradually increase difficulty
- Make questions specific and relevant to the job description

Return ONLY a JSON array of questions in this exact format:
[
    {{"question": "Question 1 text here", "type": "technical", "difficulty": "easy"}},
    {{"question": "Question 2 text here", "type": "behavioral", "difficulty": "medium"}}
]"""

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            response_text = clean_json_response(response.text)
            questions = json.loads(response_text)
            return questions
        except Exception as e:
            if "429" in str(e) or "Resource exhausted" in str(e):
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5
                    st.warning(f"Rate limit reached. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise Exception("Rate limit exceeded. Please wait a few minutes and try again.")
            else:
                raise e

def evaluate_answer(job_title, company_name, job_description, question, answer):
    """Evaluate user's answer using Gemini with retry logic"""
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    prompt = f"""You are evaluating an interview answer for {job_title} at {company_name}.

Job Description: {job_description}

Question: {question}

Candidate's Answer: {answer}

Evaluate this answer based on:
1. Relevance to the question
2. Technical correctness (if applicable)
3. Depth of explanation
4. Communication clarity

Provide:
- A score from 1 to 10
- Brief constructive feedback (2-3 sentences)

Return ONLY a JSON object in this exact format:
{{"score": 8, "feedback": "Your feedback here"}}"""

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            response_text = clean_json_response(response.text)
            evaluation = json.loads(response_text)
            return evaluation
        except Exception as e:
            if "429" in str(e) or "Resource exhausted" in str(e):
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5
                    st.warning(f"Rate limit reached. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise Exception("Rate limit exceeded. Please wait a few minutes before submitting your next answer.")
            else:
                raise e

def generate_final_summary(job_title, results, total_score):
    """Generate final evaluation summary using Gemini with retry logic"""
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    results_text = "\n".join([
        f"Q: {r['question']}\nA: {r['answer']}\nScore: {r['score']}/10\nFeedback: {r['feedback']}\n"
        for r in results
    ])
    
    prompt = f"""You are providing final interview feedback for a {job_title} candidate.

Interview Results:
{results_text}

Average Score: {total_score:.1f}/10

Provide a comprehensive evaluation (3-4 paragraphs) covering:
1. Overall performance summary
2. Key strengths demonstrated
3. Areas needing improvement
4. Specific, actionable advice for preparation

Be constructive, professional, and encouraging."""

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e) or "Resource exhausted" in str(e):
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5
                    st.warning(f"Rate limit reached. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    return "Unable to generate final summary due to API rate limits. Your detailed scores and feedback are shown above."
            else:
                raise e

# Main UI
st.markdown('<div class="main-header">INTERVIEW TRAINER</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Professional Interview Practice Platform</div>', unsafe_allow_html=True)
st.markdown("---")

# Interview Setup
if not st.session_state.interview_started:
    st.markdown('<div class="section-header">Interview Configuration</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        job_title = st.text_input("Job Title", placeholder="e.g., Senior Software Engineer")
        company_name = st.text_input("Company Name", placeholder="e.g., Tech Corp")
    
    with col2:
        num_questions = st.slider("Number of Questions", min_value=3, max_value=10, value=5)
        st.write("")
        st.write("")
    
    job_description = st.text_area(
        "Job Description",
        placeholder="Paste the complete job description here...",
        height=250
    )
    
    st.write("")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("START INTERVIEW", type="primary", use_container_width=True):
            if job_title and company_name and job_description:
                with st.spinner("Generating personalized interview questions..."):
                    try:
                        questions = generate_questions(job_title, company_name, job_description, num_questions)
                        st.session_state.questions = questions
                        st.session_state.job_title = job_title
                        st.session_state.company_name = company_name
                        st.session_state.job_description = job_description
                        st.session_state.interview_started = True
                        st.session_state.current_question_idx = 0
                        st.session_state.results = []
                        st.session_state.interview_complete = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error generating questions: {str(e)}")
            else:
                st.warning("Please fill in all fields before starting the interview.")

# Interview in Progress
elif st.session_state.interview_started and not st.session_state.interview_complete:
    progress = st.session_state.current_question_idx / len(st.session_state.questions)
    st.progress(progress)
    
    st.write("")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**QUESTION {st.session_state.current_question_idx + 1} OF {len(st.session_state.questions)}**")
    
    st.markdown("---")
    
    current_question = st.session_state.questions[st.session_state.current_question_idx]
    
    st.markdown(f'<span class="tag-badge">{current_question["type"].upper()}</span><span class="tag-badge">DIFFICULTY: {current_question["difficulty"].upper()}</span>', unsafe_allow_html=True)
    
    st.write("")
    
    st.markdown(f'<div class="question-text">{current_question["question"]}</div>', unsafe_allow_html=True)
    
    st.write("")
    
    answer = st.text_area(
        "Your Answer",
        placeholder="Type your answer here...",
        height=200,
        key=f"answer_{st.session_state.current_question_idx}"
    )
    
    st.write("")
    
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
    
    with col1:
        if st.session_state.current_question_idx > 0:
            if st.button("PREVIOUS", use_container_width=True):
                st.session_state.current_question_idx -= 1
                st.rerun()
    
    with col3:
        if st.button("SUBMIT ANSWER", type="primary", use_container_width=True):
            if answer.strip():
                with st.spinner("Evaluating your answer..."):
                    try:
                        evaluation = evaluate_answer(
                            st.session_state.job_title,
                            st.session_state.company_name,
                            st.session_state.job_description,
                            current_question['question'],
                            answer
                        )
                        
                        result = {
                            'question': current_question['question'],
                            'type': current_question['type'],
                            'difficulty': current_question['difficulty'],
                            'answer': answer,
                            'score': evaluation['score'],
                            'feedback': evaluation['feedback']
                        }
                        
                        if st.session_state.current_question_idx < len(st.session_state.results):
                            st.session_state.results[st.session_state.current_question_idx] = result
                        else:
                            st.session_state.results.append(result)
                        
                        st.write("")
                        
                        score = evaluation['score']
                        if score >= 8:
                            st.success(f"**SCORE: {score}/10**")
                            st.markdown(f'<div class="score-high"><b>FEEDBACK:</b> {evaluation["feedback"]}</div>', unsafe_allow_html=True)
                        elif score >= 6:
                            st.info(f"**SCORE: {score}/10**")
                            st.markdown(f'<div class="score-medium"><b>FEEDBACK:</b> {evaluation["feedback"]}</div>', unsafe_allow_html=True)
                        else:
                            st.warning(f"**SCORE: {score}/10**")
                            st.markdown(f'<div class="score-low"><b>FEEDBACK:</b> {evaluation["feedback"]}</div>', unsafe_allow_html=True)
                        
                        st.write("")
                        
                        col_a, col_b, col_c = st.columns([2, 1, 2])
                        with col_b:
                            if st.session_state.current_question_idx < len(st.session_state.questions) - 1:
                                if st.button("NEXT QUESTION", type="primary", key="next_btn", use_container_width=True):
                                    st.session_state.current_question_idx += 1
                                    st.rerun()
                            else:
                                if st.button("COMPLETE INTERVIEW", type="primary", key="complete_btn", use_container_width=True):
                                    st.session_state.interview_complete = True
                                    st.rerun()
                    
                    except Exception as e:
                        st.error(f"Error evaluating answer: {str(e)}")
            else:
                st.warning("Please provide an answer before submitting.")

# Interview Complete - Summary
elif st.session_state.interview_complete:
    st.success("INTERVIEW COMPLETED")
    st.markdown("---")
    
    total_score = sum(r['score'] for r in st.session_state.results) / len(st.session_state.results)
    
    st.write("")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{total_score:.1f}/10</div>
                <div class="metric-label">Overall Score</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    st.markdown("---")
    
    st.markdown('<div class="section-header">Detailed Results</div>', unsafe_allow_html=True)
    
    for i, result in enumerate(st.session_state.results):
        with st.expander(f"QUESTION {i+1}: {result['question'][:80]}..." if len(result['question']) > 80 else f"QUESTION {i+1}: {result['question']}"):
            st.markdown(f'<span class="tag-badge">{result["type"].upper()}</span><span class="tag-badge">DIFFICULTY: {result["difficulty"].upper()}</span>', unsafe_allow_html=True)
            st.write("")
            st.markdown(f"**QUESTION:** {result['question']}")
            st.markdown(f"**YOUR ANSWER:** {result['answer']}")
            st.write("")
            
            score = result['score']
            if score >= 8:
                st.markdown(f'<div class="score-high"><b>SCORE: {score}/10</b><br>{result["feedback"]}</div>', unsafe_allow_html=True)
            elif score >= 6:
                st.markdown(f'<div class="score-medium"><b>SCORE: {score}/10</b><br>{result["feedback"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="score-low"><b>SCORE: {score}/10</b><br>{result["feedback"]}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div class="section-header">Performance Analysis</div>', unsafe_allow_html=True)
    
    with st.spinner("Generating comprehensive feedback..."):
        try:
            final_summary = generate_final_summary(
                st.session_state.job_title,
                st.session_state.results,
                total_score
            )
            st.markdown(final_summary)
        except Exception as e:
            st.error(f"Error generating final summary: {str(e)}")
    
    st.write("")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("START NEW INTERVIEW", type="primary", use_container_width=True):
            st.session_state.interview_started = False
            st.session_state.questions = []
            st.session_state.current_question_idx = 0
            st.session_state.results = []
            st.session_state.interview_complete = False
            st.rerun()
