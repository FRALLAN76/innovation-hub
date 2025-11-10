# Innovation Hub - OpenShift Deployment Quickstart

Fast-track guide to deploy Innovation Hub on OpenShift with GitLab CI/CD.

## 🚀 5-Minute Setup

### Prerequisites
- OpenShift cluster access
- GitLab account with CI/CD enabled
- API keys (OpenRouter, OpenAI)

### Step 1: Run Setup Script

```bash
# Make script executable (if not already)
chmod +x setup-openshift.sh

# Run interactive setup
./setup-openshift.sh
```

The script will:
- ✅ Configure OpenShift namespace
- ✅ Create image pull secrets
- ✅ Create API key secrets
- ✅ Update all configuration files
- ✅ Create service account for CI/CD

### Step 2: Configure GitLab CI/CD

Go to: **GitLab Project → Settings → CI/CD → Variables**

Add these variables (from setup script output):

```
OPENSHIFT_SERVER = https://api.your-cluster.com:6443
OPENSHIFT_TOKEN = <token-from-setup-script>
GITLAB_PUSH_TOKEN = <your-gitlab-personal-access-token>
```

### Step 3: Deploy

```bash
# Commit changes
git add .
git commit -m "Configure OpenShift deployment"
git push origin main

# Apply to OpenShift
oc apply -k k8s/

# Check status
oc get pods -n innovation-hub
```

### Step 4: Access Application

```bash
# Get route URL
oc get route innovation-hub -n innovation-hub -o jsonpath='{.spec.host}'

# Open in browser
https://innovation-hub.apps.your-cluster.com
```

## 🔍 Verify Deployment

```bash
# Check all resources
oc get all -n innovation-hub

# Check health
curl https://your-app-url/api/health

# View logs
oc logs -f deployment/innovation-hub -n innovation-hub
```

## 🔄 GitOps with ArgoCD (Optional)

```bash
# Install ArgoCD (if not installed)
oc create namespace argocd
oc apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Deploy application via ArgoCD
oc apply -f argocd/application.yaml

# Get ArgoCD password
oc get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d

# Access ArgoCD UI
oc port-forward svc/argocd-server -n argocd 8080:443
# Open: https://localhost:8080
# Login: admin / <password-from-above>
```

## 📝 Quick Commands

### View Logs
```bash
oc logs -f deployment/innovation-hub -n innovation-hub
```

### Restart Application
```bash
oc rollout restart deployment/innovation-hub -n innovation-hub
```

### Scale Application
```bash
oc scale deployment/innovation-hub --replicas=3 -n innovation-hub
```

### Update Secrets
```bash
oc delete secret innovation-hub-secrets -n innovation-hub
oc create secret generic innovation-hub-secrets \
  --from-literal=OPENROUTER_API_KEY=<new-key> \
  --from-literal=OPENAI_API_KEY=<new-key> \
  -n innovation-hub
oc rollout restart deployment/innovation-hub -n innovation-hub
```

### Backup Database
```bash
oc rsync deployment/innovation-hub:/app/data ./backup/ -n innovation-hub
```

### Check Resource Usage
```bash
oc adm top pod -n innovation-hub
```

## 🐛 Common Issues

### Pod Not Starting
```bash
oc describe pod <pod-name> -n innovation-hub
oc logs <pod-name> -n innovation-hub
```

### Image Pull Error
```bash
# Recreate registry secret
oc delete secret gitlab-registry -n innovation-hub
oc create secret docker-registry gitlab-registry \
  --docker-server=registry.gitlab.com \
  --docker-username=<username> \
  --docker-password=<token> \
  -n innovation-hub
oc secrets link default gitlab-registry --for=pull -n innovation-hub
```

### Database Issues
```bash
# Check PVC
oc get pvc -n innovation-hub

# Access pod shell
oc rsh deployment/innovation-hub
ls -la /app/data/
```

## 📚 Full Documentation

For detailed information, see:
- [DEPLOYMENT.md](DEPLOYMENT.md) - Complete deployment guide
- [argocd/README.md](argocd/README.md) - ArgoCD setup
- [README.md](README.md) - Application documentation

## 🔐 Security Notes

⚠️ **Never commit secrets to git!**
⚠️ Always use GitLab CI/CD variables for sensitive data
⚠️ Rotate API keys regularly
⚠️ Enable RBAC for production environments

## 📞 Support

For issues:
1. Check logs: `oc logs -f deployment/innovation-hub -n innovation-hub`
2. Check events: `oc get events -n innovation-hub --sort-by='.lastTimestamp'`
3. Test health: `curl https://your-app/api/health`
4. Review [DEPLOYMENT.md](DEPLOYMENT.md) troubleshooting section

---

**Need Help?** Check the full [DEPLOYMENT.md](DEPLOYMENT.md) guide for detailed troubleshooting.
