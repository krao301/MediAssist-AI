#!/bin/bash

# 🚀 Quick Frontend Update and Build for Deployment
# Updates API URL and rebuilds frontend

set -e

echo "🚀 Preparing Frontend for Deployment"
echo "═══════════════════════════════════════"
echo ""

# Check if Render API URL is provided
RENDER_API_URL=${1:-"https://mediassist-api.onrender.com"}

echo "📝 Updating frontend configuration..."
echo "   Backend API: $RENDER_API_URL"

# Create production environment file
cat > web/.env.production << EOF
VITE_API_BASE=$RENDER_API_URL
VITE_AUTH0_DOMAIN=dev-bv4rdiy74pj3ybge.us.auth0.com
VITE_AUTH0_CLIENT_ID=k279MsPj5GZNhqEyNu5EhYpdPZu82krn
VITE_AUTH0_AUDIENCE=https://api.mediassistai
VITE_MAPS_API_KEY=AIzaSyDSYNQz5tkIRJPTiSbly-ng8Odgcqevqp4
EOF

echo "   ✅ Configuration updated"
echo ""

# Build frontend
echo "🔨 Building frontend..."
cd web
npm run build
cd ..

echo ""
echo "═══════════════════════════════════════"
echo "✅ Frontend ready for deployment!"
echo ""
echo "📦 Built files location:"
echo "   web/dist/"
echo ""
echo "🚀 Next steps:"
echo "   1. Go to: https://dash.cloudflare.com"
echo "   2. Workers & Pages → Create → Upload Assets"
echo "   3. Upload the 'web/dist' folder"
echo "   4. Project name: mediassist"
echo "   5. Deploy!"
echo ""
echo "📝 Or use Wrangler CLI:"
echo "   cd web"
echo "   npx wrangler pages deploy dist --project-name=mediassist"
echo ""
echo "🌐 Your backend API: $RENDER_API_URL"
echo ""
