# Briefly

An AI-powered note-taking and summarization API built with Django REST Framework. Users can create notes, organize them into collections, and request AI-generated summaries powered by Groq's LLaMA model.

## Tech Stack

- **Backend:** Django 6, Django REST Framework
- **Database:** PostgreSQL
- **Cache/Broker:** Redis
- **Task Queue:** Celery
- **AI:** Groq API (LLaMA 3.3 70B)
- **Auth:** JWT (SimpleJWT)
- **Docs:** drf-spectacular (Swagger UI)
- **Infrastructure:** Docker, docker-compose

## Features

- Multi-user API with JWT authentication
- Create and organize notes into collections
- AI summarization of individual notes via background tasks
- AI summarization of entire collections
- Filtering, searching, and ordering on list endpoints
- Auto-generated interactive API documentation
- Full test suite with mocked external services

## Local Development

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Clone the repository

```bash
   git clone https://github.com/yourusername/briefly.git
   cd briefly
```

2. Create a `.env` file in the project root

```bash
   cp .env.example .env
```

   Then fill in the values in `.env`.

3. Build and start the containers

```bash
   docker-compose up --build
```

4. Run migrations

```bash
   docker-compose exec web python manage.py migrate
```

5. Create a superuser

```bash
   docker-compose exec web python manage.py createsuperuser
```

6. Visit `http://localhost:8000/api/docs/` to explore the API

### Running Tests

```bash
docker-compose exec web pytest -v
```

## API Overview

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/token/` | Obtain access and refresh tokens |
| POST | `/api/token/refresh/` | Refresh access token |

### Notes

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/notes/` | List all your notes |
| POST | `/api/notes/` | Create a note |
| GET | `/api/notes/{id}/` | Retrieve a note |
| PATCH | `/api/notes/{id}/` | Update a note |
| DELETE | `/api/notes/{id}/` | Delete a note |

### Collections

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/collections/` | List all your collections |
| POST | `/api/collections/` | Create a collection |
| GET | `/api/collections/{id}/` | Retrieve a collection |
| PATCH | `/api/collections/{id}/` | Update a collection |
| DELETE | `/api/collections/{id}/` | Delete a collection |
| POST | `/api/collections/{id}/summarize/` | Trigger AI summarization |

### Filtering

Notes support filtering, searching, and ordering:
GET /api/notes/?summary_status=completed
GET /api/notes/?search=meeting
GET /api/notes/?ordering=-created_at
GET /api/notes/?collection=1

## Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Debug mode (True/False) |
| `DATABASE_URL` | Postgres connection string |
| `REDIS_URL` | Redis connection string |
| `GROQ_API_KEY` | Groq API key |

## License

MIT