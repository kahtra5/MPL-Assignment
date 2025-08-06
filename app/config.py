import os
from dotenv import load_dotenv

# This function reads your .env file and loads its variables into the environment
load_dotenv()

# --- Database Config ---
# Reads the database connection details and assembles the full URL
DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

# --- Redis Config ---
# Assembles the connection URL for the Redis broker
REDIS_URL = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0"

# --- YouTube API Config ---
# Reads the comma-separated API keys and splits them into a Python list
API_KEYS = os.getenv("YOUTUBE_API_KEYS", "").split(',')

# Reads the search query, providing a default value if it's not set
SEARCH_QUERY = os.getenv("SEARCH_QUERY", "cricket")