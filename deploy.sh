#!/bin/bash

# 🚀 MediAssist-AI Complete Deployment Script
# Deploys both backend and frontend

set -e

echo "════════════════════════════════════════════════════════"
echo "   🚀 MediAssist-AI Hackathon Deployment"
echo "   Domain: https://medi-assist.health"
echo "════════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Build and Push Docker Images
echo -e "${BLUE}📦 Step 1: Building and pushing Docker images...${NC}"
echo ""

echo "Building API image..."
docker build -f Dockerfile.api -t hrithikesh11/mediassist-api:latest .

echo "Building Web image..."
docker build -f Dockerfile.web -t hrithikesh11/mediassist-web:latest .

echo "Pushing to Docker Hub..."
docker push hrithikesh11/mediassist-api:latest &
docker push hrithikesh11/mediassist-web:latest &
wait

echo -e "${GREEN}✅ Docker images pushed!${NC}"
echo ""

# Step 2: Build Frontend
echo -e "${BLUE}🎨 Step 2: Building frontend for production...${NC}"
echo ""

cd web
npm run build
cd ..

echo -e "${GREEN}✅ Frontend built!${NC}"
echo ""

# Step 3: Instructions
echo "════════════════════════════════════════════════════════"
echo -e "${YELLOW}📋 Next Steps - Follow DEPLOYMENT_GUIDE.md${NC}"
echo "════════════════════════════════════════════════════════"
echo ""
echo -e "${BLUE}1. Deploy Backend to Render.com:${NC}"
echo "   → Go to: https://render.com"
echo "   → New Web Service → Deploy existing image"
echo "   → Image: docker.io/hrithikesh11/mediassist-api:latest"
echo "   → Add all environment variables (see DEPLOYMENT_GUIDE.md)"
echo ""
echo -e "${BLUE}2. Deploy Frontend to Cloudflare Pages:${NC}"
echo "   → Go to: https://dash.cloudflare.com"
echo "   → Workers & Pages → Create → Upload assets"
echo "   → Upload the 'web/dist' folder"
echo ""
echo -e "${BLUE}3. Configure DNS in Cloudflare:${NC}"
echo "   → Add CNAME: @ → mediassist.pages.dev"
echo "   → Add CNAME: api → mediassist-api.onrender.com"
echo ""
echo -e "${BLUE}4. Update Auth0:${NC}"
echo "   → Add https://medi-assist.health to callback URLs"
echo ""
echo -e "${GREEN}✅ Ready for deployment!${NC}"
echo ""
echo "📖 Full guide: DEPLOYMENT_GUIDE.md"
echo ""
