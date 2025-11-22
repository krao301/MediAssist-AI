# 🐳 How to Run Docker Images

## Quick Answer

You have **two options** to run your Docker images:

### Option 1: Run Locally (Testing)
```bash
# Pull and run your API image
docker run -d -p 8000:8000 \
  --env-file api/.env \
  hrithikesh11/mediassist-api:latest

# Pull and run your Web image
docker run -d -p 3000:80 \
  hrithikesh11/mediassist-web:latest
```

### Option 2: Use Docker Compose (Better)
```bash
cd infra
docker-compose up -d
```

---

## Detailed Guide

### 1. Running Individual Images

#### Backend API:
```bash
docker run -d \
  --name mediassist-api \
  -p 8000:8000 \
  -e AUTH0_DOMAIN=your-domain.auth0.com \
  -e AUTH0_AUDIENCE=https://api.mediassistai \
  -e DB_URL=your-database-url \
  -e TWILIO_ACCOUNT_SID=your-sid \
  -e TWILIO_AUTH_TOKEN=your-token \
  -e TWILIO_FROM_NUMBER=+1234567890 \
  -e GMAIL_ADDRESS=your-email \
  -e GMAIL_APP_PASSWORD=your-password \
  -e MAPS_API_KEY=your-key \
  -e GEMINI_API_KEY=your-key \
  hrithikesh11/mediassist-api:latest
```

#### Frontend Web:
```bash
docker run -d \
  --name mediassist-web \
  -p 3000:80 \
  hrithikesh11/mediassist-web:latest
```

**Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

### 2. Using Docker Compose (Recommended)

**File:** `infra/docker-compose.yml`

```bash
# Start all services
cd infra
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

---

### 3. Using Your Deployment Scripts

**Easiest way:**
```bash
# Local development (uses docker-compose)
./local-start.sh

# Stop
./local-stop.sh
```

---

## For Hackathon Deployment

**Don't run Docker locally!** Instead:

### Deploy to Render.com:
1. Go to https://render.com
2. New Web Service → "Deploy an existing image"
3. Image URL: `docker.io/hrithikesh11/mediassist-api:latest`
4. Add environment variables
5. Deploy!

Render will **pull and run your Docker image** automatically.

---

## Common Docker Commands

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# View logs
docker logs mediassist-api
docker logs -f mediassist-web

# Stop container
docker stop mediassist-api

# Remove container
docker rm mediassist-api

# Pull latest image
docker pull hrithikesh11/mediassist-api:latest

# Check image size
docker images | grep mediassist
```

---

## ⚠️ Important for Hackathon

**You do NOT need to run Docker locally!**

For hackathon submission:
1. ✅ Your images are already built and pushed
2. ✅ Deploy to Render.com (they run it for you)
3. ✅ Deploy frontend to Cloudflare Pages (static files)

**Docker is only needed for:**
- Testing locally (optional)
- Understanding the setup (optional)
- Production deployment (handled by Render.com)

---

## Quick Test

Want to test your images locally?

```bash
# Test API
docker run -p 8000:8000 \
  --env-file api/.env \
  hrithikesh11/mediassist-api:latest

# Open: http://localhost:8000/docs
```

**Ctrl+C to stop**

---

## Summary

**For hackathon:** You don't need to run Docker locally!
- Your images are ready
- Render.com will run them
- Just follow DEVPOST_SUBMISSION.md

**Want to test locally?**
- Use `./local-start.sh` (no Docker needed)
- Or use docker-compose (if you want Docker)
