# 🚀 Quick Start Guide (No Docker Required!)

## ⚡ Start Your App RIGHT NOW (Without Docker)

Since you don't have Docker installed yet, use this method:

```bash
cd /Users/hrithikeshsankineni/Documents/MediAssist-AI

# Start everything with one command!
./local-start.sh
```

**That's it!** Your browser will automatically open http://localhost:5173

---

## 📊 What You Get

- ✅ **Frontend:** http://localhost:5173
- ✅ **Backend API:** http://localhost:8000
- ✅ **API Docs:** http://localhost:8000/docs

---

## 🛑 Stop Services

```bash
./local-stop.sh
```

---

## 📝 View Logs

```bash
# Backend logs
tail -f /tmp/mediassist-backend.log

# Frontend logs
tail -f /tmp/mediassist-frontend.log
```

---

## 🐳 Want to Use Docker Instead?

### Step 1: Install Docker Desktop

```bash
# Install with Homebrew
brew install --cask docker

# Wait for installation...
# Then launch Docker Desktop
open /Applications/Docker.app

# Wait for Docker to start (whale icon in menu bar)
```

### Step 2: Use Docker

Once Docker is running:

```bash
./docker-start.sh
```

Then open http://localhost:3000

---

## 🎯 For Your Hackathon Demo

### Option A: Local (No Docker) - Use This Now!

```bash
./local-start.sh
open http://localhost:5173
```

**Pros:**
- ✅ Works immediately
- ✅ No installation needed
- ✅ Fast startup

**Cons:**
- ❌ Less professional (no containerization)
- ❌ No monitoring dashboards

---

### Option B: Docker (Install First) - Better for Demo!

```bash
# 1. Install Docker Desktop (5 minutes)
brew install --cask docker
open /Applications/Docker.app

# 2. Wait for Docker to start

# 3. Run your app
./docker-start.sh
open http://localhost:3000
```

**Pros:**
- ✅ Professional containerized setup
- ✅ Prometheus + Grafana monitoring
- ✅ More impressive for judges
- ✅ Production-ready

**Cons:**
- ❌ Requires Docker installation
- ❌ Slightly slower startup

---

## 🆘 Troubleshooting

### Port Already in Use

```bash
# Kill whatever's on port 8000
lsof -ti:8000 | xargs kill -9

# Kill whatever's on port 5173
lsof -ti:5173 | xargs kill -9

# Then restart
./local-start.sh
```

### Backend Won't Start

```bash
# Check if virtual environment exists
ls api/venv

# If not, create it:
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Won't Start

```bash
# Check if node_modules exists
ls web/node_modules

# If not, install:
cd web
npm install
```

---

## 📊 Service Status

```bash
# Check what's running
lsof -ti:8000  # Backend
lsof -ti:5173  # Frontend

# View process details
ps aux | grep uvicorn  # Backend
ps aux | grep vite     # Frontend
```

---

## 🎓 Summary

**For immediate testing:**
```bash
./local-start.sh
```

**For impressive demo (after installing Docker):**
```bash
brew install --cask docker
# Wait for Docker Desktop to start...
./docker-start.sh
```

**To stop:**
```bash
./local-stop.sh   # For local
./docker-stop.sh  # For Docker
```

---

**Your app is ready to run! Choose your method above.** 🚀
