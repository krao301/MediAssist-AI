#!/bin/bash

# 🛑 MediAssist-AI Docker Stop Script
# This script stops all Docker containers

set -e

echo "🛑 Stopping MediAssist-AI Docker containers..."

cd "$(dirname "$0")"

# Stop and remove containers
docker-compose -f infra/docker-compose.improved.yml down

echo "✅ All services stopped successfully!"
echo ""
echo "To remove volumes as well, run:"
echo "  docker-compose -f infra/docker-compose.improved.yml down -v"
