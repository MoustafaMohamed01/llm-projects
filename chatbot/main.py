from fastapi import FastAPI, Request, Form, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime
import logging
from typing import Optional
from pathlib import Path

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

try:
    from api_key import GEMINI_API_KEY
    api_key = GEMINI_API_KEY
    logger.info("API key loaded from api_key.py")
except ImportError:
    api_key = os.getenv("GEMINI_API_KEY")
    logger.info("API key loaded from environment variables")

if not api_key:
    logger.error("No API key found. Please set GEMINI_API_KEY in .env file or api_key.py")
    raise RuntimeError("No API key found")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    logger.info("Gemini AI model initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Gemini AI: {str(e)}")
    raise RuntimeError("Failed to initialize AI service")

UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(exist_ok=True)

app = FastAPI(
    title="Gemini AI Chatbot API",
    description="A professional chatbot interface powered by Google's Gemini AI",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class ChatRequest:
    def __init__(self, prompt: str, session_id: Optional[str] = None):
        self.prompt = prompt
        self.session_id = session_id
        self.timestamp = datetime.now().isoformat()

chat_session = None

@app.on_event("startup")
async def startup_event():
    global chat_session
    try:
        chat_session = model.start_chat(history=[])
        logger.info("Chat session initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize chat session: {str(e)}")

@app.get("/", response_class=HTMLResponse)
def get_chat(request: Request):
    """Serve the main chat interface"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "version": app.version,
            "current_year": datetime.now().year
        }
    )

@app.post("/api/chat")
async def chat(prompt: str = Form(...), session_id: Optional[str] = Form(None)):
    """
    Process user chat messages and return AI responses
    """
    global chat_session
    
    try:
        chat_request = ChatRequest(prompt, session_id)
        logger.info(f"Processing chat request: {chat_request.__dict__}")
        
        if chat_session is None:
            chat_session = model.start_chat(history=[])
            logger.info("Chat session reinitialized")
        
        response = chat_session.send_message(
            prompt,
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_ONLY_HIGH"
                }
            ],
            generation_config={
                "max_output_tokens": 4000,
                "temperature": 0.7,
            }
        )
        
        reply = response.text
        logger.info(f"Successfully generated response for prompt: {prompt[:50]}...")
        
        return JSONResponse(
            content={
                "response": reply,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
        )
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        
        error_message = "Sorry, I encountered an error processing your request. Please try again."
        if "API_KEY" in str(e):
            error_message = "API key error. Please check your configuration."
        elif "quota" in str(e).lower():
            error_message = "API quota exceeded. Please try again later."
        elif "safety" in str(e).lower():
            error_message = "Your message was blocked by safety filters. Please rephrase your request."
        
        return JSONResponse(
            status_code=500,
            content={
                "response": error_message,
                "status": "error",
                "error": str(e)
            }
        )

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        max_size = 5 * 1024 * 1024
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > max_size:
            raise HTTPException(status_code=400, detail="File too large (max 5MB)")
        
        allowed_types = [
            "text/plain", "application/pdf", 
            "image/jpeg", "image/png",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ]
        
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())
        
        return JSONResponse(
            content={
                "status": "success",
                "filename": file.filename,
                "content_type": file.content_type,
                "size": file_size,
                "message": "File uploaded successfully"
            }
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "message": str(e)}
        )

@app.get("/api/health")
async def health_check():
    """Endpoint for health checks and monitoring"""
    return JSONResponse(
        content={
            "status": "healthy",
            "version": app.version,
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
