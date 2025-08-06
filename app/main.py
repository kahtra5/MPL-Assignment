# app/main.py

from typing import List
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import engine, get_db

# This creates the tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="YouTube Video Fetcher API",
    description="An API to fetch and store latest YouTube videos.",
    version="1.0.0"
)

@app.get("/", tags=["Root"])
def read_root():
    """ A simple health check endpoint. """
    return {"status": "ok", "message": "Welcome to the YouTube API!"}

@app.get("/dashboard", tags=["Frontend"])
def get_dashboard():
    """ Serve the frontend dashboard. """
    return FileResponse("../frontend/index.html")

@app.get("/videos", response_model=List[schemas.Video], tags=["Videos"])
def read_videos(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """
    Retrieve stored videos in a paginated response, sorted by publishing date.
    """
    videos = crud.get_videos(db, skip=skip, limit=limit)
    return videos