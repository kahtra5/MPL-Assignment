# app/main.py

from typing import List
from fastapi import FastAPI, Depends
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