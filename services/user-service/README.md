# User Service

Authentication service.

## Setup

```bash
pip install -r requirements.txt
cp env.example .env
alembic upgrade head
uvicorn app.main:app --reload --port 8001
```

## Endpoints

- `POST /api/v1/auth/register` - Register
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Get current user
- `GET /docs` - API docs
