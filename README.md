# House API

A FastAPI-based clinical recommendations service with authentication, caching, and message queuing.

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

1. Clone the repository:
```bash
git clone https://github.com/cvagarinho/house-api.git
cd house-api
```

2. Create environment file:
```bash
cp .env.example .env.local
```

3. Build and start services:
```bash
make build
```

4. Start the application:
```bash
make up
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
│   │   ├── endpoints/     # API endpoint handlers
│   │   └── routes.py      # API router configuration
│   ├── cache/            # Redis cache management
│   ├── core/             # Core functionality
│   │   ├── auth/         # Authentication logic
│   │   └── config.py     # Settings management
│   ├── db/              # Database configuration
│   ├── messaging/       # RabbitMQ integration
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic models
│   └── services/       # Business logic
```

### Available Make Commands

- `make build` - Build all services
- `make up` - Start all services
- `make down` - Stop all services
- `make logs` - View logs
- `make rebuild-clean` - Rebuild from scratch


## Authors

Claudio Vagarinho