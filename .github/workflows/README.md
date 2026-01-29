# CI/CD Pipeline

GitHub Actions workflow for continuous integration and deployment.

## Workflow Jobs

### 1. Lint
- Runs flake8 for code quality checks
- Runs black for code formatting validation
- Runs on all services

### 2. Test
- Sets up PostgreSQL test database
- Installs dependencies for all services
- Runs pytest tests (if tests exist)
- Generates coverage reports

### 3. Build
- Builds Docker images for all services
- Pushes to GitHub Container Registry
- Tags images with branch name and commit SHA
- Uses Docker layer caching

### 4. Deploy
- Deploys to Kubernetes (main branch only)
- Updates image tags in deployment manifests
- Applies all Kubernetes resources
- Waits for rollout completion

## Setup

1. **Container Registry**: Uses GitHub Container Registry (ghcr.io)
   - Images: `ghcr.io/OWNER/REPO/service-name`

2. **Secrets Required**:
   - `KUBECONFIG`: Base64 encoded kubeconfig file (for deployment)

3. **Environment Variables**:
   - Set in repository settings or workflow file

## Manual Deployment

If automatic deployment is disabled:

```bash
# Build and push images
docker build -t ghcr.io/OWNER/REPO/user-service:latest ./services/user-service
docker push ghcr.io/OWNER/REPO/user-service:latest

# Update Kubernetes manifests with new image tags
# Apply manifests
kubectl apply -f infrastructure/kubernetes/
```

## Workflow Triggers

- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Deployment only runs on `main` branch pushes

