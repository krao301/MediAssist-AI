#!/bin/bash

# 🚀 HACKATHON FAST DEPLOYMENT
# Deploy MediAssist-AI in 20 minutes

echo "════════════════════════════════════════════════════════"
echo "   🚀 MediAssist-AI Hackathon Deployment"
echo "   Domain: https://medi-assist.health"
echo "════════════════════════════════════════════════════════"
echo ""

# Step 1: Build frontend with production API URL
echo "📦 Step 1: Building frontend..."
cd web

# Create production env (will be updated after backend deploys)
cat > .env.production << 'EOF'
VITE_API_BASE=https://mediassist-api.onrender.com
VITE_AUTH0_DOMAIN=dev-bv4rdiy74pj3ybge.us.auth0.com
VITE_AUTH0_CLIENT_ID=k279MsPj5GZNhqEyNu5EhYpdPZu82krn
VITE_AUTH0_AUDIENCE=https://api.mediassistai
VITE_MAPS_API_KEY=AIzaSyDSYNQz5tkIRJPTiSbly-ng8Odgcqevqp4
EOF

npm run build
cd ..

echo "✅ Frontend built!"
echo ""

# Step 2: Verify Docker images exist
echo "🐳 Step 2: Checking Docker images..."
docker images | grep hrithikesh11/mediassist

echo ""
echo "════════════════════════════════════════════════════════"
echo "   📋 DEPLOYMENT INSTRUCTIONS"
echo "════════════════════════════════════════════════════════"
echo ""
echo "✅ Frontend built at: web/dist"
echo "✅ Docker images ready on Docker Hub"
echo ""
echo "🎯 NEXT: Follow these steps (copy-paste!):"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📱 STEP 1: Deploy Backend to Render.com (5 min)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Go to: https://render.com"
echo "2. Sign up with GitHub"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Select 'Deploy an existing image from a registry'"
echo "5. Image URL: docker.io/hrithikesh11/mediassist-api:latest"
echo "6. Name: mediassist-api"
echo "7. Add these environment variables (one by one):"
echo ""
cat << 'ENVEOF'
AUTH0_DOMAIN=dev-bv4rdiy74pj3ybge.us.auth0.com
AUTH0_AUDIENCE=https://api.mediassistai
AUTH0_JWKS=https://dev-bv4rdiy74pj3ybge.us.auth0.com/.well-known/jwks.json
DB_URL=postgresql://neondb_owner:npg_TJOy0MUH8YiA@ep-withered-unit-ad1fm90p-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
TWILIO_ACCOUNT_SID=ACea04dbf8586de660a5585e20d85c6668
TWILIO_AUTH_TOKEN=600665820ff037b203b653bfa9832550
TWILIO_FROM_NUMBER=+16363317602
GMAIL_ADDRESS=shritikesh8999@gmail.com
GMAIL_APP_PASSWORD=kxzfnaeizmkqibhb
MAPS_API_KEY=AIzaSyDSYNQz5tkIRJPTiSbly-ng8Odgcqevqp4
GEMINI_API_KEY=AIzaSyCEPUDlgsYj1i6MffQp_dxRGd4ztGCTtSE
ELEVENLABS_API_KEY=sk_70d4491d69eab0f41e5d1574263aa4b6b26510576835daab
ENVEOF
echo ""
echo "8. Click 'Create Web Service'"
echo "9. WAIT 5 minutes for deployment"
echo "10. COPY your Render URL (e.g., https://mediassist-api.onrender.com)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 STEP 2: Deploy Frontend to Cloudflare Pages (5 min)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Go to: https://dash.cloudflare.com"
echo "2. Login/Sign up"
echo "3. Click 'Workers & Pages'"
echo "4. Click 'Create application' → 'Pages' → 'Upload assets'"
echo "5. Project name: mediassist"
echo "6. Drag and drop the folder: web/dist"
echo "7. Click 'Deploy site'"
echo "8. WAIT 2 minutes"
echo "9. COPY your Cloudflare URL (e.g., https://mediassist.pages.dev)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 STEP 3: Update Frontend with Backend URL (5 min)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "After backend is deployed, update frontend:"
echo ""
echo "1. Edit web/.env.production:"
echo "   VITE_API_BASE=<YOUR_RENDER_URL>"
echo ""
echo "2. Rebuild frontend:"
echo "   cd web && npm run build && cd .."
echo ""
echo "3. Redeploy to Cloudflare Pages (drag new dist folder)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 STEP 4: Update Auth0 (2 min)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Go to: https://manage.auth0.com"
echo "2. Applications → Your App"
echo "3. Add your Cloudflare URL to:"
echo "   - Allowed Callback URLs"
echo "   - Allowed Logout URLs"
echo "   - Allowed Web Origins"
echo "4. Save"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 STEP 5: Submit to DevPost (3 min)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Go to: https://ub-hacking-fall-2025.devpost.com/"
echo "2. Fill in:"
echo "   - Live Demo: <YOUR_CLOUDFLARE_URL>"
echo "   - GitHub: https://github.com/krao301/MediAssist-AI"
echo "   - Description: (see README.md)"
echo "3. Submit!"
echo ""
echo "════════════════════════════════════════════════════════"
echo "✅ Ready to deploy! Start with Step 1!"
echo "════════════════════════════════════════════════════════"
echo ""
