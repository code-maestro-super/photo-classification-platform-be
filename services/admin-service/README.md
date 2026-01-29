# Admin Service

Admin panel API service.

## Setup

```bash
pip install -r requirements.txt
cp env.example .env
uvicorn app.main:app --reload --port 8004
```

## Endpoints

- `GET /api/v1/admin/submissions` - List submissions with filters
- `GET /api/v1/admin/submissions/{id}` - Get submission details
- `GET /docs` - API docs

## Query Parameters

- `age` - Filter by age
- `gender` - Filter by gender
- `location` - Filter by place of living
- `country` - Filter by country
- `date_from` - Filter from date (ISO format)
- `date_to` - Filter to date (ISO format)
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 100, max: 1000)
- `sort_by` - Sort field (default: created_at)
- `sort_order` - asc or desc (default: desc)

