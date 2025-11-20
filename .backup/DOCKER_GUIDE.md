# 🐳 Docker Setup Guide for MediAssist-AI

## 📋 Current Docker Configuration Analysis

Your project has a good Docker foundation! Here's what you have:

### ✅ Existing Files:
- `Dockerfile.api` - Backend API container
- `Dockerfile.web` - Frontend web container  
- `infra/docker-compose.yml` - Multi-container orchestration
- `infra/nginx.web.conf` - Nginx configuration for frontend

### 🎯 Services Configured:
1. **API** (FastAPI backend on port 8000)
2. **Web** (React frontend on port 3000)
3. **Redis** (Cache/session storage)
4. **Prometheus** (Metrics collection)
5. **Grafana** (Monitoring dashboards on port 3001)
6. **Node Exporter** (System metrics)
7. **cAdvisor** (Container metrics)
8. **Redis Exporter** (Redis metrics)

---

## 🚀 Quick Start Guide

### Prerequisites:

```bash
# Check if Docker is installed
docker --version

# If not installed:
# macOS: Download from https://www.docker.com/products/docker-desktop
# Or use Homebrew:
brew install --cask docker
```

### Step 1: Create Environment File

Create `/Users/hrithikeshsankineni/Documents/MediAssist-AI/api/.env.docker`:

```env
# Database (Using Neon PostgreSQL)
DB_URL=postgresql://neondb_owner:npg_TJOy0MUH8YiA@ep-withered-unit-ad1fm90p-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require

# Redis
REDIS_URL=redis://redis:6379/0

# Auth0
AUTH0_DOMAIN=dev-bv4rdiy74pj3ybge.us.auth0.com
AUTH0_AUDIENCE=https://api.mediassistai
AUTH0_JWKS=https://dev-bv4rdiy74pj3ybge.us.auth0.com/.well-known/jwks.json

# Twilio
TWILIO_ACCOUNT_SID=ACea04dbf8586de660a5585e20d85c6668
TWILIO_AUTH_TOKEN=600665820ff037b203b653bfa9832550
TWILIO_FROM_NUMBER=+16363317602

# Gmail SMTP
GMAIL_ADDRESS=shritikesh8999@gmail.com
GMAIL_APP_PASSWORD=kxzfnaeizmkqibhb

# API Keys
MAPS_API_KEY=AIzaSyDSYNQz5tkIRJPTiSbly-ng8Odgcqevqp4
GEMINI_API_KEY=AIzaSyCEPUDlgsYj1i6MffQp_dxRGd4ztGCTtSE
ELEVENLABS_API_KEY=sk_70d4491d69eab0f41e5d1574263aa4b6b26510576835daab

# Base URL
BASE_URL=http://localhost:8000
```

### Step 2: Build and Run

```bash
# Navigate to project root
cd /Users/hrithikeshsankineni/Documents/MediAssist-AI

# Build all containers
docker-compose -f infra/docker-compose.yml build

# Start all services
docker-compose -f infra/docker-compose.yml up -d

# Check status
docker-compose -f infra/docker-compose.yml ps

# View logs
docker-compose -f infra/docker-compose.yml logs -f api
docker-compose -f infra/docker-compose.yml logs -f web
```

### Step 3: Access Services

- **Frontend:** http://localhost:3000
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Grafana:** http://localhost:3001 (admin/admin)
- **Prometheus:** http://localhost:9090

---

## 🔧 Improvements Needed

I'll create improved versions of your Docker files:

### Issues Found:
1. ❌ Missing `.dockerignore` files (causes large image sizes)
2. ⚠️ Environment variables hardcoded in docker-compose.yml
3. ⚠️ No health checks configured
4. ⚠️ API Dockerfile missing init_db.py execution
5. ⚠️ Missing volume mounts for development

---

## 📝 Useful Docker Commands

### Basic Operations:

```bash
# Start services
docker-compose -f infra/docker-compose.yml up -d

# Stop services
docker-compose -f infra/docker-compose.yml down

# Restart a specific service
docker-compose -f infra/docker-compose.yml restart api

# Rebuild a service
docker-compose -f infra/docker-compose.yml build --no-cache api

# View logs
docker-compose -f infra/docker-compose.yml logs -f
docker-compose -f infra/docker-compose.yml logs -f api
docker-compose -f infra/docker-compose.yml logs -f web

# Execute command in container
docker-compose -f infra/docker-compose.yml exec api bash
docker-compose -f infra/docker-compose.yml exec api python -m app.database

# Scale services
docker-compose -f infra/docker-compose.yml up -d --scale api=3
```

### Cleanup:

```bash
# Stop and remove containers
docker-compose -f infra/docker-compose.yml down

# Remove volumes too
docker-compose -f infra/docker-compose.yml down -v

# Remove all unused containers, networks, images
docker system prune -a

# Remove specific image
docker rmi mediassist-ai-api
docker rmi mediassist-ai-web
```

### Debugging:

```bash
# Check container status
docker ps
docker ps -a

# Inspect container
docker inspect <container_id>

# Check container resource usage
docker stats

# View container IP
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name>

# Copy files from container
docker cp <container_id>:/app/logs ./logs
```

---

## 🏗️ Development vs Production

### Development Setup (Hot Reload):

```yaml
# docker-compose.dev.yml
services:
  api:
    build:
      context: ..
      dockerfile: Dockerfile.api
    volumes:
      - ../api:/app  # Mount source code
    environment:
      - RELOAD=true
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Setup:

```bash
# Use the existing docker-compose.yml as-is
docker-compose -f infra/docker-compose.yml up -d
```

---

## 📊 Monitoring with Grafana

Once running:

1. Open http://localhost:3001
2. Login: admin / admin
3. Add Prometheus datasource: http://prometheus:9090
4. Import dashboards for:
   - Docker containers (cAdvisor)
   - Redis metrics
   - API performance
   - System resources

---

## 🐛 Troubleshooting

### Port Already in Use:

```bash
# Find process using port
lsof -ti:8000
lsof -ti:3000

# Kill process
kill -9 <PID>

# Or use different ports in docker-compose.yml
```

### Container Won't Start:

```bash
# Check logs
docker-compose -f infra/docker-compose.yml logs api

# Check if it's a permissions issue
docker-compose -f infra/docker-compose.yml exec api ls -la /app

# Rebuild without cache
docker-compose -f infra/docker-compose.yml build --no-cache api
```

### Database Connection Failed:

```bash
# Test connection from container
docker-compose -f infra/docker-compose.yml exec api python -c "
from app.database import engine
try:
    engine.connect()
    print('✅ Database connected!')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

### Redis Connection Failed:

```bash
# Check Redis is running
docker-compose -f infra/docker-compose.yml ps redis

# Test Redis connection
docker-compose -f infra/docker-compose.yml exec redis redis-cli ping
```

---

## 🎯 Next Steps

Would you like me to:

1. ✅ Create `.dockerignore` files to reduce image size
2. ✅ Create improved `docker-compose.yml` with health checks
3. ✅ Create `docker-compose.dev.yml` for development
4. ✅ Add database initialization to API Dockerfile
5. ✅ Create deployment scripts for easy setup
6. ✅ Add GitHub Actions for CI/CD with Docker

Let me know which improvements you'd like me to implement!

---

## 📦 Current Project Structure

```
MediAssist-AI/
├── api/
│   ├── app/
│   ├── Dockerfile          # Old (not used)
│   └── requirements.txt
├── web/
│   ├── src/
│   ├── package.json
│   └── ...
├── infra/
│   ├── docker-compose.yml
│   ├── nginx.web.conf
│   └── prometheus.yml
├── Dockerfile.api          # Used by docker-compose ✅
├── Dockerfile.web          # Used by docker-compose ✅
└── ...
```

---

## 🚀 Production Deployment

For hackathon/production:

```bash
# 1. Build optimized images
docker-compose -f infra/docker-compose.yml build

# 2. Tag images
docker tag mediassist-ai-api your-registry/mediassist-api:latest
docker tag mediassist-ai-web your-registry/mediassist-web:latest

# 3. Push to registry
docker push your-registry/mediassist-api:latest
docker push your-registry/mediassist-web:latest

# 4. Deploy to server
ssh your-server "docker-compose pull && docker-compose up -d"
```

---

**Ready to containerize your app! What would you like me to help with first?** 🐳
