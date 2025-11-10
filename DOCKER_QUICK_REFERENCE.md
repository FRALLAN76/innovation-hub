# Innovation Hub - Docker Quick Reference

Fast commands for local Docker testing.

## 🚀 Quick Start (3 Methods)

### Method 1: Automated Test Script (Recommended)
```bash
./test-docker.sh
```
Runs complete validation suite and keeps container running.

### Method 2: Docker Compose (Easiest)
```bash
# Setup
cp .env.example .env
# Edit .env with your API keys

# Start
docker compose up -d

# Access
open http://localhost:8000
```

### Method 3: Manual Docker Run
```bash
docker build -t innovation-hub:local .

docker run -d \
  --name innovation-hub \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/local-data:/app/data \
  -v $(pwd)/local-chroma:/app/chroma_db \
  innovation-hub:local
```

## 📋 Essential Commands

### Build
```bash
# Build image
docker build -t innovation-hub:local .

# Build without cache
docker build -t innovation-hub:local . --no-cache

# Build with verbose output
docker build -t innovation-hub:local . --progress=plain
```

### Run
```bash
# Start with docker-compose
docker compose up -d

# Start manually
docker run -d --name innovation-hub -p 8000:8000 --env-file .env innovation-hub:local

# Start with interactive logs
docker compose up
```

### Manage
```bash
# View logs
docker logs -f innovation-hub
docker compose logs -f

# Check status
docker ps
docker compose ps

# Shell access
docker exec -it innovation-hub bash

# Stop
docker stop innovation-hub
docker compose stop

# Remove
docker rm innovation-hub
docker compose down

# Restart
docker restart innovation-hub
docker compose restart
```

### Monitor
```bash
# Resource usage
docker stats innovation-hub

# Health status
docker inspect --format='{{.State.Health.Status}}' innovation-hub

# Process list
docker top innovation-hub
```

## 🧪 Testing Commands

### Health Checks
```bash
# Liveness
curl http://localhost:8000/api/health/live

# Readiness
curl http://localhost:8000/api/health/ready

# Main health
curl http://localhost:8000/api/health
```

### API Tests
```bash
# View API docs
open http://localhost:8000/docs

# Get ideas
curl http://localhost:8000/api/ideas

# Create idea
curl -X POST http://localhost:8000/api/ideas \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","description":"Testing","type":"idea","target_group":"citizens"}'

# Stats
curl http://localhost:8000/api/ideas/stats
```

### Security Tests
```bash
# Check user ID (should not be 0)
docker exec innovation-hub id

# Test with random UID (OpenShift simulation)
docker run -d --name test --user $(shuf -i 100000-200000 -n 1):0 \
  -p 8001:8000 --env-file .env innovation-hub:local
```

### Performance Tests
```bash
# Response time
time curl http://localhost:8000/api/health

# Load test (requires 'ab')
ab -n 1000 -c 10 http://localhost:8000/api/health
```

## 🔧 Troubleshooting

### View Logs
```bash
docker logs innovation-hub
docker logs innovation-hub --tail 50
docker logs innovation-hub -f --since 5m
```

### Debug Container
```bash
# Shell access
docker exec -it innovation-hub bash

# Check processes
docker exec innovation-hub ps aux

# Check listening ports
docker exec innovation-hub netstat -tlnp

# Check files
docker exec innovation-hub ls -la /app/data/
```

### Fix Issues
```bash
# Port in use
sudo lsof -i :8000
# Or change port: -p 8001:8000

# Permission issues
mkdir -p local-data local-chroma
chmod 777 local-data local-chroma

# Clean restart
docker compose down -v
docker compose up -d --build

# Complete cleanup
docker stop innovation-hub
docker rm innovation-hub
docker rmi innovation-hub:local
rm -rf local-data/ local-chroma/
```

## 🗄️ Database Operations

```bash
# Access database
docker exec -it innovation-hub sqlite3 /app/data/innovation_hub.db

# In SQLite shell:
.tables                    # List tables
.schema ideas              # Show schema
SELECT COUNT(*) FROM ideas; # Count ideas
SELECT * FROM ideas LIMIT 5; # View ideas
.quit                      # Exit

# Backup database
docker cp innovation-hub:/app/data/innovation_hub.db ./backup.db

# Restore database
docker cp ./backup.db innovation-hub:/app/data/innovation_hub.db
docker restart innovation-hub
```

## 📦 Volume Management

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect innovation-hub_data

# Backup volumes
docker run --rm \
  -v innovation-hub_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/data-backup.tar.gz /data

# Restore volumes
docker run --rm \
  -v innovation-hub_data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/data-backup.tar.gz -C /
```

## 🧹 Cleanup Commands

```bash
# Stop and remove container
docker compose down

# Remove with volumes
docker compose down -v

# Remove image
docker rmi innovation-hub:local

# Remove local data
rm -rf local-data/ local-chroma/

# Nuclear option (removes all unused Docker resources)
docker system prune -a --volumes
```

## 🔐 Environment Variables

Create `.env` file:
```bash
cp .env.example .env
```

Required variables:
```bash
OPENROUTER_API_KEY=sk-or-v1-...
OPENAI_API_KEY=sk-proj-...
```

Optional variables:
```bash
DEBUG=True
HOST=0.0.0.0
PORT=8000
AI_MODEL=qwen/qwen3-32b
```

## 🎯 Before OpenShift Deployment

Run these tests:
```bash
# 1. Automated test
./test-docker.sh

# 2. Manual checks
curl http://localhost:8000/api/health
curl http://localhost:8000/api/health/ready
docker exec innovation-hub id

# 3. OpenShift simulation
docker run -d --user $(shuf -i 100000-200000 -n 1):0 \
  --name openshift-test -p 8001:8000 --env-file .env \
  innovation-hub:local

# 4. Wait and test
sleep 30
curl http://localhost:8001/api/health

# 5. Cleanup
docker stop openshift-test && docker rm openshift-test
```

## 📚 Full Documentation

- **Complete Guide**: [LOCAL_TESTING.md](LOCAL_TESTING.md)
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)

## 💡 Pro Tips

1. **Use docker-compose for development** - easier to manage
2. **Keep .env file secure** - never commit it
3. **Test with random UIDs** before OpenShift deployment
4. **Monitor logs** during first run
5. **Backup database** before major changes
6. **Clean up regularly** to free disk space

## 🆘 Common Issues

| Issue | Solution |
|-------|----------|
| Port in use | Change port: `-p 8001:8000` |
| Permission denied | `chmod 777 local-data` |
| Container won't start | Check logs: `docker logs innovation-hub` |
| Health check fails | Wait 30s, check `/api/health` |
| Can't access frontend | Check port: `docker port innovation-hub` |
| Database locked | Stop container, remove `.db-journal` file |

---

**Need more details?** See [LOCAL_TESTING.md](LOCAL_TESTING.md) for comprehensive testing guide.
