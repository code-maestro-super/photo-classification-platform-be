# Classification Service

Image classification service.

## Setup

```bash
pip install -r requirements.txt
cp env.example .env
uvicorn app.main:app --reload --port 8003
```

## Endpoints

- `POST /api/v1/classify` - Classify image
- `GET /health` - Health check
- `GET /docs` - API docs

