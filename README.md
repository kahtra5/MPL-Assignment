# YouTube Video Fetcher API & Dashboard

This project is a scalable system designed to continuously fetch the latest YouTube videos for a specific search query. It stores the video data in a PostgreSQL database and provides a paginated REST API and a simple, interactive web dashboard to view the results.

## Features

- **Continuous Background Fetching:** A Celery worker fetches new videos from the YouTube API every 10 seconds.
- **Paginated REST API:** A clean, paginated `GET /videos` endpoint to retrieve stored video data.
- **Resilient API Key Management:** Automatically rotates between multiple API keys if one runs out of quota.
- **Interactive Dashboard:** A simple frontend built with Jinja2 and vanilla JavaScript to view, filter, and sort the videos in real-time.
- **Scalable Architecture:** Built with FastAPI, Celery, and Docker, the system is designed for high performance and easy scalability.
- **Easy Setup:** The entire application stack is containerized with Docker and managed with a single Docker Compose file.

## Architecture

The system uses a microservices-style architecture where the API server is decoupled from the background data-fetching process.

- **API Server (FastAPI):** Handles user requests for the API and the dashboard.
- **Database (PostgreSQL):** Stores all video data.
- **Worker (Celery):** Runs the background task of calling the YouTube API.
- **Scheduler (Celery Beat):** Triggers the worker task on a regular interval.
- **Message Broker (Redis):** Passes messages between the scheduler and the worker.

## Technology Stack

- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** PostgreSQL
- **Async Tasks:** Celery, Redis
- **Frontend:** Jinja2, JavaScript, Pico.css
- **Containerization:** Docker, Docker Compose

---

## Setup and Installation

Follow these steps to get the project running locally.

### Prerequisites

- [Git](https://git-scm.com/downloads)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd youtube-api-project
```

### 2. Configure Environment Variables

Create a `.env` file by copying the example file.

```bash
cp .env.example .env
```

Now, open the `.env` file and add your own credentials:

```ini
# .env

# PostgreSQL Database (you can leave these as they are for local development)
POSTGRES_USER=admin
POSTGRES_PASSWORD=supersecret
POSTGRES_DB=youtube_videos
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis (leave as is)
REDIS_HOST=redis
REDIS_PORT=6379

# YouTube API Keys (REQUIRED: add your comma-separated keys)
YOUTUBE_API_KEYS="YOUR_API_KEY_1,YOUR_API_KEY_2"

# Search Query (change if you want)
SEARCH_QUERY="cricket"
```

### 3. Run the Application

Use Docker Compose to build the images and start all the services.

```bash
docker-compose up --build
```

The application will now be running. The worker will start fetching videos in the background.

---

## Usage

Once the application is running, you can access the following:

### 1. Web Dashboard

The main user interface for viewing videos.

- **URL:** `http://localhost:8000/dashboard`

### 2. API Documentation (Swagger UI)

FastAPI automatically generates interactive API documentation.

- **URL:** `http://localhost:8000/docs`

### 3. API Examples

You can interact with the API directly using tools like `curl` or Postman.

- **Get the first page of videos:**
  ```bash
  curl "http://localhost:8000/videos"
  ```
- **Get the next page:**
  ```bash
  curl "http://localhost:8000/videos?skip=20&limit=20"
  ```
- **Search for videos with "highlight" in the title:**
  ```bash
  curl "http://localhost:8000/videos?search=highlight"
  ```

## Project Structure

```
.
├── app/                  # Main Python application source code
│   ├── __init__.py
│   ├── config.py         # Loads environment variables
│   ├── crud.py           # Database interaction logic (CRUD)
│   ├── database.py       # Database session management
│   ├── main.py           # FastAPI app, API endpoints
│   ├── models.py         # SQLAlchemy database models
│   ├── schemas.py        # Pydantic data schemas
│   └── worker.py         # Celery worker and tasks
├── templates/            # Jinja2 HTML templates
│   └── index.html
├── .env                  # Your local environment variables (ignored by Git)
├── .env.example          # Example environment file
├── .gitignore            # Files and directories to be ignored by Git
├── docker-compose.yml    # Defines and configures all services
├── Dockerfile            # Blueprint for building the Python app image
├── requirements.txt      # Python dependencies
└── README.md             # This file
```
