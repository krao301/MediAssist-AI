# 🐳 Docker Deployment Guide

Complete guide for running MediAssist-AI with Docker.

---

## 📦 Quick Start (3 commands)

```bash
# 1. Clone/navigate to project
cd /Users/hrithikeshsankineni/Documents/MediAssist-AI

# 2. Start everything
./docker-start.sh

# 3. Open in browser
open http://localhost:3000
```

That's it! 🎉

---

## 📋 What You Get

When you run `./docker-start.sh`, you get a complete stack:

### Core Services:
- **Frontend (React)** - http://localhost:3000
- **API (FastAPI)** - http://localhost:8000
- **API Docs** - http://localhost:8000/docs
- **Redis Cache** - localhost:6379

### Monitoring Stack:
- **Grafana** - http://localhost:3001 (admin/admin)
- **Prometheus** - http://localhost:9090
- **cAdvisor** - http://localhost:8081 (container metrics)
- **Node Exporter** - http://localhost:9100 (system metrics)
- **Redis Exporter** - http://localhost:9121 (Redis metrics)

---

## 🚀 Deployment Options

### Option 1: Production (Recommended for Hackathon)

```bash
./docker-start.sh
```

**What it does:**
- ✅ Full monitoring stack (Prometheus + Grafana)
- ✅ Production-optimized builds
- ✅ Health checks enabled
- ✅ Automatic restarts
- ✅ Runs in background

**View logs:**
```bash
docker-compose -f infra/docker-compose.improved.yml logs -f
```

**Stop services:**
```bash
./docker-stop.sh
```

---

### Option 2: Development (Hot-Reload)

```bash
./docker-dev.sh
```

**What it does:**
- ✅ Source code mounted as volumes
- ✅ Auto-reload on file changes
- ✅ Vite dev server (port 5173)
- ✅ Uvicorn with --reload
- ✅ Faster development cycle

**Note:** Logs appear in terminal. Press `Ctrl+C` to stop.

---

### Option 3: Manual Control

If you prefer manual commands:

```bash
# Build images
docker-compose -f infra/docker-compose.improved.yml build

# Start services
docker-compose -f infra/docker-compose.improved.yml up -d

# Check status
docker-compose -f infra/docker-compose.improved.yml ps

# View logs
docker-compose -f infra/docker-compose.improved.yml logs -f api
docker-compose -f infra/docker-compose.improved.yml logs -f web

# Stop services
docker-compose -f infra/docker-compose.improved.yml down
```

---

## 🔧 Configuration

### Environment Variables

All configuration is in `api/.env.docker`:

```bash
# Database (Neon PostgreSQL Cloud)
DB_URL=postgresql://...

# Redis (Provided by Docker)
REDIS_URL=redis://redis:6379/0

# Twilio (SMS/Calls)
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_FROM_NUMBER=+16363317602

# Gmail (Emails)
GMAIL_ADDRESS=shritikesh8999@gmail.com
GMAIL_APP_PASSWORD=...

# APIs
MAPS_API_KEY=...
GEMINI_API_KEY=...
ELEVENLABS_API_KEY=...
```

**⚠️ Important:** Never commit `.env.docker` to git!

---

## 🐛 Troubleshooting

### Issue: Port Already in Use

```bash
# Find what's using the port
lsof -ti:8000

# Kill it
kill -9 <PID>

# Or use different ports in docker-compose.yml
```

### Issue: API Container Won't Start

```bash
# Check logs
docker-compose -f infra/docker-compose.improved.yml logs api

# Rebuild without cache
docker-compose -f infra/docker-compose.improved.yml build --no-cache api

# Check health
docker-compose -f infra/docker-compose.improved.yml ps
```

### Issue: Database Connection Failed

```bash
# Test connection from container
docker-compose -f infra/docker-compose.improved.yml exec api python -c "
from app.database import engine
try:
    engine.connect()
    print('✅ Database connected!')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

### Issue: Frontend Shows "Cannot connect to API"

```bash
# Check if API is running
curl http://localhost:8000/health

# Should return: {"status":"healthy"}

# Check API logs
docker-compose -f infra/docker-compose.improved.yml logs api
```

### Issue: Redis Connection Failed

```bash
# Check if Redis is running
docker-compose -f infra/docker-compose.improved.yml ps redis

# Test Redis connection
docker-compose -f infra/docker-compose.improved.yml exec redis redis-cli ping
# Should return: PONG
```

---

## 📊 Monitoring with Grafana

### Setup Grafana Dashboard

1. Open http://localhost:3001
2. Login: `admin` / `admin`
3. Add Prometheus datasource:
   - URL: `http://prometheus:9090`
   - Click "Save & Test"
4. Import dashboards:
   - Dashboard ID `1860` (Node Exporter)
   - Dashboard ID `193` (Docker Monitoring)
   - Dashboard ID `763` (Redis)

### Useful Metrics to Monitor

- **API Response Time** - Track `/triage` endpoint performance
- **Redis Hit Rate** - Cache effectiveness
- **Container Memory** - Ensure no memory leaks
- **Request Rate** - Traffic patterns
- **Error Rate** - Failed requests

---

## 🔍 Useful Commands

### Container Management

```bash
# List all containers
docker ps

# Stop a specific container
docker stop mediassist-api

# Restart a container
docker restart mediassist-api

# View container logs
docker logs -f mediassist-api

# Execute command in container
docker exec -it mediassist-api bash

# View container resource usage
docker stats
```

### Database Operations

```bash
# Access database from container
docker-compose -f infra/docker-compose.improved.yml exec api python manage_contacts.py
```

### Cleanup

```bash
# Stop and remove containers
./docker-stop.sh

# Remove volumes too (WARNING: deletes data)
docker-compose -f infra/docker-compose.improved.yml down -v

# Clean up unused Docker resources
docker system prune -a
```

---

## 🎯 Deployment to Cloud

### Deploy to DigitalOcean (Recommended)

```bash
# 1. Create a Droplet (Ubuntu 22.04)
# 2. SSH into droplet
ssh root@your-droplet-ip

# 3. Install Docker
curl -fsSL https://get.docker.com | sh

# 4. Clone your repo
git clone https://github.com/yourusername/MediAssist-AI.git
cd MediAssist-AI

# 5. Configure environment
nano api/.env.docker

# 6. Start services
./docker-start.sh

# 7. Setup domain (optional)
# Point your domain to droplet IP
# Setup Nginx reverse proxy with SSL
```

### Deploy to AWS ECS

```bash
# 1. Push images to ECR
aws ecr create-repository --repository-name mediassist-api
aws ecr create-repository --repository-name mediassist-web

docker tag mediassist-ai-api:latest <account>.dkr.ecr.us-east-1.amazonaws.com/mediassist-api:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/mediassist-api:latest

# 2. Create ECS task definition
# 3. Create ECS service
# 4. Setup load balancer
```

### Deploy to Google Cloud Run

```bash
# 1. Build and push to GCR
gcloud builds submit --tag gcr.io/<project>/mediassist-api

# 2. Deploy to Cloud Run
gcloud run deploy mediassist-api \
  --image gcr.io/<project>/mediassist-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 📦 Docker Image Optimization

### Current Image Sizes

```bash
# Check image sizes
docker images | grep mediassist

# Expected sizes:
# mediassist-api: ~500MB
# mediassist-web: ~50MB (multi-stage build)
```

### Further Optimization

If you need smaller images:

```dockerfile
# Use alpine variants
FROM python:3.12-alpine
FROM node:20-alpine

# Multi-stage builds (already implemented for web)
# Remove dev dependencies in production
RUN pip install --no-cache-dir -r requirements.txt
```

---

## 🔒 Security Checklist

### Before Deploying to Production:

- [ ] Change default Grafana password
- [ ] Use secrets management (AWS Secrets Manager, etc.)
- [ ] Enable HTTPS/SSL certificates
- [ ] Restrict CORS origins in `main.py`
- [ ] Use non-root users in containers (already implemented)
- [ ] Regular security updates:
  ```bash
  docker-compose pull
  docker-compose up -d
  ```
- [ ] Setup firewall rules
- [ ] Enable Docker logs rotation
- [ ] Backup strategy for Grafana dashboards

---

## 📈 Performance Tips

### For Hackathon Demo:

1. **Pre-warm the API:**
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/
   ```

2. **Monitor during demo:**
   - Keep Grafana dashboard open
   - Watch API logs in separate terminal
   - Test emergency flow before presenting

3. **Load testing (optional):**
   ```bash
   # Install hey
   brew install hey

   # Test API endpoint
   hey -n 100 -c 10 http://localhost:8000/health
   ```

### Production Scaling:

```bash
# Scale API horizontally
docker-compose -f infra/docker-compose.improved.yml up -d --scale api=3

# Add load balancer (Nginx)
# See infra/nginx.conf for example
```

---

## 🎓 Learning Resources

- **Docker Compose Docs:** https://docs.docker.com/compose/
- **Docker Best Practices:** https://docs.docker.com/develop/dev-best-practices/
- **Monitoring Guide:** https://prometheus.io/docs/guides/dockerswarm/
- **Multi-stage Builds:** https://docs.docker.com/build/building/multi-stage/

---

## ✅ Pre-Demo Checklist

Before your hackathon presentation:

- [ ] All services running: `docker-compose -f infra/docker-compose.improved.yml ps`
- [ ] Frontend accessible: http://localhost:3000
- [ ] API healthy: `curl http://localhost:8000/health`
- [ ] Test emergency flow (CRITICAL case)
- [ ] Test first aid flow (MINOR case)
- [ ] Check Grafana dashboards working
- [ ] Verify SMS/calls working
- [ ] Check email delivery
- [ ] Test nearby people finder (using hardcoded contacts)
- [ ] Have backup plan if Docker fails (run locally)

---

## 🆘 Emergency Commands

If something goes wrong during demo:

```bash
# Quick restart everything
./docker-stop.sh && ./docker-start.sh

# Check what's broken
docker-compose -f infra/docker-compose.improved.yml ps

# View recent logs
docker-compose -f infra/docker-compose.improved.yml logs --tail=50

# Nuclear option: rebuild everything
docker-compose -f infra/docker-compose.improved.yml down -v
docker system prune -a
./docker-start.sh
```

---

## 📞 Support

If you need help:

1. Check logs: `docker-compose logs`
2. Verify environment variables in `api/.env.docker`
3. Test individual services
4. Check GitHub Issues
5. Review DOCKER_GUIDE.md

---

**Good luck with your hackathon! 🚀**
