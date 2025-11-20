#!/bin/bash

# 🔐 SECURITY CLEANUP - Remove Exposed Credentials
# This script removes sensitive data from documentation and git history

set -e

echo "🔐 SECURITY CLEANUP"
echo "════════════════════════════════════════"
echo ""

# Step 1: Remove credentials from documentation
echo "📝 Step 1: Sanitizing documentation files..."

# Replace credentials with placeholders in DEPLOYMENT_GUIDE.md
if [ -f "DEPLOYMENT_GUIDE.md" ]; then
    sed -i.bak 's/npg_TJOy0MUH8YiA/YOUR_NEON_PASSWORD_HERE/g' DEPLOYMENT_GUIDE.md
    sed -i.bak 's/ACea04dbf8586de660a5585e20d85c6668/YOUR_TWILIO_SID_HERE/g' DEPLOYMENT_GUIDE.md
    sed -i.bak 's/600665820ff037b203b653bfa9832550/YOUR_TWILIO_TOKEN_HERE/g' DEPLOYMENT_GUIDE.md
    sed -i.bak 's/kxzfnaeizmkqibhb/YOUR_GMAIL_APP_PASSWORD_HERE/g' DEPLOYMENT_GUIDE.md
    sed -i.bak 's/shritikesh8999@gmail.com/YOUR_GMAIL_ADDRESS/g' DEPLOYMENT_GUIDE.md
    sed -i.bak 's/sankinenihrithikesh@gmail.com/YOUR_EMAIL_HERE/g' DEPLOYMENT_GUIDE.md
    sed -i.bak 's/AIzaSyDSYNQz5tkIRJPTiSbly-ng8Odgcqevqp4/YOUR_MAPS_API_KEY_HERE/g' DEPLOYMENT_GUIDE.md
    sed -i.bak 's/AIzaSyCEPUDlgsYj1i6MffQp_dxRGd4ztGCTtSE/YOUR_GEMINI_API_KEY_HERE/g' DEPLOYMENT_GUIDE.md
    sed -i.bak 's/sk_70d4491d69eab0f41e5d1574263aa4b6b26510576835daab/YOUR_ELEVENLABS_API_KEY_HERE/g' DEPLOYMENT_GUIDE.md
    rm -f DEPLOYMENT_GUIDE.md.bak
    echo "  ✅ DEPLOYMENT_GUIDE.md sanitized"
fi

# Replace credentials in DEVPOST_SUBMISSION.md
if [ -f "DEVPOST_SUBMISSION.md" ]; then
    sed -i.bak 's/npg_TJOy0MUH8YiA/YOUR_NEON_PASSWORD_HERE/g' DEVPOST_SUBMISSION.md
    sed -i.bak 's/ACea04dbf8586de660a5585e20d85c6668/YOUR_TWILIO_SID_HERE/g' DEVPOST_SUBMISSION.md
    sed -i.bak 's/600665820ff037b203b653bfa9832550/YOUR_TWILIO_TOKEN_HERE/g' DEVPOST_SUBMISSION.md
    sed -i.bak 's/kxzfnaeizmkqibhb/YOUR_GMAIL_APP_PASSWORD_HERE/g' DEVPOST_SUBMISSION.md
    sed -i.bak 's/shritikesh8999@gmail.com/YOUR_GMAIL_ADDRESS/g' DEVPOST_SUBMISSION.md
    sed -i.bak 's/sankinenihrithikesh@gmail.com/YOUR_EMAIL_HERE/g' DEVPOST_SUBMISSION.md
    sed -i.bak 's/AIzaSyDSYNQz5tkIRJPTiSbly-ng8Odgcqevqp4/YOUR_MAPS_API_KEY_HERE/g' DEVPOST_SUBMISSION.md
    sed -i.bak 's/AIzaSyCEPUDlgsYj1i6MffQp_dxRGd4ztGCTtSE/YOUR_GEMINI_API_KEY_HERE/g' DEVPOST_SUBMISSION.md
    sed -i.bak 's/sk_70d4491d69eab0f41e5d1574263aa4b6b26510576835daab/YOUR_ELEVENLABS_API_KEY_HERE/g' DEVPOST_SUBMISSION.md
    rm -f DEVPOST_SUBMISSION.md.bak
    echo "  ✅ DEVPOST_SUBMISSION.md sanitized"
fi

# Step 2: Remove .env.docker from git (it should not be tracked)
echo ""
echo "🗑️  Step 2: Removing .env.docker from git..."
git rm --cached api/.env.docker 2>/dev/null || echo "  ℹ️  .env.docker not in git"

# Step 3: Remove docker-compose.yml with credentials
echo ""
echo "🗑️  Step 3: Sanitizing docker-compose.yml..."
if [ -f "infra/docker-compose.yml" ]; then
    sed -i.bak 's/npg_TJOy0MUH8YiA/${DB_PASSWORD}/g' infra/docker-compose.yml
    rm -f infra/docker-compose.yml.bak
    echo "  ✅ docker-compose.yml sanitized"
fi

# Step 4: Update .gitignore
echo ""
echo "📝 Step 4: Updating .gitignore..."
cat >> .gitignore << 'EOF'

# Environment files with credentials
api/.env
api/.env.docker
api/.env.local
web/.env
web/.env.local
web/.env.production

# Deployment guides with credentials
DEPLOYMENT_GUIDE_PRIVATE.md
DEVPOST_SUBMISSION_PRIVATE.md
EOF
echo "  ✅ .gitignore updated"

echo ""
echo "════════════════════════════════════════"
echo "✅ Security cleanup complete!"
echo ""
echo "⚠️  IMPORTANT NEXT STEPS:"
echo ""
echo "1. ROTATE YOUR CREDENTIALS (Do this NOW!):"
echo "   - Neon Database: Reset password in Neon dashboard"
echo "   - Twilio: Rotate auth token in Twilio console"
echo "   - Gmail: Generate new app password"
echo "   - Google Maps API: Restrict/rotate in Google Cloud"
echo "   - Gemini API: Rotate in Google AI Studio"
echo "   - ElevenLabs: Rotate in ElevenLabs dashboard"
echo ""
echo "2. Update your local .env files with new credentials"
echo ""
echo "3. Commit changes:"
echo "   git add ."
echo "   git commit -m 'Security: Remove exposed credentials'"
echo "   git push"
echo ""
echo "4. For hackathon deployment:"
echo "   - Use environment variables in Render.com"
echo "   - DO NOT commit .env files"
echo "   - DO NOT include credentials in documentation"
echo ""
