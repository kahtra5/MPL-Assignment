from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Video(Base):
    __tablename__ = "videos"

    video_id = Column(String, primary_key=True, index=True, unique=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    published_at = Column(DateTime, index=True, nullable=False)
    thumbnail_url = Column(String, nullable=True)

    def __repr__(self):
        return f"<Video(title='{self.title}')>"