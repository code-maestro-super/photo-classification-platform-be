# Architecture Overview

## System Architecture

The Photo Classification Platform is built using a microservices architecture with four independent services communicating via HTTP/REST APIs.

## Microservices

### 1. User Service
- **Port**: 8001
- **Responsibilities**: User authentication, registration, JWT token management
- **Database**: PostgreSQL (users table)
- **Endpoints**: `/api/v1/auth/*`

### 2. Submission Service
- **Port**: 8002
- **Responsibilities**: Photo uploads, metadata storage, classification requests
- **Database**: PostgreSQL (submissions table)
- **File Storage**: Local filesystem (Docker volumes)
- **Endpoints**: `/api/v1/submissions/*`
- **Dependencies**: Classification Service

### 3. Classification Service
- **Port**: 8003
- **Responsibilities**: Image classification processing
- **Endpoints**: `/api/v1/classify`
- **Dependencies**: None

### 4. Admin Service
- **Port**: 8004
- **Responsibilities**: Admin panel, filtering, search
- **Database**: PostgreSQL (submissions table - read-only)
- **Endpoints**: `/api/v1/admin/*`
- **Dependencies**: User Service (for admin role validation)

## Data Flow

```
User Request
    ↓
Nginx (API Gateway)
    ↓
┌─────────────────────────────────────┐
│  User Service                       │
│  - Register/Login                   │
│  - JWT Token Generation             │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Submission Service                 │
│  - Photo Upload                     │
│  - Metadata Storage                 │
│  - Classification Request           │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Classification Service             │
│  - Image Processing                 │
│  - Classification Result            │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Admin Service                      │
│  - Filter & Search                  │
│  - View Submissions                 │
└─────────────────────────────────────┘
```

## Communication Patterns

### Service-to-Service Communication
- **Protocol**: HTTP/REST
- **Method**: Async HTTP calls (httpx)
- **Authentication**: JWT tokens passed in Authorization header
- **Service Discovery**: Docker service names / Kubernetes DNS

### Database Access
- **Shared Database**: PostgreSQL
- **Schema**: Separate tables per service
- **Migrations**: Alembic per service

## Deployment Architecture

### Docker Compose (Development)
```
┌─────────────┐
│   Nginx     │ (Port 80)
└──────┬──────┘
       │
   ┌───┴───┬──────────┬──────────────┬──────────┐
   │       │          │              │          │
┌──▼──┐ ┌──▼──┐   ┌──▼──┐       ┌──▼──┐   ┌──▼──┐
│User │ │Sub  │   │Class│       │Admin│   │Post │
│     │ │     │   │     │       │     │   │gres │
└─────┘ └─────┘   └─────┘       └─────┘   └─────┘
```

### Kubernetes (Production)
- **Namespace**: photo-classification
- **Deployments**: 2 replicas per service
- **Services**: ClusterIP for internal communication
- **Ingress**: Nginx Ingress Controller
- **Storage**: PersistentVolumes for database and uploads
- **ConfigMap**: Non-sensitive configuration
- **Secrets**: Sensitive data (passwords, keys)

## Security

- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control (user/admin)
- File upload validation
- Input sanitization
- CORS configuration

## Scalability

- Horizontal scaling via Kubernetes replicas
- Stateless services (except database)
- Load balancing via Nginx
- Resource limits and requests configured

