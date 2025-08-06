# app/crud.py

from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from . import models, schemas

def get_latest_video_timestamp(db: Session) -> datetime:
    """
    Fetches the publishing timestamp of the most recent video stored in the database.
    """
    latest_video = db.query(models.Video).order_by(models.Video.published_at.desc()).first()
    if latest_video:
        return latest_video.published_at
    # If DB is empty, fetch videos from the last 5 minutes as a starting point.
    return datetime.now(timezone.utc) - timedelta(minutes=5)

def create_video(db: Session, video: schemas.VideoCreate):
    """
    Creates a new video record in the database if it doesn't already exist.
    """
    # Check if a video with the same ID already exists
    db_video = db.query(models.Video).filter(models.Video.video_id == video.video_id).first()
    if db_video:
        return db_video # Video already exists, do nothing

    db_video = models.Video(**video.dict())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

def get_videos(db: Session, skip: int = 0, limit: int = 20):
    """
    Retrieves a paginated list of videos from the database, sorted by published date.
    """
    return db.query(models.Video).order_by(models.Video.published_at.desc()).offset(skip).limit(limit).all()