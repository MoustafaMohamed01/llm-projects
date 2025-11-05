import streamlit as st
import google.generativeai as genai
from pathlib import Path
import PyPDF2
import docx
import io
import json
import os

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme design
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: #000000;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: #0a0a0a;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8);
        margin: 1rem;
        border: 1px solid #1a1a1a;
    }
    
    /* Headers */
    h1 {
        color: #ffffff;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        font-size: 3rem !important;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
    }
    
    h2 {
        color: #ffffff;
        font-weight: 700;
        margin-top: 1.5rem;
        border-bottom: 3px solid #333333;
        padding-bottom: 0.5rem;
    }
    
    h3 {
        color: #ffffff;
        font-weight: 600;
    }
    
    /* All text color */
    p, span, div, label {
        color: #cccccc !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #0a0a0a;
        border-right: 1px solid #1a1a1a;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #cccccc;
    }
    
    [data-testid="stSidebar"] h2 {
        color: #ffffff;
        border-bottom: 2px solid #333333;
    }
    
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    
    /* Input fields */
    .stTextInput input, .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #1a1a1a;
        padding: 10px;
        font-size: 16px;
        background-color: #0a0a0a;
        color: #ffffff;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #333333;
        box-shadow: 0 0 0 2px rgba(51, 51, 51, 0.3);
        background-color: #141414;
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        border: none;
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
        border: 1px solid #333333;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 255, 255, 0.1);
        background: linear-gradient(135deg, #2d2d2d 0%, #404040 100%);
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #0a0a0a;
        border-radius: 15px;
        padding: 2rem;
        border: 2px dashed #333333;
    }
    
    [data-testid="stFileUploader"] label {
        color: #ffffff !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
    }
    
    [data-testid="stMetricLabel"] {
        color: #888888 !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #1a1a1a 0%, #404040 100%);
        height: 20px;
        border-radius: 10px;
    }
    
    .stProgress > div {
        background-color: #0a0a0a;
        border: 1px solid #1a1a1a;
    }
    
    /* Success/Warning/Info boxes */
    .stSuccess {
        background-color: rgba(34, 197, 94, 0.15);
        border-left: 5px solid #22c55e;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stWarning {
        background-color: rgba(251, 146, 60, 0.15);
        border-left: 5px solid #fb923c;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stInfo {
        background-color: rgba(156, 163, 175, 0.15);
        border-left: 5px solid #9ca3af;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stAlert {
        background-color: rgba(239, 68, 68, 0.15);
        border-left: 5px solid #ef4444;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Chat messages */
    [data-testid="stChatMessage"] {
        background: #0a0a0a;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        border: 1px solid #1a1a1a;
    }
    
    [data-testid="stChatInput"] {
        background-color: #0a0a0a;
        border: 2px solid #1a1a1a;
        border-radius: 10px;
    }
    
    [data-testid="stChatInput"] textarea {
        color: #ffffff !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #0a0a0a;
        border-radius: 10px;
        font-weight: 600;
        color: #ffffff !important;
        border: 1px solid #1a1a1a;
    }
    
    .streamlit-expanderContent {
        background-color: #0a0a0a;
        border: 1px solid #1a1a1a;
        border-top: none;
    }
    
    /* Score card styling */
    .score-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8);
        margin: 2rem 0;
        border: 2px solid #333333;
    }
    
    .score-number {
        font-size: 4rem;
        font-weight: 800;
        margin: 1rem 0;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
    }
    
    /* Card styling */
    .custom-card {
        background: #0a0a0a;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        margin: 1rem 0;
        border: 1px solid #1a1a1a;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Configure API key from api_key.py file
try:
    from api_key import GEMINI_API_KEY
    API_KEY = GEMINI_API_KEY
except ImportError:
    st.error("API Key not found. Please create 'api_key.py' file with your GEMINI_API_KEY.")
    st.info("Create a file named 'api_key.py' in the same folder with:\nGEMINI_API_KEY = 'your_api_key_here'")
    st.stop()

if not API_KEY:
    st.error("API Key is empty. Please add your key to api_key.py")
    st.stop()

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

# Helper functions
def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    doc = docx.Document(io.BytesIO(file.read()))
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_txt(file):
    """Extract text from TXT file"""
    return file.read().decode('utf-8')

def analyze_resume(resume_text, job_description, role, company):
    """Analyze resume against job description"""
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    prompt = f"""
You are an expert resume analyzer and career coach. Analyze the following resume against the job description for the position of {role} at {company}.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

TARGET ROLE: {role}
TARGET COMPANY: {company}

Provide a comprehensive analysis in the following JSON format:

{{
    "overall_score": <number between 0-100>,
    "strengths": [
        "strength 1",
        "strength 2",
        ...
    ],
    "missing_skills": [
        "missing skill 1",
        "missing skill 2",
        ...
    ],
    "keyword_match": {{
        "matched_keywords": ["keyword1", "keyword2", ...],
        "missing_keywords": ["keyword3", "keyword4", ...]
    }},
    "experience_relevance": <number between 0-100>,
    "skills_match": <number between 0-100>,
    "formatting_score": <number between 0-100>,
    "suggested_improvements": [
        "improvement 1",
        "improvement 2",
        ...
    ],
    "rewrite_suggestions": {{
        "summary": "Suggested professional summary",
        "key_achievements": ["achievement 1", "achievement 2", ...]
    }},
    "detailed_feedback": "A detailed paragraph explaining the overall assessment"
}}

Be specific, actionable, and honest in your assessment.
"""
    
    response = model.generate_content(prompt)
    
    # Parse JSON from response
    response_text = response.text
    # Remove markdown code blocks if present
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]
    
    return json.loads(response_text.strip())

def chat_with_ai(user_message, resume_text, job_description, role, company, analysis_result):
    """Chat with AI about resume improvements"""
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    context = f"""
You are a career coach helping improve a resume for the position of {role} at {company}.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

PREVIOUS ANALYSIS:
{json.dumps(analysis_result, indent=2)}

Previous conversation:
{format_chat_history(st.session_state.chat_history)}

User question: {user_message}

Provide helpful, specific advice to improve the resume. Be conversational and supportive.
"""
    
    response = model.generate_content(context)
    return response.text

def format_chat_history(history):
    """Format chat history for context"""
    formatted = ""
    for msg in history[-5:]:  # Last 5 messages for context
        formatted += f"{msg['role']}: {msg['content']}\n"
    return formatted

# Main UI
st.markdown("<h1>AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888; font-size: 1.2rem; margin-bottom: 2rem;'>Powered by Gemini 2.0 Flash - Get instant feedback on your resume</p>", unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.markdown("## Job Details")
    role = st.text_input("Target Role", placeholder="e.g., Senior Software Engineer", help="Enter the position you're applying for")
    company = st.text_input("Target Company", placeholder="e.g., Google", help="Enter the company name")
    
    st.markdown("---")
    st.markdown("## About")
    st.info("Upload your resume and job description to get AI-powered analysis with personalized improvement suggestions.")
    
    st.markdown("---")
    st.markdown("## How It Works")
    st.markdown("""
    1. Enter target role and company
    2. Upload your resume
    3. Paste job description
    4. Click 'Analyze Resume'
    5. Chat for improvements
    """)
    
    st.markdown("---")
    st.markdown("## Tips")
    st.markdown("""
    - Use complete job descriptions
    - Ensure resume is well-formatted
    - Be specific about your target role
    """)

# Main content area
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("## Upload Documents")
    
    resume_file = st.file_uploader(
        "**Upload Your Resume**",
        type=['pdf', 'docx', 'txt'],
        help="Supported formats: PDF, DOCX, TXT"
    )
    
    if resume_file:
        file_type = resume_file.name.split('.')[-1].lower()
        
        try:
            if file_type == 'pdf':
                st.session_state.resume_text = extract_text_from_pdf(resume_file)
            elif file_type == 'docx':
                st.session_state.resume_text = extract_text_from_docx(resume_file)
            else:
                st.session_state.resume_text = extract_text_from_txt(resume_file)
            
            st.success(f"Resume uploaded successfully!")
            st.info(f"**{len(st.session_state.resume_text)}** characters extracted")
        except Exception as e:
            st.error(f"Error reading resume: {str(e)}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    job_desc = st.text_area(
        "**Job Description**",
        height=250,
        placeholder="Paste the complete job description here...\n\nInclude responsibilities, requirements, and qualifications for best results.",
        help="The more detailed the job description, the better the analysis"
    )
    
    if job_desc:
        st.session_state.job_description = job_desc

with col2:
    st.markdown("## Ready to Analyze?")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    can_analyze = resume_file and job_desc and role and company
    
    if not can_analyze:
        st.warning("Please complete all fields to analyze your resume:")
        missing = []
        if not role: missing.append("Target Role")
        if not company: missing.append("Target Company")
        if not resume_file: missing.append("Resume")
        if not job_desc: missing.append("Job Description")
        st.markdown("**Missing:** " + ", ".join(missing))
    
    analyze_button = st.button("Analyze Resume", type="primary", disabled=not can_analyze, use_container_width=True)
    
    if analyze_button:
        with st.spinner("AI is analyzing your resume... This may take a moment."):
            try:
                result = analyze_resume(
                    st.session_state.resume_text,
                    st.session_state.job_description,
                    role,
                    company
                )
                st.session_state.analysis_result = result
                st.session_state.analysis_done = True
                st.success("Analysis complete!")
                st.rerun()
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")

# Display analysis results
if st.session_state.analysis_done and st.session_state.analysis_result:
    st.markdown("---")
    
    result = st.session_state.analysis_result
    
    # Overall score card
    st.markdown(f"""
    <div class="score-card">
        <h2 style="color: white; margin: 0; border: none;">Overall Match Score</h2>
        <div class="score-number">{result['overall_score']}%</div>
        <p style="font-size: 1.1rem; margin: 0;">{"Excellent Match!" if result['overall_score'] >= 80 else "Good Match!" if result['overall_score'] >= 60 else "Room for Improvement"}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed scores
    st.markdown("### Detailed Breakdown")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Experience Relevance", f"{result['experience_relevance']}%", delta=None)
    with col2:
        st.metric("Skills Match", f"{result['skills_match']}%", delta=None)
    with col3:
        st.metric("Formatting", f"{result['formatting_score']}%", delta=None)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detailed feedback in a card
    st.markdown(f"""
    <div class="custom-card">
        <h3 style="margin-top: 0;">Detailed Feedback</h3>
        <p style="font-size: 1.05rem; line-height: 1.6;">{result['detailed_feedback']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Two columns for strengths and missing skills
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### Your Strengths")
        for strength in result['strengths']:
            st.success(f"**+** {strength}")
    
    with col2:
        st.markdown("### Missing Skills")
        for skill in result['missing_skills']:
            st.warning(f"**-** {skill}")
    
    # Keywords analysis
    st.markdown("---")
    st.markdown("### Keyword Analysis")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("**Matched Keywords:**")
        keywords_matched = ", ".join(result['keyword_match']['matched_keywords'])
        st.markdown(f"<div class='custom-card' style='border-left-color: #22c55e;'>{keywords_matched}</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Missing Keywords:**")
        keywords_missing = ", ".join(result['keyword_match']['missing_keywords'])
        st.markdown(f"<div class='custom-card' style='border-left-color: #fb923c;'>{keywords_missing}</div>", unsafe_allow_html=True)
    
    # Suggested improvements
    st.markdown("---")
    st.markdown("### Suggested Improvements")
    
    for i, improvement in enumerate(result['suggested_improvements'], 1):
        st.info(f"**{i}.** {improvement}")
    
    # Rewrite suggestions
    st.markdown("---")
    st.markdown("### Content Rewrite Suggestions")
    
    with st.expander("**Suggested Professional Summary**", expanded=False):
        st.markdown(f"<div style='padding: 1rem; background: #0a0a0a; border-radius: 10px; border: 1px solid #1a1a1a; color: #cccccc;'>{result['rewrite_suggestions']['summary']}</div>", unsafe_allow_html=True)
    
    with st.expander("**Key Achievements to Highlight**", expanded=False):
        for achievement in result['rewrite_suggestions']['key_achievements']:
            st.markdown(f"• {achievement}")
    
    # Chat interface
    st.markdown("---")
    st.markdown("### Chat with AI Career Coach")
    st.markdown("Ask questions about improving your resume, get clarification, or request specific rewrites.")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about improving your resume..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = chat_with_ai(
                        prompt,
                        st.session_state.resume_text,
                        st.session_state.job_description,
                        role,
                        company,
                        st.session_state.analysis_result
                    )
                    st.write(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #888888;'>
    <p style='font-size: 0.9rem;'>Built with streamlit and Google Gemini AI</p>
    <p style='font-size: 0.8rem; color: #666666;'>2025 AI Resume Analyzer - Your Career Success Partner</p>
</div>
""", unsafe_allow_html=True)
