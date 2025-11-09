#!/bin/bash

# 🔧 MediAssist-AI Development Docker Script
# This script starts services with hot-reload for development

set -e

echo "🔧 Starting MediAssist-AI in DEVELOPMENT mode..."
echo ""

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo -e "${BLUE}📋 Development Configuration:${NC}"
echo "  - Hot-reload enabled for API and Web"
echo "  - Frontend: http://localhost:5173 (Vite dev server)"
echo "  - API: http://localhost:8000 (with --reload)"
echo "  - Source code mounted as volumes"
echo ""

cd "$(dirname "$0")"

if [ ! -f "api/.env.docker" ]; then
    echo -e "${YELLOW}⚠️  api/.env.docker not found!${NC}"
    echo "Creating from template..."
    cp api/.env.example api/.env.docker 2>/dev/null || echo "Please create api/.env.docker manually"
fi

echo -e "${BLUE}🏗️  Building development images...${NC}"
docker-compose -f infra/docker-compose.dev.yml build

echo ""
echo -e "${BLUE}🚀 Starting development services...${NC}"
docker-compose -f infra/docker-compose.dev.yml up

# Note: Not using -d so we can see logs
# Use Ctrl+C to stop
