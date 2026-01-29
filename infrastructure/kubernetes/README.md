# Kubernetes Deployment

Kubernetes deployment configurations for photo classification platform.

## Prerequisites

- Kubernetes cluster (v1.24+)
- kubectl configured
- Docker images built and pushed to registry
- Ingress controller installed (nginx-ingress)

## Deployment Steps

1. Create namespace:
```bash
kubectl apply -f namespace.yaml
```

2. Create secrets (update values first):
```bash
cp secrets.yaml.example secrets.yaml
# Edit secrets.yaml with your values
kubectl apply -f secrets.yaml
```

3. Create ConfigMap:
```bash
kubectl apply -f configmap.yaml
```

4. Deploy PostgreSQL:
```bash
kubectl apply -f postgres-statefulset.yaml
```

5. Deploy services:
```bash
kubectl apply -f user-service-deployment.yaml
kubectl apply -f submission-service-deployment.yaml
kubectl apply -f classification-service-deployment.yaml
kubectl apply -f admin-service-deployment.yaml
```

6. Deploy Ingress:
```bash
kubectl apply -f ingress.yaml
```

## Scaling

Scale services:
```bash
kubectl scale deployment user-service --replicas=3 -n photo-classification
```

## Secrets Management

Update secrets:
```bash
kubectl edit secret app-secrets -n photo-classification
```

## Observability

View logs:
```bash
kubectl logs -f deployment/user-service -n photo-classification
```

Check pod status:
```bash
kubectl get pods -n photo-classification
```

## Database Migrations

Run migrations manually:
```bash
kubectl exec -it deployment/user-service -n photo-classification -- alembic upgrade head
```

## Notes

- Update image tags in deployments before applying
- Configure ingress hostname for your domain
- Adjust resource limits based on workload
- Use external secret management in production

