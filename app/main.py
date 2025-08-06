# app/main.py

from typing import List, Optional
from fastapi import FastAPI, Depends
from fastapi import FastAPI, Depends, Request # Add Request
from fastapi.responses import HTMLResponse # Add HTMLResponse
from fastapi.templating import Jinja2Templates # Add Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from . import models, schemas, crud, config
from .database import engine, get_db

# This creates the tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="YouTube Video Fetcher API",
    description="An API to fetch and store latest YouTube videos.",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")

@app.get("/", tags=["Root"])
def read_root():
    """ A simple health check endpoint. """
    return {"status": "ok", "message": "Welcome to the YouTube API!"}

@app.get("/dashboard", response_class=HTMLResponse, tags=["Dashboard"])
def get_dashboard(request: Request, db: Session = Depends(get_db)):
    """
    Serves the HTML dashboard.
    """
    # Fetch initial data to render the page
    videos = crud.get_videos(db, limit=50) # Load 50 videos initially
    return templates.TemplateResponse("index.html", {
        "request": request,
        "videos": videos,
        "search_query": config.SEARCH_QUERY
    })

@app.get("/videos", response_model=List[schemas.Video], tags=["Videos"])
def read_videos(skip: int = 0, limit: int = 20, search: Optional[str] = None, sort: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Retrieve stored videos in a paginated response, sorted by publishing date.
    """
    videos = crud.get_videos(db, skip=skip, limit=limit, search=search, sort=sort)
    return videos