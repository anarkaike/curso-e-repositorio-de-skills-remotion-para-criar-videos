from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from typing import List, Optional
import uuid
import logging
from duckduckgo_search import DDGS
import urllib.parse
import shutil
import requests
from pathlib import Path
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from database import create_db_and_tables, get_session
from models import (
    Project, ProjectCreate, ProjectUpdate, ProjectRead, 
    Reference, ReferenceBase, ImageSuggestion, VideoGenerationRequest
)
from services import run_video_generation, generate_suggestions

# Setup logging
logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/suggestions/{suggestion_type}")
async def get_suggestions(suggestion_type: str, context: str):
    """
    Get AI suggestions for wizard fields.
    suggestion_type: target_audience, keywords, colors, emotions
    context: string input
    """
    return await generate_suggestions(suggestion_type, context)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Mount uploads directory to serve images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def read_root():
    return {"message": "Video Wizard API is running with SQLite Persistence"}

@app.post("/projects", response_model=ProjectRead)
def create_project(project_in: ProjectCreate, session: Session = Depends(get_session)):
    project_id = project_in.id or str(uuid.uuid4())
    db_project = Project.model_validate(project_in, update={"id": project_id})
    
    # Handle list conversions
    db_project.keywords = project_in.keywords
    db_project.emotions = project_in.emotions
    
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

@app.put("/projects/{project_id}", response_model=ProjectRead)
def update_project(project_id: str, project_in: ProjectUpdate, session: Session = Depends(get_session)):
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project_data = project_in.model_dump(exclude_unset=True)
    
    # Handle special list fields
    if "keywords" in project_data:
        db_project.keywords = project_data.pop("keywords")
    if "emotions" in project_data:
        db_project.emotions = project_data.pop("emotions")
    if "context_photos" in project_data:
        db_project.context_photos = project_data.pop("context_photos")
        
    # Handle references separately if needed, or just update basic fields
    # For simplicity, we assume references are handled via separate endpoint or we update logic here
    # Since Reference is a separate table, we should update it carefully.
    # For now, let's update simple fields:
    for key, value in project_data.items():
        if key != "references":
            setattr(db_project, key, value)
            
    # Update references
    if project_in.references is not None:
        # Clear existing references (simple approach)
        for ref in db_project.references:
            session.delete(ref)
        
        # Add new ones
        for ref_in in project_in.references:
            db_ref = Reference.model_validate(ref_in)
            db_ref.project = db_project
            session.add(db_ref)
            
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

@app.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(project_id: str, session: Session = Depends(get_session)):
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@app.get("/projects", response_model=List[ProjectRead])
def list_projects(session: Session = Depends(get_session)):
    projects = session.exec(select(Project)).all()
    return projects

@app.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = UPLOAD_DIR / filename
        
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {"url": f"http://localhost:35000/uploads/{filename}", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import random

@app.get("/proxy/image")
async def proxy_image(url: str):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        resp = requests.get(url, headers=headers, stream=True, timeout=10)
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch image")
        
        return StreamingResponse(resp.iter_content(chunk_size=1024), media_type=resp.headers.get("content-type", "image/jpeg"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/suggestions/images", response_model=List[ImageSuggestion])
def get_image_suggestions(query: str):
    results = []
    
    # 1. AI Generation (Pollinations.ai)
    prompts = [
        f"professional photo of {query}, cinematic lighting, 4k",
        f"illustration of {query}, modern vector art",
        f"close up shot of {query}, detailed"
    ]
    
    for i, prompt in enumerate(prompts):
        encoded_prompt = urllib.parse.quote(prompt)
        # Use simpler URL structure which might be more stable
        # Add random seed to ensure variety
        seed = random.randint(0, 10000)
        original_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true&seed={seed}&width=1080&height=1920"
        
        # Verify if URL is reachable (optional, but good for user experience)
        proxied_url = f"http://localhost:35000/proxy/image?url={urllib.parse.quote(original_url)}"

        results.append(ImageSuggestion(
            url=proxied_url,
            source="AI (Pollinations)",
            description=prompt
        ))

    # 2. Web Search (DuckDuckGo)
    try:
        with DDGS() as ddgs:
            ddgs_images = list(ddgs.images(query, max_results=5))
            for img in ddgs_images:
                original_url = img['image']
                proxied_url = f"http://localhost:35000/proxy/image?url={urllib.parse.quote(original_url)}"
                results.append(ImageSuggestion(
                    url=proxied_url,
                    source="Web (DDG)",
                    description=img['title']
                ))
    except Exception as e:
        logging.error(f"DDG Search failed: {e}")
        # Fallback to placeholder if search fails
        results.append(ImageSuggestion(
            url=f"https://placehold.co/600x400?text={query}", 
            source="Fallback", 
            description=f"Placeholder for {query}"
        ))

    return results

import pydantic

class GenerateVideoRequest(pydantic.BaseModel):
    project_id: str
    selected_images: List[str]
    script_text: str
    template: str = "simple"
    header_text: str = ""
    footer_text: str = ""

@app.post("/generate/video")
async def generate_video(request: GenerateVideoRequest, session: Session = Depends(get_session)):
    db_project = session.get(Project, request.project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Convert SQLModel to dict for the service
    project_dict = db_project.model_dump()
    project_dict['keywords'] = db_project.keywords
    project_dict['emotions'] = db_project.emotions
    
    # Run video generation
    result = await run_video_generation(
        project_dict, 
        request.selected_images,
        request.script_text,
        template=request.template,
        header_text=request.header_text,
        footer_text=request.footer_text
    )
    
    if result["status"] == "failed":
         raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
         
    return result
