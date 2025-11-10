# ArgoCD Deployment

This directory contains the ArgoCD Application manifest for deploying Innovation Hub.

## Prerequisites

1. ArgoCD must be installed in your OpenShift cluster
2. GitLab repository must be accessible from ArgoCD
3. Configure ArgoCD credentials for GitLab (if private repo)

## Setup ArgoCD

### 1. Install ArgoCD (if not already installed)

```bash
# Create ArgoCD namespace
oc create namespace argocd

# Install ArgoCD
oc apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Get ArgoCD admin password
oc get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d

# Access ArgoCD UI
oc port-forward svc/argocd-server -n argocd 8080:443
# Open: https://localhost:8080
# Username: admin
# Password: <from above command>
```

### 2. Configure GitLab Repository Access

If your repository is private, add credentials to ArgoCD:

```bash
# Using HTTPS with token
argocd repo add https://gitlab.com/your-group/innovation-hub.git \
  --username gitlab-token \
  --password <YOUR_GITLAB_TOKEN>

# Or using SSH
argocd repo add git@gitlab.com:your-group/innovation-hub.git \
  --ssh-private-key-path ~/.ssh/id_rsa
```

### 3. Deploy Application

```bash
# Apply the ArgoCD application
oc apply -f argocd/application.yaml

# Or using argocd CLI
argocd app create innovation-hub \
  --repo https://gitlab.com/your-group/innovation-hub.git \
  --path k8s \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace innovation-hub \
  --sync-policy automated \
  --auto-prune \
  --self-heal

# Sync the application
argocd app sync innovation-hub

# Check application status
argocd app get innovation-hub
```

## GitOps Workflow

1. **Developer pushes code** to GitLab
2. **GitLab CI/CD** builds Docker image and pushes to registry
3. **GitLab CI/CD** updates `k8s/kustomization.yaml` with new image tag
4. **ArgoCD** detects change in git and syncs to OpenShift
5. **OpenShift** performs rolling update to new version

## Manual Sync

If automated sync is disabled:

```bash
# Sync via CLI
argocd app sync innovation-hub

# Or via UI
# Go to ArgoCD UI → Select application → Click "Sync"
```

## Monitoring

```bash
# Watch application status
argocd app get innovation-hub --watch

# View sync history
argocd app history innovation-hub

# View logs
oc logs -f deployment/innovation-hub -n innovation-hub
```

## Rollback

```bash
# Rollback to previous version
argocd app rollback innovation-hub

# Or rollback to specific revision
argocd app rollback innovation-hub <revision-number>
```

## Troubleshooting

### Application Out of Sync

```bash
# Check diff between git and cluster
argocd app diff innovation-hub

# Force sync
argocd app sync innovation-hub --force
```

### Application Unhealthy

```bash
# Check pod status
oc get pods -n innovation-hub

# Check pod logs
oc logs -l app=innovation-hub -n innovation-hub

# Check events
oc get events -n innovation-hub --sort-by='.lastTimestamp'
```

### Image Pull Errors

```bash
# Create GitLab registry secret
oc create secret docker-registry gitlab-registry \
  --docker-server=registry.gitlab.com \
  --docker-username=<your-gitlab-username> \
  --docker-password=<your-gitlab-token> \
  --docker-email=<your-email> \
  -n innovation-hub

# Link secret to service account
oc secrets link default gitlab-registry --for=pull -n innovation-hub
```
