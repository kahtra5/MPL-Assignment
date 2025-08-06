from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL

# The database "engine" is the entry point to our database.
# It's configured with the URL from our .env file.
engine = create_engine(DATABASE_URL)

# A SessionLocal class is a factory for creating new Session objects.
# A Session is what you'll use to execute queries.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function to get a DB session for each request.
# This ensures the session is properly closed after the request is finished.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()