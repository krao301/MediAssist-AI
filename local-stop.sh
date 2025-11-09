#!/bin/bash

# 🛑 MediAssist-AI Local Stop
# This script stops the locally running services

echo "🛑 Stopping MediAssist-AI services..."

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Stop using saved PIDs
if [ -f /tmp/mediassist-backend.pid ]; then
    BACKEND_PID=$(cat /tmp/mediassist-backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID 2>/dev/null || true
        echo -e "${GREEN}✅ Backend stopped${NC}"
    fi
    rm /tmp/mediassist-backend.pid
fi

if [ -f /tmp/mediassist-frontend.pid ]; then
    FRONTEND_PID=$(cat /tmp/mediassist-frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID 2>/dev/null || true
        echo -e "${GREEN}✅ Frontend stopped${NC}"
    fi
    rm /tmp/mediassist-frontend.pid
fi

# Force kill any remaining processes on ports
if lsof -ti:8000 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Cleaning up port 8000...${NC}"
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
fi

if lsof -ti:5173 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Cleaning up port 5173...${NC}"
    lsof -ti:5173 | xargs kill -9 2>/dev/null || true
fi

echo ""
echo -e "${GREEN}✅ All services stopped!${NC}"
