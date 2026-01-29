# Photo Classification Platform

Microservices-based platform for photo classification with user submissions and admin management.

## Architecture

The platform consists of four microservices:

- **User Service** (Port 8001) - Authentication, registration, user management
- **Submission Service** (Port 8002) - Photo uploads, metadata submission, classification requests
- **Classification Service** (Port 8003) - Image classification processing
- **Admin Service** (Port 8004) - Admin panel with filtering and search

## Tech Stack

- **Backend**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15
- **File Storage**: Local filesystem (with Docker volumes)
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes
- **API Gateway**: Nginx
- **CI/CD**: GitHub Actions

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 14+ (or use Docker)
- Docker and Docker Compose (optional)

### Local Development

1. Clone repository:
```bash
git clone <repository-url>
cd photo-classification-platform-be
```

2. Set up environment:
```bash
cp env.example .env
# Edit .env with your configuration
```

3. Set up each service:
```bash
cd services/user-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
# Edit .env
alembic upgrade head
uvicorn app.main:app --reload --port 8001
```

Repeat for other services on ports 8002, 8003, 8004.

### Docker Setup

1. Build and start all services:
```bash
docker-compose up -d
```

2. Run database migrations:
```bash
docker-compose exec user-service alembic upgrade head
docker-compose exec submission-service alembic upgrade head
```

3. Access services:
- API Gateway: http://localhost
- User Service: http://localhost:8001
- Submission Service: http://localhost:8002
- Classification Service: http://localhost:8003
- Admin Service: http://localhost:8004

### Kubernetes Deployment

See [infrastructure/kubernetes/README.md](infrastructure/kubernetes/README.md) for deployment instructions.

## API Documentation

Once services are running, interactive API documentation is available:

- User Service: http://localhost:8001/docs
- Submission Service: http://localhost:8002/docs
- Classification Service: http://localhost:8003/docs
- Admin Service: http://localhost:8004/docs

## Database Migrations

### User Service
```bash
cd services/user-service
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1  # rollback
```

### Submission Service
```bash
cd services/submission-service
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Testing

Run tests:
```bash
pip install -r requirements-dev.txt
pytest
pytest --cov=services --cov-report=html
```

## Project Structure

```
photo-classification-platform-be/
├── services/
│   ├── user-service/
│   ├── submission-service/
│   ├── classification-service/
│   └── admin-service/
├── infrastructure/
│   ├── docker/
│   ├── kubernetes/
│   └── nginx/
├── tests/
│   └── integration/
├── .github/
│   └── workflows/
├── docs/
├── docker-compose.yml
└── README.md
```

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running
- Check DATABASE_URL in .env files
- Ensure database exists

### Service Communication Issues
- Verify all services are running
- Check service URLs in environment variables
- Review Docker network configuration

### File Upload Issues
- Check UPLOAD_DIR permissions
- Verify MAX_FILE_SIZE setting
- Ensure sufficient disk space

## License

See [LICENSE](LICENSE) file.
