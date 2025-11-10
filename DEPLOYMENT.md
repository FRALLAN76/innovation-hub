# Innovation Hub - OpenShift Deployment Guide

Complete guide for deploying Innovation Hub to OpenShift using GitLab CI/CD and ArgoCD.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Architecture](#architecture)
3. [Setup Steps](#setup-steps)
4. [Configuration](#configuration)
5. [Deployment](#deployment)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Tools

- OpenShift CLI (`oc`) - version 4.x
- GitLab account with CI/CD enabled
- ArgoCD installed on OpenShift cluster
- Docker (for local testing)
- Access to OpenShift cluster with appropriate permissions

### Required Access

- OpenShift cluster admin or namespace admin privileges
- GitLab project with maintainer/owner role
- GitLab Container Registry enabled
- API keys for:
  - OpenRouter API (for AI analysis)
  - OpenAI API (for embeddings)

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   GitLab    │─────▶│  GitLab CI   │─────▶│  Container  │
│  Repository │      │    Pipeline  │      │  Registry   │
└─────────────┘      └──────────────┘      └─────────────┘
                            │                      │
                            ▼                      │
                     ┌──────────────┐              │
                     │  Update      │              │
                     │  k8s/        │              │
                     │  kustomize   │              │
                     └──────────────┘              │
                            │                      │
                            ▼                      │
                     ┌──────────────┐              │
                     │   ArgoCD     │◀─────────────┘
                     │   Detects    │
                     │   Changes    │
                     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  OpenShift   │
                     │   Cluster    │
                     └──────────────┘
```

### Components

- **FastAPI Backend**: Runs on port 8000
- **SQLite Database**: Stored in PersistentVolume (`/app/data`)
- **ChromaDB**: Vector database stored in PersistentVolume (`/app/chroma_db`)
- **Static Frontend**: Served by FastAPI

## Setup Steps

### 1. Prepare GitLab Repository

```bash
# Clone your repository
git clone https://gitlab.com/your-group/innovation-hub.git
cd innovation-hub

# Copy all deployment files (already created)
# - Dockerfile
# - .gitlab-ci.yml
# - k8s/
# - argocd/
```

### 2. Configure GitLab CI/CD Variables

Go to GitLab Project → Settings → CI/CD → Variables

Add the following variables:

| Variable | Value | Protected | Masked |
|----------|-------|-----------|--------|
| `OPENSHIFT_SERVER` | https://api.your-cluster.com:6443 | ✓ | ✗ |
| `OPENSHIFT_TOKEN` | <service-account-token> | ✓ | ✓ |
| `GITLAB_PUSH_TOKEN` | <gitlab-personal-access-token> | ✓ | ✓ |
| `OPENROUTER_API_KEY` | <your-openrouter-key> | ✓ | ✓ |
| `OPENAI_API_KEY` | <your-openai-key> | ✓ | ✓ |

#### How to get OPENSHIFT_TOKEN:

```bash
# Create service account for GitLab CI
oc create serviceaccount gitlab-ci -n innovation-hub

# Grant permissions
oc policy add-role-to-user admin system:serviceaccount:innovation-hub:gitlab-ci -n innovation-hub

# Get token
oc serviceaccounts get-token gitlab-ci -n innovation-hub
```

#### How to create GITLAB_PUSH_TOKEN:

1. Go to GitLab → User Settings → Access Tokens
2. Create token with `api`, `write_repository` scopes
3. Copy token and add to CI/CD variables

### 3. Update Configuration Files

#### Update `.gitlab-ci.yml`

```yaml
# Change image name
variables:
  IMAGE_NAME: registry.gitlab.com/your-group/innovation-hub
```

#### Update `k8s/kustomization.yaml`

```yaml
images:
  - name: innovation-hub
    newName: registry.gitlab.com/your-group/innovation-hub
    newTag: latest
```

#### Update `k8s/route.yaml`

```yaml
spec:
  host: innovation-hub.apps.your-cluster.example.com
```

#### Update `k8s/deployment.yaml`

```yaml
containers:
- name: innovation-hub
  image: registry.gitlab.com/your-group/innovation-hub:latest
```

### 4. Create Secrets in OpenShift

```bash
# Login to OpenShift
oc login --token=<your-token> --server=https://api.your-cluster.com:6443

# Create namespace
oc create namespace innovation-hub

# Create GitLab registry credentials
oc create secret docker-registry gitlab-registry \
  --docker-server=registry.gitlab.com \
  --docker-username=<your-gitlab-username> \
  --docker-password=<your-gitlab-token> \
  --docker-email=<your-email> \
  -n innovation-hub

# Create API secrets
oc create secret generic innovation-hub-secrets \
  --from-literal=OPENROUTER_API_KEY=<your-key> \
  --from-literal=OPENAI_API_KEY=<your-key> \
  -n innovation-hub
```

### 5. Setup ArgoCD

```bash
# Install ArgoCD (if not already installed)
oc create namespace argocd
oc apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Get initial admin password
oc get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d

# Access ArgoCD UI
oc port-forward svc/argocd-server -n argocd 8080:443
# Open: https://localhost:8080
# Username: admin
# Password: <from above>

# Add GitLab repository to ArgoCD
argocd repo add https://gitlab.com/your-group/innovation-hub.git \
  --username <gitlab-username> \
  --password <gitlab-token>

# Create ArgoCD application
oc apply -f argocd/application.yaml
```

## Configuration

### Environment Variables

All environment variables are defined in `k8s/configmap.yaml` and `k8s/secret.yaml`.

#### ConfigMap (Non-sensitive)

```yaml
HOST: "0.0.0.0"
PORT: "8000"
DEBUG: "False"
DATABASE_URL: "sqlite:////app/data/innovation_hub.db"
AI_MODEL: "qwen/qwen3-32b"
OPENROUTER_BASE_URL: "https://openrouter.ai/api/v1"
```

#### Secrets (Sensitive)

```yaml
OPENROUTER_API_KEY: "<your-key>"
OPENAI_API_KEY: "<your-key>"
```

### Persistent Volumes

Two PVCs are created automatically:

1. **innovation-hub-data** (5Gi): SQLite database
2. **innovation-hub-chroma** (10Gi): ChromaDB vector database

Both use `ReadWriteOnce` access mode.

### Resource Limits

Default resource allocation per pod:

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "2Gi"
    cpu: "1000m"
```

Adjust in `k8s/deployment.yaml` if needed.

## Deployment

### Initial Deployment

```bash
# Commit and push changes
git add .
git commit -m "Initial OpenShift deployment setup"
git push origin main

# GitLab CI will automatically:
# 1. Run tests
# 2. Build Docker image
# 3. Push to GitLab Container Registry
# 4. Update kustomization.yaml with new image tag

# ArgoCD will automatically:
# 1. Detect changes in git
# 2. Apply manifests to OpenShift
# 3. Perform rolling update
```

### Manual Deployment (Without ArgoCD)

```bash
# Apply manifests directly
oc apply -k k8s/

# Check deployment status
oc get all -n innovation-hub

# Check logs
oc logs -f deployment/innovation-hub -n innovation-hub

# Get route URL
oc get route innovation-hub -n innovation-hub -o jsonpath='{.spec.host}'
```

### Triggering New Deployment

Any push to `main` branch will trigger:

1. Build new Docker image
2. Update image tag in kustomization.yaml
3. ArgoCD syncs changes to cluster

```bash
# Make changes to code
git add .
git commit -m "Update feature X"
git push origin main

# Monitor deployment
oc rollout status deployment/innovation-hub -n innovation-hub
```

## Monitoring

### Health Checks

The application provides three health endpoints:

1. **Liveness**: `/api/health/live` - Is the app alive?
2. **Readiness**: `/api/health/ready` - Is the app ready to serve traffic?
3. **Startup**: `/api/health` - Basic health check with database connectivity

```bash
# Test health endpoints
curl https://innovation-hub.apps.your-cluster.com/api/health
curl https://innovation-hub.apps.your-cluster.com/api/health/ready
curl https://innovation-hub.apps.your-cluster.com/api/health/live
```

### View Logs

```bash
# Stream logs
oc logs -f deployment/innovation-hub -n innovation-hub

# View last 100 lines
oc logs deployment/innovation-hub -n innovation-hub --tail=100

# View previous container logs (after crash)
oc logs deployment/innovation-hub -n innovation-hub --previous
```

### Check Resources

```bash
# Pod status
oc get pods -n innovation-hub

# Deployment status
oc get deployment innovation-hub -n innovation-hub

# Service and route
oc get svc,route -n innovation-hub

# PVC status
oc get pvc -n innovation-hub

# Events
oc get events -n innovation-hub --sort-by='.lastTimestamp'
```

### ArgoCD Monitoring

```bash
# Application status
argocd app get innovation-hub

# Sync status
argocd app sync innovation-hub --dry-run

# View history
argocd app history innovation-hub

# Watch for changes
argocd app wait innovation-hub --health
```

## Troubleshooting

### Pod Not Starting

```bash
# Check pod status
oc describe pod <pod-name> -n innovation-hub

# Common issues:
# 1. Image pull errors → Check registry credentials
# 2. CrashLoopBackOff → Check logs and health checks
# 3. Pending → Check PVC binding
```

### Image Pull Errors

```bash
# Verify secret exists
oc get secret gitlab-registry -n innovation-hub

# Recreate secret
oc delete secret gitlab-registry -n innovation-hub
oc create secret docker-registry gitlab-registry \
  --docker-server=registry.gitlab.com \
  --docker-username=<username> \
  --docker-password=<token> \
  -n innovation-hub

# Ensure pod uses secret
oc set sa deployment/innovation-hub default -n innovation-hub
oc secrets link default gitlab-registry --for=pull -n innovation-hub
```

### Database Issues

```bash
# Check PVC
oc get pvc innovation-hub-data -n innovation-hub

# Check volume mount
oc describe pod <pod-name> -n innovation-hub | grep -A5 "Mounts:"

# Access pod and check database
oc rsh deployment/innovation-hub
ls -la /app/data/
sqlite3 /app/data/innovation_hub.db ".tables"
```

### ArgoCD Out of Sync

```bash
# Check diff
argocd app diff innovation-hub

# Force sync
argocd app sync innovation-hub --force --prune

# Refresh cache
argocd app get innovation-hub --refresh
```

### Health Check Failures

```bash
# Test endpoints manually
oc port-forward deployment/innovation-hub 8000:8000 -n innovation-hub
curl http://localhost:8000/api/health
curl http://localhost:8000/api/health/ready

# Adjust probe timings in deployment.yaml if needed
```

### Performance Issues

```bash
# Check resource usage
oc adm top pod -n innovation-hub

# Increase resources in deployment.yaml
resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "4Gi"
    cpu: "2000m"
```

### Rollback

```bash
# Via ArgoCD
argocd app rollback innovation-hub

# Via OpenShift
oc rollout undo deployment/innovation-hub -n innovation-hub

# To specific revision
oc rollout undo deployment/innovation-hub --to-revision=2 -n innovation-hub
```

## Security Best Practices

1. **Never commit secrets** to git
2. **Use sealed-secrets** or External Secrets Operator for production
3. **Rotate API keys** regularly
4. **Enable RBAC** for namespace isolation
5. **Use NetworkPolicies** to restrict traffic
6. **Enable audit logging** for compliance
7. **Regular security scans** of container images

## Maintenance

### Backup Database

```bash
# Copy database from pod
oc rsync deployment/innovation-hub:/app/data/innovation_hub.db ./backup/ -n innovation-hub

# Or create a CronJob for automated backups
```

### Update Application

```bash
# Just commit and push - CI/CD handles the rest
git commit -am "Update to version X"
git push origin main
```

### Scale Application

```bash
# Scale to 3 replicas
oc scale deployment/innovation-hub --replicas=3 -n innovation-hub

# Or update deployment.yaml and commit
```

### Update Secrets

```bash
# Delete old secret
oc delete secret innovation-hub-secrets -n innovation-hub

# Create new secret
oc create secret generic innovation-hub-secrets \
  --from-literal=OPENROUTER_API_KEY=<new-key> \
  --from-literal=OPENAI_API_KEY=<new-key> \
  -n innovation-hub

# Restart pods to use new secret
oc rollout restart deployment/innovation-hub -n innovation-hub
```

## Contact & Support

For issues or questions:
- Check logs first
- Review health endpoints
- Consult ArgoCD UI
- Check GitLab CI/CD pipeline logs

---

**Last Updated**: 2025-10-27
**Version**: 1.0.0
