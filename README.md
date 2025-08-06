# YouTube Videos Dashboard - MPL Assignment

A complete YouTube video fetching and dashboard system with a modern web interface for browsing and filtering videos.

## 🚀 Quick Start

1. **Clone and Setup**:

   ```bash
   git clone <repository-url>
   cd MPL-Assignment
   ```

2. **Configure Environment**:
   Create a `.env` file with your configuration:

   ```env
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_DB=youtube_videos
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   REDIS_HOST=redis
   REDIS_PORT=6379
   YOUTUBE_API_KEYS=your_api_key1,your_api_key2
   SEARCH_QUERY=cricket
   ```

3. **Start the Application**:

   ```bash
   docker-compose up
   ```

4. **Access the Dashboard**:
   Open your browser and go to: **http://localhost:8000/dashboard**

## 📊 Dashboard Features

### 🎯 Main Features

- **Real-time Video Display**: Shows videos fetched from YouTube API
- **Advanced Search**: Search by title or description with real-time filtering
- **Date Range Filtering**: Filter videos by publication date
- **Responsive Pagination**: Navigate through large video collections
- **Auto-refresh**: Updates every 30 seconds to show new videos
- **Mobile-friendly**: Responsive design that works on all devices

### 🔍 Filtering Options

- **Text Search**: Type in the search box to filter by title/description
- **Date Range**: Use "From Date" and "To Date" to filter by publication time
- **Results Per Page**: Choose 10, 20, 50, or 100 videos per page
- **Real-time Updates**: Filters apply automatically as you type

### 📱 User Interface

- **Modern Design**: Clean, professional interface with gradient backgrounds
- **Video Cards**: Each video shows thumbnail, title, description, and metadata
- **Statistics**: Real-time stats showing total videos and last update time
- **Error Handling**: User-friendly error messages and loading states

## 🏗️ Architecture

### Backend Components

- **FastAPI**: REST API server with automatic documentation
- **PostgreSQL**: Database for storing video metadata
- **Redis**: Message broker for background tasks
- **Celery**: Background worker for fetching YouTube videos
- **SQLAlchemy**: ORM for database operations

### Frontend Components

- **HTML5**: Semantic markup with modern structure
- **CSS3**: Responsive design with Flexbox/Grid layouts
- **Vanilla JavaScript**: No frameworks, pure ES6+ code
- **Font Awesome**: Icons for better visual experience

## 🛠️ API Endpoints

### Core Endpoints

- `GET /`: Health check endpoint
- `GET /videos`: Retrieve paginated videos (supports `skip` and `limit`)
- `GET /dashboard`: Serve the frontend dashboard
- `GET /static/*`: Static file serving for CSS/JS

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

Run the test script to verify everything works:

```bash
python test_dashboard.py
```

This will test:

- API health and connectivity
- Videos endpoint functionality
- Dashboard HTML serving
- Static file serving (CSS/JS)

## 📁 Project Structure

```
MPL-Assignment/
├── app/                    # Backend application
│   ├── main.py            # FastAPI application with CORS and static serving
│   ├── models.py          # SQLAlchemy database models
│   ├── schemas.py         # Pydantic schemas for API
│   ├── crud.py            # Database operations
│   ├── worker.py          # Celery background tasks
│   ├── database.py        # Database configuration
│   └── config.py          # Environment configuration
├── frontend/              # Frontend dashboard
│   ├── index.html         # Main dashboard HTML
│   ├── styles.css         # Responsive CSS styling
│   ├── script.js          # JavaScript for API interaction
│   └── README.md          # Frontend-specific documentation
├── docker-compose.yml     # Multi-container setup
├── Dockerfile            # Container configuration
├── requirements.txt      # Python dependencies
├── test_dashboard.py     # Test script for verification
└── README.md            # This file
```
