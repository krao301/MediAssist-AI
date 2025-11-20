#!/bin/bash

# 🚀 MediAssist-AI Frontend Deployment Script
# Builds and deploys frontend to Cloudflare Pages

set -e

echo "🎨 Building MediAssist-AI Frontend for Production..."
echo ""

cd "$(dirname "$0")/web"

# Check if .env.production exists
if [ ! -f ".env.production" ]; then
    echo "❌ Error: .env.production not found"
    echo "Please create web/.env.production with your production API URL"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Build for production
echo "🔨 Building production bundle..."
npm run build

echo ""
echo "✅ Build complete! Output in: web/dist"
echo ""
echo "📤 Next steps:"
echo ""
echo "Option 1: Deploy to Cloudflare Pages (Web UI)"
echo "  1. Go to: https://dash.cloudflare.com"
echo "  2. Workers & Pages → Create → Pages → Upload assets"
echo "  3. Drag and drop the 'web/dist' folder"
echo "  4. Project name: mediassist"
echo ""
echo "Option 2: Deploy using Wrangler CLI"
echo "  npx wrangler pages deploy dist --project-name=mediassist"
echo ""
echo "🌐 Your domain: https://medi-assist.health"
echo ""
