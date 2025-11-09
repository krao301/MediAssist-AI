#!/bin/bash

# 🚀 MediAssist-AI Docker Quick Start Script
# This script builds and starts all Docker containers

set -e  # Exit on error

echo "🐳 Starting MediAssist-AI with Docker..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo -e "${BLUE}📋 Docker Configuration:${NC}"
echo "  - Production mode with full monitoring stack"
echo "  - Frontend: http://localhost:3000"
echo "  - API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Grafana: http://localhost:3001 (admin/admin)"
echo "  - Prometheus: http://localhost:9090"
echo ""

# Navigate to project root
cd "$(dirname "$0")"

# Check if .env.docker exists
if [ ! -f "api/.env.docker" ]; then
    echo -e "${YELLOW}⚠️  api/.env.docker not found!${NC}"
    echo "Creating from template..."
    cp api/.env.example api/.env.docker 2>/dev/null || echo "Please create api/.env.docker manually"
fi

echo -e "${BLUE}🏗️  Building Docker images...${NC}"
docker-compose -f infra/docker-compose.improved.yml build

echo ""
echo -e "${BLUE}🚀 Starting services...${NC}"
docker-compose -f infra/docker-compose.improved.yml up -d

echo ""
echo -e "${GREEN}✅ All services started successfully!${NC}"
echo ""
echo -e "${BLUE}📊 Service Status:${NC}"
docker-compose -f infra/docker-compose.improved.yml ps

echo ""
echo -e "${BLUE}📝 View logs with:${NC}"
echo "  docker-compose -f infra/docker-compose.improved.yml logs -f"
echo ""
echo -e "${BLUE}🛑 Stop services with:${NC}"
echo "  docker-compose -f infra/docker-compose.improved.yml down"
echo ""
echo -e "${GREEN}🎉 MediAssist-AI is ready!${NC}"
echo "Open http://localhost:3000 in your browser"
