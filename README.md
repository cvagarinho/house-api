# House API 🏥

> "Everybody lies... except this API's documentation" - Not Dr. House

A FastAPI-based clinical recommendations service that channels your inner Gregory House, M.D., minus the Vicodin addiction and questionable bedside manner. Just like the legendary doctor, this API excels at providing medical recommendations based on patient data - but with significantly less sarcasm and fewer workplace HR violations.

## Features

- 🔐 JWT Authentication
- 📊 Clinical Recommendations Generation
- 🚀 Redis Caching
- 📨 RabbitMQ Message Queue
- 🛢️ PostgreSQL Database
- 🔄 Async Database Operations
- 📝 OpenAPI Documentation

## Technology Stack

- FastAPI
- PostgreSQL with SQLAlchemy
- Redis for Caching
- RabbitMQ for Message Queue
- Docker & Docker Compose
- Python 3.12

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Make (optional)

### Installation

1. **Install Prerequisites**:
   ```bash
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Install Docker Compose
   sudo apt-get update
   sudo apt-get install docker-compose-plugin
   
   # Install Make
   sudo apt-get install make
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/cvagarinho/house-api.git
   cd house-api
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env.local
   ```
   Open `.env.local` and update these required variables

4. **Build and start services**:
   ```bash
   # First time setup
   make build
   
   # Start all services
   make up
   ```

5. **Verify installation**:
   ```bash
   # Check if all containers are running
   docker ps
   
   # Should show containers for:
   # - API
   # - PostgreSQL
   # - Redis
   # - RabbitMQ
   # - Worker
   ```

### Troubleshooting

- If services fail to start, check logs:
  ```bash
  make logs
  ```

- If port conflicts occur, modify these ports in `docker-compose.yml`:
  - API: 8000
  - PostgreSQL: 5432
  - Redis: 6379
  - RabbitMQ: 5672, 15672

### Development Setup

For local development without Docker:

1. **Create virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Run tests**:
   ```bash
   pytest
   ```

4. **Start development server**:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once running, access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication

- POST `/api/auth/register` - Register new user
- POST `/api/auth/token` - Login and get access token

### Recommendations

- GET `/api/recommendations/{recommendation_id}` - Get specific recommendation
- POST `/api/evaluate` - Generate new recommendation

## Development

### Project Structure

```
house-api/
├── app/
│   ├── api/
│   │   ├── endpoints/            # API endpoint handlers
│   │   │   ├── auth.py          # Authentication routes
│   │   │   ├── evaluate.py      # Evaluation routes
│   │   │   └── recommendations.py # Recommendation routes
│   ├── cache/
│   │   └── redis_manager.py     # Redis cache handling
│   ├── core/
│   │   ├── auth/
│   │   │   ├── jwt.py          # JWT operations
│   │   │   └── password.py     # Password hashing
│   │   └── config.py           # Environment settings
│   ├── db/
│   │   ├── base.py             # SQLAlchemy base class
│   │   └── session.py          # Database session
│   ├── messaging/
│   │   └── publisher.py        # RabbitMQ publisher
│   ├── models/
│   │   ├── recommendation.py   # Recommendation model
│   │   └── user.py            # User model
│   ├── schemas/
│   │   ├── recommendation.py   # Recommendation schemas
│   │   └── user.py            # User schemas
│   ├── services/
│   │   ├── base.py            # Base service class
│   │   ├── recommendation.py   # Recommendation service
│   │   └── user.py            # User service
│   └── main.py                # FastAPI application
├── tests/
│   ├── unit/
│   │   ├── test_auth.py       # Auth tests
│   │   ├── test_evaluate.py   # Evaluation tests
│   │   └── test_recommendations.py # Recommendation tests
│   └── conftest.py            # Test fixtures
├── .env.example               # Example environment variables
├── .flake8                    # Flake8 configuration
├── .gitignore                # Git ignore rules
├── Dockerfile                # API container definition
├── Makefile                  # Development commands
├── docker-compose.yml        # Service definitions
├── pyproject.toml            # Project configuration
└── requirements.txt          # Production dependencies
```

## Authors

Claudio Vagarinho