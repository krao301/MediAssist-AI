# 🐳 Docker Installation Guide for macOS

## You Don't Have Docker Installed Yet!

No worries - here's how to install it.

---

## Option 1: Docker Desktop (Recommended - Easiest)

### Install with Homebrew (5 minutes):

```bash
# Install Docker Desktop
brew install --cask docker

# Wait for installation to complete...
# Then launch Docker Desktop from Applications folder
# Or use:
open /Applications/Docker.app
```

**After installation:**
1. Docker Desktop will open
2. Wait for "Docker Desktop is running" message
3. You'll see a whale icon in your menu bar
4. Then you can run: `./docker-start.sh`

---

## Option 2: Manual Download (Alternative)

1. Go to: https://www.docker.com/products/docker-desktop
2. Download Docker Desktop for Mac (Apple Silicon or Intel)
3. Open the `.dmg` file
4. Drag Docker to Applications folder
5. Open Docker from Applications
6. Wait for it to start (whale icon in menu bar)

---

## ⚡ Quick Alternative: Run Without Docker (Right Now!)

**Since you don't have Docker yet, let's run your app the traditional way:**

### Terminal 1 - Start Backend:

```bash
cd /Users/hrithikeshsankineni/Documents/MediAssist-AI/api
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

### Terminal 2 - Start Frontend:

```bash
cd /Users/hrithikeshsankineni/Documents/MediAssist-AI/web
npm run dev
```

### Then open:
- Frontend: http://localhost:5173
- API: http://localhost:8000

---

## Verify Docker Installation

After installing Docker Desktop, verify it works:

```bash
# Check Docker is installed
docker --version

# Should show: Docker version 24.x.x or similar

# Check Docker is running
docker ps

# Should show: (empty list or running containers)

# Test Docker works
docker run hello-world
```

---

## Then Use Docker

Once Docker is installed and running:

```bash
cd /Users/hrithikeshsankineni/Documents/MediAssist-AI

# Start everything with Docker
./docker-start.sh

# Open browser
open http://localhost:3000
```

---

## Why Docker Desktop Takes Time to Install

- **Size:** ~500MB download
- **First launch:** Takes 2-3 minutes to initialize
- **Worth it:** Consistent environment, easy deployment, professional setup

---

## Current Status

❌ Docker not installed
✅ Homebrew installed (can use to install Docker)
✅ Your app works locally without Docker

**Recommendation:** Install Docker Desktop now for your hackathon demo, but use local setup for immediate testing.

---

## Install Docker Now?

Run this command:

```bash
brew install --cask docker
```

Then wait for it to complete, launch Docker Desktop, and run `./docker-start.sh`

---

**Need to demo NOW? Use the "Run Without Docker" section above! ⚡**
