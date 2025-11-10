# Innovation Hub - OpenShift Deployment Validation Checklist

Use this checklist to ensure your deployment is successful and production-ready.

## ✅ Pre-Deployment Validation

### Files Created
- [ ] `Dockerfile` exists and is OpenShift-compatible
- [ ] `.dockerignore` exists
- [ ] `.gitlab-ci.yml` configured
- [ ] `k8s/` directory contains all 8 manifests
- [ ] `argocd/` directory contains application.yaml
- [ ] `setup-openshift.sh` is executable
- [ ] `.gitignore` includes secrets and sensitive files

### Configuration Updated
- [ ] k8s/deployment.yaml: Image name updated
- [ ] k8s/route.yaml: Domain name updated
- [ ] k8s/kustomization.yaml: Image name updated
- [ ] .gitlab-ci.yml: Image name and domain updated
- [ ] argocd/application.yaml: Repository URL updated

### API Keys Obtained
- [ ] OpenRouter API key available
- [ ] OpenAI API key available
- [ ] GitLab personal access token created (with api, write_repository scopes)
- [ ] OpenShift access token available

### Access Confirmed
- [ ] OpenShift cluster accessible via oc CLI
- [ ] GitLab repository created
- [ ] GitLab CI/CD enabled
- [ ] GitLab Container Registry accessible

## 🔧 Setup Script Validation

Run: `./setup-openshift.sh`

- [ ] Script prompts for all required information
- [ ] Successfully logs into OpenShift
- [ ] Creates innovation-hub namespace
- [ ] Creates gitlab-registry secret
- [ ] Creates innovation-hub-secrets
- [ ] Creates gitlab-ci service account
- [ ] Updates configuration files
- [ ] Displays service account token

## 🔐 GitLab CI/CD Variables

Go to: **GitLab → Settings → CI/CD → Variables**

Required Variables:
- [ ] `OPENSHIFT_SERVER` set (Protected: Yes)
- [ ] `OPENSHIFT_TOKEN` set (Protected: Yes, Masked: Yes)
- [ ] `GITLAB_PUSH_TOKEN` set (Protected: Yes, Masked: Yes)

Optional Variables:
- [ ] `OPENROUTER_API_KEY` set (Protected: Yes, Masked: Yes)
- [ ] `OPENAI_API_KEY` set (Protected: Yes, Masked: Yes)

## 🚀 Initial Deployment

### Apply Manifests
```bash
oc apply -k k8s/
```

Verify:
- [ ] Namespace created: `oc get namespace innovation-hub`
- [ ] ConfigMap created: `oc get configmap -n innovation-hub`
- [ ] Secrets created: `oc get secrets -n innovation-hub`
- [ ] PVCs created and bound: `oc get pvc -n innovation-hub`
- [ ] Deployment created: `oc get deployment -n innovation-hub`
- [ ] Service created: `oc get service -n innovation-hub`
- [ ] Route created: `oc get route -n innovation-hub`

### Pod Status
```bash
oc get pods -n innovation-hub
```

Expected:
- [ ] Pod status: Running
- [ ] Ready: 1/1
- [ ] Restarts: 0
- [ ] Age: > 0

### Check Events
```bash
oc get events -n innovation-hub --sort-by='.lastTimestamp' | tail -20
```

Expected:
- [ ] No error events
- [ ] Image pulled successfully
- [ ] Container created successfully
- [ ] Pod started successfully

## 🏥 Health Check Validation

Get route URL:
```bash
ROUTE_URL=$(oc get route innovation-hub -n innovation-hub -o jsonpath='{.spec.host}')
```

Test endpoints:
```bash
curl https://$ROUTE_URL/api/health/live
curl https://$ROUTE_URL/api/health/ready
curl https://$ROUTE_URL/api/health
```

Expected responses:
- [ ] `/api/health/live` returns: `{"status":"alive",...}`
- [ ] `/api/health/ready` returns: `{"status":"ready",...}`
- [ ] `/api/health` returns: `{"status":"healthy","database":"healthy",...}`

### Frontend Access
```bash
open https://$ROUTE_URL
# or curl https://$ROUTE_URL
```

Expected:
- [ ] Frontend loads successfully
- [ ] No 404 errors
- [ ] Static assets load
- [ ] API calls work

### API Documentation
```bash
open https://$ROUTE_URL/docs
```

Expected:
- [ ] Swagger UI loads
- [ ] All endpoints listed
- [ ] Try it out works

## 📊 Resource Validation

### Pod Resources
```bash
oc describe pod -l app=innovation-hub -n innovation-hub
```

Verify:
- [ ] CPU requests: 250m
- [ ] Memory requests: 512Mi
- [ ] CPU limits: 1000m
- [ ] Memory limits: 2Gi
- [ ] Volumes mounted correctly

### Storage Validation
```bash
oc get pvc -n innovation-hub
```

Expected:
- [ ] innovation-hub-data: Bound, 5Gi
- [ ] innovation-hub-chroma: Bound, 10Gi

Verify data persistence:
```bash
# Access pod
oc rsh deployment/innovation-hub -n innovation-hub

# Check database
ls -lh /app/data/innovation_hub.db

# Check ChromaDB
ls -lh /app/chroma_db/

# Exit
exit
```

Expected:
- [ ] Database file exists and has size > 0
- [ ] ChromaDB directory exists with data

## 📝 Logging Validation

### View Logs
```bash
oc logs -f deployment/innovation-hub -n innovation-hub --tail=100
```

Expected:
- [ ] No ERROR level logs
- [ ] Application started successfully
- [ ] Database initialized
- [ ] Health checks passing
- [ ] No connection errors

### Log Patterns to Look For
- [ ] ✅ "Innovation Hub - Module 1: Core Data Foundation"
- [ ] ✅ "Database ready!"
- [ ] ✅ "Starting Innovation Hub API..."
- [ ] ✅ "Application startup complete"
- [ ] ❌ No "Error" or "Exception" messages

## 🔄 CI/CD Pipeline Validation

### Trigger Pipeline
```bash
git commit --allow-empty -m "Test CI/CD pipeline"
git push origin main
```

Go to: **GitLab → CI/CD → Pipelines**

Expected:
- [ ] Pipeline triggered automatically
- [ ] Test stage: Passed
- [ ] Build stage: Passed
- [ ] Image pushed to registry
- [ ] Deploy stage: Available (manual)

### Manual Deploy
- [ ] Click "Play" button on deploy job
- [ ] Job runs successfully
- [ ] kustomization.yaml updated with new image tag
- [ ] Commit pushed to repository

## 🔀 ArgoCD Validation (Optional)

### ArgoCD Installation
```bash
oc get pods -n argocd
```

Expected:
- [ ] All ArgoCD pods running
- [ ] argocd-server accessible

### Application Status
```bash
argocd app get innovation-hub
```

Expected:
- [ ] Health Status: Healthy
- [ ] Sync Status: Synced
- [ ] No errors

### Auto-Sync Test
1. Make change to k8s/configmap.yaml
2. Commit and push
3. Wait 3 minutes

Expected:
- [ ] ArgoCD detects change
- [ ] Auto-sync triggered
- [ ] Application updated successfully

## 🔒 Security Validation

### Non-Root Validation
```bash
oc rsh deployment/innovation-hub -n innovation-hub
id
```

Expected:
- [ ] UID: Not 0 (root)
- [ ] GID: 0 (root group)

### Secret Security
```bash
oc get secret innovation-hub-secrets -n innovation-hub -o yaml
```

Expected:
- [ ] Values are base64 encoded
- [ ] No plaintext secrets visible
- [ ] Type: Opaque

### Image Pull Secret
```bash
oc get secret gitlab-registry -n innovation-hub
```

Expected:
- [ ] Secret exists
- [ ] Type: kubernetes.io/dockerconfigjson
- [ ] Linked to default service account

## 🌐 Network Validation

### Route Testing
```bash
oc get route innovation-hub -n innovation-hub
```

Expected:
- [ ] Host name configured
- [ ] TLS: edge
- [ ] Path: / (root)

### TLS Certificate
```bash
curl -vI https://$ROUTE_URL 2>&1 | grep -i "certificate"
```

Expected:
- [ ] Certificate valid
- [ ] TLS 1.2 or higher
- [ ] No certificate errors

### Service Connectivity
```bash
oc run test-pod --image=busybox -it --rm -n innovation-hub -- wget -O- http://innovation-hub:8000/api/health
```

Expected:
- [ ] Connection successful
- [ ] Health check returns 200 OK

## 📈 Performance Validation

### Response Times
```bash
time curl https://$ROUTE_URL/api/health
```

Expected:
- [ ] Response time < 500ms
- [ ] No timeouts
- [ ] Consistent response times

### Resource Usage
```bash
oc adm top pod -n innovation-hub
```

Expected:
- [ ] CPU usage: < 80% of limit
- [ ] Memory usage: < 80% of limit
- [ ] No OOMKilled status

## 🔄 Update & Rollback Validation

### Trigger Update
```bash
# Make small change
echo "# Update test" >> README.md
git commit -am "Test update"
git push origin main
```

Expected:
- [ ] CI/CD pipeline runs
- [ ] New image built and pushed
- [ ] Rolling update triggered
- [ ] Zero downtime (old pod running until new pod ready)
- [ ] New pod becomes ready
- [ ] Old pod terminated

### Rollback Test
```bash
oc rollout undo deployment/innovation-hub -n innovation-hub
```

Expected:
- [ ] Rollback initiated
- [ ] Previous version deployed
- [ ] Application still healthy
- [ ] No data loss

## 🧪 Functional Testing

### Create Test Idea
Via UI or API:
```bash
curl -X POST https://$ROUTE_URL/api/ideas \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Idea from Deployment",
    "description": "Validating the deployment",
    "type": "idea",
    "target_group": "citizens"
  }'
```

Expected:
- [ ] Idea created successfully
- [ ] Returns ID and analysis results
- [ ] Idea appears in UI

### Verify Persistence
```bash
# Restart pod
oc rollout restart deployment/innovation-hub -n innovation-hub
oc rollout status deployment/innovation-hub -n innovation-hub

# Check if idea still exists
curl https://$ROUTE_URL/api/ideas | grep "Test Idea"
```

Expected:
- [ ] Data persisted after restart
- [ ] Test idea still exists
- [ ] No data loss

## 📋 Documentation Validation

- [ ] DEPLOYMENT.md readable and accurate
- [ ] QUICKSTART.md tested and working
- [ ] DEPLOYMENT_FILES.md lists all files
- [ ] argocd/README.md provides clear instructions
- [ ] All commands in docs tested and working

## ✅ Final Checklist

### Critical
- [ ] Application accessible via route
- [ ] All health checks passing
- [ ] Database persisting data
- [ ] No errors in logs
- [ ] CI/CD pipeline working
- [ ] Secrets not committed to git

### Important
- [ ] TLS/HTTPS working
- [ ] Resource limits set
- [ ] Pod running as non-root
- [ ] PVCs bound and working
- [ ] ArgoCD syncing (if used)

### Nice to Have
- [ ] Monitoring configured
- [ ] Alerts set up
- [ ] Backup strategy defined
- [ ] Disaster recovery plan documented

## 🎉 Success Criteria

Your deployment is successful when:

✅ All health endpoints return 200 OK
✅ Frontend loads without errors
✅ API creates and retrieves ideas
✅ Data persists across pod restarts
✅ CI/CD pipeline runs successfully
✅ No critical errors in logs
✅ Security best practices followed

## 📞 Troubleshooting

If any checks fail, refer to:
- [DEPLOYMENT.md](DEPLOYMENT.md) - Troubleshooting section
- [QUICKSTART.md](QUICKSTART.md) - Common issues

Or check:
```bash
# Pod events
oc describe pod -l app=innovation-hub -n innovation-hub

# Logs
oc logs -f deployment/innovation-hub -n innovation-hub

# Resources
oc get all -n innovation-hub
```

---

**Last Updated**: 2025-10-27
**Status**: Ready for Production ✅
