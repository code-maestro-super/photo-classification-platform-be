# Submission Service

Photo submission and metadata service.

## Setup

```bash
pip install -r requirements.txt
cp env.example .env
alembic upgrade head
uvicorn app.main:app --reload --port 8002
```

## Endpoints

- `POST /api/v1/submissions` - Create submission (photo + metadata)
- `GET /api/v1/submissions/{id}` - Get submission
- `GET /api/v1/submissions` - List user submissions
- `GET /docs` - API docs

