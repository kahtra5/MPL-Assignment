# app/schemas.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base schema with fields common to both creation and reading
class VideoBase(BaseModel):
    video_id: str
    title: str
    description: Optional[str] = None
    published_at: datetime
    thumbnail_url: Optional[str] = None

# Schema used when creating a video (used by the worker)
class VideoCreate(VideoBase):
    pass

# Schema used when reading a video from the API (includes ORM mode)
class Video(VideoBase):
    class Config:
        orm_mode = True