# app/worker.py

import logging
from celery import Celery
from celery.schedules import crontab
from datetime import datetime, timedelta, timezone

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dateutil.parser import isoparse

from . import config, crud, models, schemas
from .database import SessionLocal

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Celery Setup ---
celery_app = Celery(__name__, broker=config.REDIS_URL, backend=config.REDIS_URL)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# --- API Key Management ---
class ApiKeyManager:
    """ A simple class to cycle through API keys. """
    def __init__(self, keys):
        self.keys = keys
        self.current_key_index = 0
    
    def get_key(self):
        return self.keys[self.current_key_index]
    
    def get_next_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.keys)
        logger.warning(f"Switching to API key index: {self.current_key_index}")
        return self.get_key()

api_key_manager = ApiKeyManager(config.API_KEYS)

# --- Celery Task Definition ---
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """ Sets up the periodic task to run every 10 seconds. """
    sender.add_periodic_task(10.0, fetch_latest_videos.s(), name='fetch videos every 10s')

@celery_app.task
def fetch_latest_videos():
    """
    A Celery task to fetch the latest videos from YouTube for a predefined query.
    """
    db = SessionLocal()
    try:
        # Get the timestamp of the latest video we have stored
        published_after_dt = crud.get_latest_video_timestamp(db)
        # Format for YouTube API (RFC 3339 format)
        published_after = published_after_dt.isoformat("T", "seconds") + "Z"
        
        logger.info(f"Fetching videos published after: {published_after}")
        
        youtube_service = None
        
        # Loop to handle API key rotation
        for _ in range(len(api_key_manager.keys)):
            try:
                api_key = api_key_manager.get_key()
                youtube_service = build("youtube", "v3", developerKey=api_key)
                
                request = youtube_service.search().list(
                    q=config.SEARCH_QUERY,
                    part="snippet",
                    type="video",
                    order="date",
                    maxResults=25, # Fetch up to 25 results per call
                    publishedAfter=published_after
                )
                response = request.execute()
                
                videos_saved = 0
                for item in response.get("items", []):
                    video_data = schemas.VideoCreate(
                        video_id=item["id"]["videoId"],
                        title=item["snippet"]["title"],
                        description=item["snippet"]["description"],
                        published_at=isoparse(item["snippet"]["publishedAt"]),
                        thumbnail_url=item["snippet"]["thumbnails"]["default"]["url"],
                    )
                    crud.create_video(db=db, video=video_data)
                    videos_saved += 1
                
                if videos_saved > 0:
                    logger.info(f"Successfully fetched and saved {videos_saved} new videos.")
                else:
                    logger.info("No new videos found.")
                
                # If the call was successful, break the loop
                break

            except HttpError as e:
                # Check if the error is a quota exhaustion error
                if e.resp.status == 403:
                    logger.error("Quota exhausted on current API key. Trying next key...")
                    api_key_manager.get_next_key()  # Switch to the next key
                    continue # Retry the loop with the new key
                else:
                    logger.error(f"An unexpected HTTP error occurred: {e}")
                    break # Break on other HTTP errors
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                break # Break on any other non-HTTP error

    finally:
        db.close()