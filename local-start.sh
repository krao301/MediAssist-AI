#!/bin/bash

# 🚀 MediAssist-AI Local Start (No Docker Required)
# This script runs your app locally without Docker

set -e

echo "🚀 Starting MediAssist-AI locally (without Docker)..."
echo ""

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if backend is already running
if lsof -ti:8000 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Port 8000 is already in use. Killing existing process...${NC}"
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Check if frontend is already running
if lsof -ti:5173 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Port 5173 is already in use. Killing existing process...${NC}"
    lsof -ti:5173 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

echo -e "${BLUE}📋 Starting services:${NC}"
echo "  - Backend API: http://localhost:8000"
echo "  - Frontend: http://localhost:5173"
echo "  - API Docs: http://localhost:8000/docs"
echo ""

# Start backend
echo -e "${BLUE}🔧 Starting Backend API...${NC}"
cd "$(dirname "$0")/api"

if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found at api/venv${NC}"
    echo "Please create it first: cd api && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Start backend in background, redirect logs
source venv/bin/activate
nohup python -m uvicorn app.main:app --reload --port 8000 > /tmp/mediassist-backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"

# Give backend time to start
sleep 3

# Start frontend
echo -e "${BLUE}🎨 Starting Frontend...${NC}"
cd ../web

if [ ! -d "node_modules" ]; then
    echo -e "${RED}❌ node_modules not found${NC}"
    echo "Please install dependencies first: cd web && npm install"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Start frontend in background, redirect logs
nohup npm run dev > /tmp/mediassist-frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"

# Save PIDs for stop script
echo $BACKEND_PID > /tmp/mediassist-backend.pid
echo $FRONTEND_PID > /tmp/mediassist-frontend.pid

echo ""
echo -e "${GREEN}✅ All services started successfully!${NC}"
echo ""
echo -e "${BLUE}📊 Access your app:${NC}"
echo "  Frontend:  http://localhost:5173"
echo "  API:       http://localhost:8000"
echo "  API Docs:  http://localhost:8000/docs"
echo ""
echo -e "${BLUE}📝 View logs:${NC}"
echo "  Backend:  tail -f /tmp/mediassist-backend.log"
echo "  Frontend: tail -f /tmp/mediassist-frontend.log"
echo ""
echo -e "${BLUE}🛑 Stop services:${NC}"
echo "  ./local-stop.sh"
echo ""
echo -e "${BLUE}💡 Tip:${NC} Opening browser in 3 seconds..."
sleep 3
open http://localhost:5173

echo ""
echo -e "${GREEN}🎉 MediAssist-AI is running!${NC}"
