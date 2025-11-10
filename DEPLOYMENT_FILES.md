# Innovation Hub - Deployment Files Summary

Complete list of files created for OpenShift deployment with GitLab CI/CD and ArgoCD.

## 📁 File Structure

```
innovation-hub/
├── Dockerfile                      # OpenShift-compatible container image
├── .dockerignore                   # Docker build exclusions
├── .gitlab-ci.yml                  # GitLab CI/CD pipeline
├── setup-openshift.sh              # Interactive setup script
│
├── k8s/                            # Kubernetes manifests
│   ├── namespace.yaml              # Namespace definition
│   ├── configmap.yaml              # Environment configuration
│   ├── secret.yaml                 # API keys (template)
│   ├── pvc.yaml                    # Persistent volume claims
│   ├── deployment.yaml             # Application deployment
│   ├── service.yaml                # Kubernetes service
│   ├── route.yaml                  # OpenShift route (ingress)
│   └── kustomization.yaml          # Kustomize config
│
├── argocd/                         # ArgoCD GitOps
│   ├── application.yaml            # ArgoCD app definition
│   └── README.md                   # ArgoCD setup guide
│
└── docs/                           # Documentation
    ├── DEPLOYMENT.md               # Complete deployment guide
    ├── QUICKSTART.md               # Fast-track setup
    └── DEPLOYMENT_FILES.md         # This file
```

## 🐳 Container Configuration

### Dockerfile
**Purpose**: Build OpenShift-compatible container image
**Key Features**:
- Non-root user (UID 1001)
- Group permissions for OpenShift random UIDs
- Multi-stage build for smaller image
- Health check built-in
- Persistent data directories

**Base Image**: `python:3.11-slim`
**Exposed Port**: 8000
**Volumes**: `/app/data`, `/app/chroma_db`

### .dockerignore
**Purpose**: Exclude unnecessary files from Docker build
**Excludes**: Git files, venv, docs, IDE files, database files

## 🔄 CI/CD Pipeline

### .gitlab-ci.yml
**Stages**: test → build → deploy
**Features**:
- Run tests before building
- Build and push to GitLab Container Registry
- Update kustomization.yaml with new image tag
- Manual approval for production
- Direct OpenShift deployment option (commented out)
- ArgoCD GitOps integration

**Environment Variables Required**:
- `OPENSHIFT_SERVER`: Cluster API URL
- `OPENSHIFT_TOKEN`: Service account token
- `GITLAB_PUSH_TOKEN`: Token for git push
- `OPENROUTER_API_KEY`: AI service key
- `OPENAI_API_KEY`: Embeddings key

## ☸️ Kubernetes Manifests

### namespace.yaml
Creates `innovation-hub` namespace with labels

### configmap.yaml
**Non-sensitive configuration**:
- `HOST`: 0.0.0.0
- `PORT`: 8000
- `DEBUG`: False
- `DATABASE_URL`: sqlite:////app/data/innovation_hub.db
- `AI_MODEL`: qwen/qwen3-32b
- `OPENROUTER_BASE_URL`: https://openrouter.ai/api/v1

### secret.yaml
**Sensitive configuration** (template):
- `OPENROUTER_API_KEY`: AI service key
- `OPENAI_API_KEY`: Embeddings key

⚠️ **Do not commit real secrets!** Create manually or via CI/CD.

### pvc.yaml
**Persistent storage**:
1. `innovation-hub-data` (5Gi): SQLite database
2. `innovation-hub-chroma` (10Gi): ChromaDB vector database

**Access Mode**: ReadWriteOnce
**Storage Class**: Auto-provisioned by OpenShift

### deployment.yaml
**Container specification**:
- **Image**: registry.gitlab.com/your-group/innovation-hub:latest
- **Replicas**: 1 (scalable)
- **Strategy**: RollingUpdate
- **Resources**:
  - Requests: 512Mi RAM, 250m CPU
  - Limits: 2Gi RAM, 1000m CPU
- **Security**: Non-root, no privilege escalation
- **Volumes**: Mounted at /app/data and /app/chroma_db

**Health Checks**:
- **Liveness**: /api/health/live (every 10s)
- **Readiness**: /api/health/ready (every 5s)
- **Startup**: /api/health (every 10s, max 5min)

### service.yaml
**Service definition**:
- **Type**: ClusterIP
- **Port**: 8000
- **Protocol**: TCP
- **Selector**: app=innovation-hub

### route.yaml
**OpenShift route** (equivalent to Ingress):
- **Host**: innovation-hub.apps.your-cluster.com
- **TLS**: Edge termination
- **Redirect**: HTTP → HTTPS

### kustomization.yaml
**Kustomize configuration**:
- Manages all resources
- Common labels: app=innovation-hub, managed-by=argocd
- Image patching for GitOps

## 🔀 ArgoCD Configuration

### argocd/application.yaml
**GitOps application definition**:
- **Source**: GitLab repository
- **Path**: k8s/
- **Destination**: innovation-hub namespace
- **Sync Policy**: Automated (prune + self-heal)
- **Kustomize**: v5.0.0

**Features**:
- Auto-sync on git changes
- Auto-prune deleted resources
- Self-healing when drift detected
- Retry on failure (5 attempts)

### argocd/README.md
**Setup guide**:
- ArgoCD installation
- Repository configuration
- Application deployment
- Monitoring and troubleshooting

## 🛠️ Setup Script

### setup-openshift.sh
**Interactive setup wizard** that:
1. Validates prerequisites (oc CLI)
2. Prompts for configuration
3. Logs into OpenShift
4. Creates namespace and secrets
5. Updates all config files
6. Creates service account for CI/CD
7. Displays next steps

**Usage**:
```bash
chmod +x setup-openshift.sh
./setup-openshift.sh
```

## 📚 Documentation

### DEPLOYMENT.md (4,500+ words)
**Comprehensive guide** covering:
- Prerequisites and requirements
- Architecture diagram
- Step-by-step setup
- Configuration details
- Deployment procedures
- Monitoring and logging
- Troubleshooting (15+ scenarios)
- Security best practices
- Maintenance procedures

### QUICKSTART.md
**Fast-track guide** (5-minute setup):
- Prerequisites checklist
- Quick setup steps
- Essential commands
- Common issues with fixes
- Quick reference

### DEPLOYMENT_FILES.md
**This file** - Overview of all deployment files

## 🔐 Security Features

### Dockerfile Security
- ✅ Non-root user (UID 1001)
- ✅ No privilege escalation
- ✅ Minimal base image (slim)
- ✅ Drop all capabilities
- ✅ Group permissions for OpenShift

### Kubernetes Security
- ✅ Security contexts enforced
- ✅ Non-root enforcement
- ✅ Read-only root filesystem capable
- ✅ Resource limits set
- ✅ Network policies ready
- ✅ RBAC configured

### Secrets Management
- ✅ Secrets separate from config
- ✅ Not committed to git
- ✅ Injected via CI/CD variables
- ✅ Can use Sealed Secrets
- ✅ Can use External Secrets Operator

## 📊 Resource Requirements

### Minimum
- **CPU**: 250m (0.25 cores)
- **Memory**: 512Mi
- **Storage**: 15Gi (5Gi data + 10Gi vector DB)

### Recommended
- **CPU**: 500m-1000m
- **Memory**: 1-2Gi
- **Storage**: 25Gi (10Gi data + 15Gi vector DB)

### Production
- **Replicas**: 2-3 (with load balancing)
- **CPU**: 1000m-2000m per pod
- **Memory**: 2-4Gi per pod
- **Storage**: 50Gi+ (with backups)

## 🔄 Deployment Workflow

```
Developer        GitLab           ArgoCD          OpenShift
   │                │                │                │
   ├─ Push Code ──▶│                │                │
   │                ├─ Run Tests    │                │
   │                ├─ Build Image  │                │
   │                ├─ Push Image   │                │
   │                ├─ Update Tag ──┤                │
   │                │                ├─ Detect ──────┤
   │                │                ├─ Sync ────────┤
   │                │                │                ├─ Deploy
   │                │                │                ├─ Rolling Update
   │                │                │                ├─ Health Check
   │◀─── Success ──┴────────────────┴────────────────┤
```

## ✅ Checklist for Deployment

### Before Deployment
- [ ] OpenShift cluster access confirmed
- [ ] GitLab CI/CD enabled
- [ ] API keys obtained (OpenRouter, OpenAI)
- [ ] Domain name configured
- [ ] Storage provisioner available

### Configuration
- [ ] Updated k8s/deployment.yaml with image name
- [ ] Updated k8s/route.yaml with domain
- [ ] Updated k8s/kustomization.yaml with image name
- [ ] Updated .gitlab-ci.yml with image name
- [ ] Updated argocd/application.yaml with repo URL

### GitLab Setup
- [ ] OPENSHIFT_SERVER variable set
- [ ] OPENSHIFT_TOKEN variable set
- [ ] GITLAB_PUSH_TOKEN variable set
- [ ] OPENROUTER_API_KEY variable set (optional)
- [ ] OPENAI_API_KEY variable set (optional)

### OpenShift Setup
- [ ] Namespace created
- [ ] Registry secret created
- [ ] Application secrets created
- [ ] PVCs created
- [ ] Service account created for CI/CD

### ArgoCD Setup (Optional)
- [ ] ArgoCD installed
- [ ] Repository added to ArgoCD
- [ ] Application created
- [ ] Auto-sync configured

### Testing
- [ ] Health endpoint responds
- [ ] Database persists data
- [ ] Frontend loads correctly
- [ ] API documentation accessible
- [ ] Logs show no errors

## 🎯 Quick Commands Reference

```bash
# Deploy
oc apply -k k8s/

# Check status
oc get all -n innovation-hub

# View logs
oc logs -f deployment/innovation-hub -n innovation-hub

# Restart
oc rollout restart deployment/innovation-hub -n innovation-hub

# Scale
oc scale deployment/innovation-hub --replicas=3 -n innovation-hub

# Update secrets
oc create secret generic innovation-hub-secrets --dry-run=client -o yaml \
  --from-literal=OPENROUTER_API_KEY=xxx | oc apply -f -

# Port forward for testing
oc port-forward deployment/innovation-hub 8000:8000 -n innovation-hub

# Access database
oc rsh deployment/innovation-hub
sqlite3 /app/data/innovation_hub.db

# Backup
oc rsync deployment/innovation-hub:/app/data ./backup/ -n innovation-hub

# Monitor resources
oc adm top pod -n innovation-hub
```

## 📞 Support Resources

- **Full Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Quick Setup**: [QUICKSTART.md](QUICKSTART.md)
- **ArgoCD Setup**: [argocd/README.md](argocd/README.md)
- **Application Docs**: [README.md](README.md)

## 🔄 Updates and Maintenance

### To Update Application
```bash
git commit -am "Update feature X"
git push origin main
# CI/CD + ArgoCD handles the rest
```

### To Update Configuration
```bash
# Edit k8s/configmap.yaml or k8s/secret.yaml
oc apply -k k8s/
oc rollout restart deployment/innovation-hub -n innovation-hub
```

### To Update Secrets
```bash
oc delete secret innovation-hub-secrets -n innovation-hub
oc create secret generic innovation-hub-secrets \
  --from-literal=OPENROUTER_API_KEY=new-key \
  --from-literal=OPENAI_API_KEY=new-key \
  -n innovation-hub
oc rollout restart deployment/innovation-hub -n innovation-hub
```

---

**Created**: 2025-10-27
**Version**: 1.0.0
**Status**: Production Ready ✅
