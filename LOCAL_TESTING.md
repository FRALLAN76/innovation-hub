# Innovation Hub - Local Docker Testing Guide

Complete guide for testing the Docker image locally before deploying to OpenShift.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Manual Docker Build & Run](#manual-docker-build--run)
4. [Docker Compose](#docker-compose)
5. [Testing OpenShift Compatibility](#testing-openshift-compatibility)
6. [Validation](#validation)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

- Docker installed (20.10+)
- Docker Compose installed (v2.0+)
- API keys for OpenRouter and OpenAI
- At least 2GB free disk space

### Check Prerequisites

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker compose version

# Check Docker is running
docker ps
```

## Quick Start

### 1. Setup Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
nano .env  # or vim, code, etc.
```

Add your keys:
```bash
OPENROUTER_API_KEY=sk-or-v1-your-actual-key
OPENAI_API_KEY=sk-proj-your-actual-key
```

### 2. Run with Docker Compose

```bash
# Build and start
docker compose up --build

# Or in detached mode
docker compose up -d --build

# View logs
docker compose logs -f

# Stop
docker compose down
```

### 3. Access Application

- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## Manual Docker Build & Run

### Build Image

```bash
# Build the image
docker build -t innovation-hub:local .

# Check image
docker images | grep innovation-hub
```

### Run Container (Simple)

```bash
# Run with environment variables from .env file
docker run -d \
  --name innovation-hub \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/local-data:/app/data \
  -v $(pwd)/local-chroma:/app/chroma_db \
  innovation-hub:local

# View logs
docker logs -f innovation-hub

# Stop and remove
docker stop innovation-hub
docker rm innovation-hub
```

### Run Container (With All Options)

```bash
docker run -d \
  --name innovation-hub \
  -p 8000:8000 \
  -e HOST="0.0.0.0" \
  -e PORT="8000" \
  -e DEBUG="True" \
  -e DATABASE_URL="sqlite:////app/data/innovation_hub.db" \
  -e AI_MODEL="qwen/qwen3-32b" \
  -e OPENROUTER_BASE_URL="https://openrouter.ai/api/v1" \
  -e OPENROUTER_API_KEY="${OPENROUTER_API_KEY}" \
  -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
  -v $(pwd)/local-data:/app/data \
  -v $(pwd)/local-chroma:/app/chroma_db \
  --health-cmd="curl -f http://localhost:8000/api/health || exit 1" \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  --health-start-period=40s \
  innovation-hub:local
```

## Docker Compose

### Basic Usage

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f innovation-hub

# Check status
docker compose ps

# Restart service
docker compose restart

# Stop services
docker compose stop

# Stop and remove
docker compose down

# Stop and remove with volumes
docker compose down -v
```

### Rebuild After Code Changes

```bash
# Rebuild and restart
docker compose up -d --build

# Force rebuild (no cache)
docker compose build --no-cache
docker compose up -d
```

### View Resource Usage

```bash
# Container stats
docker stats innovation-hub

# Detailed inspect
docker inspect innovation-hub
```

## Testing OpenShift Compatibility

### Test Non-Root User

```bash
# Check what user the container runs as
docker exec innovation-hub id

# Expected output:
# uid=1001 gid=0(root) groups=0(root)
```

### Test File Permissions

```bash
# Check data directory permissions
docker exec innovation-hub ls -la /app/data

# Try writing to data directory
docker exec innovation-hub touch /app/data/test.txt
docker exec innovation-hub rm /app/data/test.txt
```

### Test Volume Mounts

```bash
# Create test data
docker exec innovation-hub sqlite3 /app/data/test.db "CREATE TABLE test(id INT);"

# Verify on host
ls -lh local-data/

# Stop container
docker compose down

# Start again
docker compose up -d

# Verify data persisted
docker exec innovation-hub ls -lh /app/data/
```

### Test Health Checks

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' innovation-hub

# View health check logs
docker inspect --format='{{json .State.Health}}' innovation-hub | jq
```

### Simulate OpenShift Security Context

Run with random UID like OpenShift does:

```bash
# Run as random UID in root group (simulating OpenShift)
docker run -d \
  --name innovation-hub-openshift-test \
  -p 8001:8000 \
  --user $(shuf -i 100000-200000 -n 1):0 \
  --env-file .env \
  -v $(pwd)/local-data:/app/data \
  -v $(pwd)/local-chroma:/app/chroma_db \
  innovation-hub:local

# Check if it runs successfully
docker logs innovation-hub-openshift-test

# Access it
curl http://localhost:8001/api/health

# Cleanup
docker stop innovation-hub-openshift-test
docker rm innovation-hub-openshift-test
```

## Validation

### Health Endpoints

```bash
# Liveness probe
curl http://localhost:8000/api/health/live
# Expected: {"status":"alive","message":"Application is alive"}

# Readiness probe
curl http://localhost:8000/api/health/ready
# Expected: {"status":"ready","message":"Application is ready to serve traffic"}

# Main health check
curl http://localhost:8000/api/health
# Expected: {"status":"healthy","message":"...","database":"healthy","version":"1.0.0"}
```

### API Endpoints

```bash
# Get API stats
curl http://localhost:8000/api/ideas/stats

# List ideas
curl http://localhost:8000/api/ideas

# Create test idea
curl -X POST http://localhost:8000/api/ideas \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Idea from Docker",
    "description": "Testing the Docker image",
    "type": "idea",
    "target_group": "citizens"
  }'

# List ideas again (should see your test idea)
curl http://localhost:8000/api/ideas | jq
```

### Frontend Test

```bash
# Open in browser
open http://localhost:8000

# Or test with curl
curl -I http://localhost:8000
# Expected: 200 OK
```

### Database Persistence Test

```bash
# Create test data
curl -X POST http://localhost:8000/api/ideas \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Persistence Test",
    "description": "This should survive container restart",
    "type": "idea",
    "target_group": "citizens"
  }'

# Stop container
docker compose down

# Check that data exists on host
ls -lh local-data/innovation_hub.db

# Start container again
docker compose up -d

# Verify data still exists
curl http://localhost:8000/api/ideas | jq '.[] | select(.title=="Persistence Test")'
```

### Performance Test

```bash
# Test response time
time curl http://localhost:8000/api/health

# Stress test (requires 'ab' - Apache Bench)
ab -n 100 -c 10 http://localhost:8000/api/health

# Or use wrk
wrk -t2 -c10 -d30s http://localhost:8000/api/health
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs innovation-hub

# Common issues:
# 1. Port 8000 already in use
sudo lsof -i :8000
# Kill process or change port

# 2. Missing environment variables
docker exec innovation-hub env | grep -E "OPENROUTER|OPENAI"

# 3. Permission issues
docker exec innovation-hub ls -la /app/data
```

### Health Check Failing

```bash
# Check health status
docker inspect --format='{{json .State.Health}}' innovation-hub | jq

# Test health endpoint manually
docker exec innovation-hub curl -f http://localhost:8000/api/health

# Check if app is listening
docker exec innovation-hub netstat -tlnp | grep 8000
```

### Database Issues

```bash
# Check if database file exists
docker exec innovation-hub ls -lh /app/data/

# Check database integrity
docker exec innovation-hub sqlite3 /app/data/innovation_hub.db "PRAGMA integrity_check;"

# Access database
docker exec -it innovation-hub sqlite3 /app/data/innovation_hub.db
# Then run SQL commands:
# .tables
# .schema ideas
# SELECT COUNT(*) FROM ideas;
# .quit
```

### Volume Permission Issues

```bash
# Check volume permissions on host
ls -la local-data/

# If permission denied, fix ownership
sudo chown -R $(id -u):$(id -g) local-data/ local-chroma/

# Or create directories first
mkdir -p local-data local-chroma
chmod 777 local-data local-chroma  # For testing only
```

### Memory Issues

```bash
# Check container memory usage
docker stats innovation-hub --no-stream

# Increase memory limit
docker run -d \
  --name innovation-hub \
  --memory="2g" \
  --memory-swap="2g" \
  -p 8000:8000 \
  --env-file .env \
  innovation-hub:local
```

### Network Issues

```bash
# Check port binding
docker port innovation-hub

# Test from inside container
docker exec innovation-hub curl http://localhost:8000/api/health

# Test from host
curl http://localhost:8000/api/health

# Check Docker network
docker network inspect bridge
```

### Build Issues

```bash
# Build with verbose output
docker build -t innovation-hub:local . --progress=plain

# Build without cache
docker build -t innovation-hub:local . --no-cache

# Check build context size
du -sh .
# If too large, check .dockerignore
```

## Clean Up

### Remove Containers

```bash
# Stop and remove via docker compose
docker compose down

# Or manually
docker stop innovation-hub
docker rm innovation-hub
```

### Remove Images

```bash
# Remove local image
docker rmi innovation-hub:local

# Remove all unused images
docker image prune -a
```

### Remove Volumes

```bash
# Remove local data (careful!)
rm -rf local-data/ local-chroma/

# Remove Docker volumes (if using named volumes)
docker volume ls
docker volume rm <volume-name>
```

### Complete Cleanup

```bash
# Remove everything
docker compose down -v --rmi all
rm -rf local-data/ local-chroma/
```

## Best Practices

### For Development

1. **Use docker-compose.yml** for easy start/stop
2. **Mount volumes** to persist data
3. **Use .env file** for configuration
4. **Enable DEBUG mode** for detailed logs
5. **Check logs frequently**: `docker compose logs -f`

### Before Pushing to OpenShift

1. **Test with random UID**: Simulate OpenShift security
2. **Test health checks**: Ensure all probes work
3. **Test persistence**: Restart container and verify data
4. **Test resource limits**: Run with memory/CPU constraints
5. **Test without root**: Ensure non-root user works

### Security

1. **Never commit .env** to git
2. **Use .env.example** as template
3. **Rotate API keys** regularly
4. **Don't expose ports** unnecessarily
5. **Use Docker secrets** for production

## Integration with OpenShift Workflow

```bash
# 1. Test locally
docker compose up -d
curl http://localhost:8000/api/health

# 2. Tag for registry
docker tag innovation-hub:local registry.gitlab.com/your-group/innovation-hub:test

# 3. (Optional) Push to test if registry works
docker login registry.gitlab.com
docker push registry.gitlab.com/your-group/innovation-hub:test

# 4. Deploy to OpenShift
oc apply -k k8s/
```

## Quick Commands Reference

```bash
# Start
docker compose up -d

# Logs
docker compose logs -f

# Status
docker compose ps

# Shell access
docker exec -it innovation-hub bash

# Health check
curl http://localhost:8000/api/health

# Restart
docker compose restart

# Stop
docker compose down

# Rebuild
docker compose up -d --build
```

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `HOST` | No | 0.0.0.0 | Host to bind to |
| `PORT` | No | 8000 | Port to listen on |
| `DEBUG` | No | False | Enable debug mode |
| `DATABASE_URL` | No | sqlite:///./innovation_hub.db | Database connection |
| `AI_MODEL` | No | qwen/qwen3-32b | AI model to use |
| `OPENROUTER_API_KEY` | Yes | - | OpenRouter API key |
| `OPENAI_API_KEY` | Yes | - | OpenAI API key |
| `OPENROUTER_BASE_URL` | No | https://openrouter.ai/api/v1 | API endpoint |

---

**Ready to deploy?** Once local testing passes, proceed with OpenShift deployment using [DEPLOYMENT.md](DEPLOYMENT.md).
