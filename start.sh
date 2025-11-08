#!/bin/bash

# MediAssist AI - Quick Start Script
# Usage: ./start.sh [backend|frontend|docker|all]

set -e

MODE=${1:-all}

start_backend() {
    echo "🚀 Starting Backend API..."
    cd api
    
    if [ ! -d ".venv" ]; then
        echo "Creating Python virtual environment..."
        python3 -m venv .venv
    fi
    
    source .venv/bin/activate
    pip install -q -r requirements.txt
    
    if [ ! -f ".env" ]; then
        echo "⚠️  No .env file found. Creating from example..."
        cp .env.example .env
        echo "📝 Please edit api/.env with your API keys before continuing."
        exit 1
    fi
    
    echo "✅ Backend ready on http://localhost:8000"
    uvicorn app.main:app --reload --port 8000
}

start_frontend() {
    echo "🚀 Starting Frontend PWA..."
    cd web
    
    if [ ! -d "node_modules" ]; then
        echo "Installing npm dependencies..."
        npm install
    fi
    
    if [ ! -f ".env" ]; then
        echo "⚠️  No .env file found. Creating from example..."
        cp .env.example .env
    fi
    
    echo "✅ Frontend ready on http://localhost:5173"
    npm run dev
}

start_docker() {
    echo "🐳 Starting Docker services..."
    cd infra
    docker-compose up -d
    echo "✅ Services started:"
    echo "   - PostgreSQL: localhost:5432"
    echo "   - Redis: localhost:6379"
    echo "   - API: http://localhost:8000"
}

case $MODE in
    backend)
        start_backend
        ;;
    frontend)
        start_frontend
        ;;
    docker)
        start_docker
        ;;
    all)
        echo "🎯 Starting all services..."
        echo ""
        echo "Option 1: Docker (Recommended)"
        echo "  ./start.sh docker"
        echo ""
        echo "Option 2: Manual"
        echo "  Terminal 1: ./start.sh backend"
        echo "  Terminal 2: ./start.sh frontend"
        echo ""
        echo "Choose your method and run the appropriate command."
        ;;
    *)
        echo "Usage: ./start.sh [backend|frontend|docker|all]"
        exit 1
        ;;
esac
