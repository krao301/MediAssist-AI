#!/bin/bash

# 🧹 Project Cleanup for Hackathon Submission
# Removes development documentation, keeps only essential files

set -e

echo "🧹 Cleaning up MediAssist-AI for hackathon submission..."
echo ""

# Create backup directory
mkdir -p .backup
echo "📦 Creating backup in .backup/ directory..."

# Move development docs to backup
echo "📝 Moving development documentation to backup..."
mv AI_LEARNING_IMPLEMENTATION.md .backup/ 2>/dev/null || true
mv AI_LEARNING_QUICKREF.md .backup/ 2>/dev/null || true
mv AI_LEARNING_SYSTEM.md .backup/ 2>/dev/null || true
mv AI_TRAINING_STRATEGY.md .backup/ 2>/dev/null || true
mv API.md .backup/ 2>/dev/null || true
mv AUTH0_IMPLEMENTATION.md .backup/ 2>/dev/null || true
mv AUTH0_SETUP.md .backup/ 2>/dev/null || true
mv DATABASE_READY.md .backup/ 2>/dev/null || true
mv DATABASE_SESSION_FIX.md .backup/ 2>/dev/null || true
mv DEMO_CHEAT_SHEET.md .backup/ 2>/dev/null || true
mv DOCKER_FRONTEND_CONFIG.md .backup/ 2>/dev/null || true
mv DOCKER_GUIDE.md .backup/ 2>/dev/null || true
mv DOCKER_QUICKREF.md .backup/ 2>/dev/null || true
mv DOCKER_README.md .backup/ 2>/dev/null || true
mv DOCKER_SETUP_SUMMARY.md .backup/ 2>/dev/null || true
mv DOCKER_STARTING.md .backup/ 2>/dev/null || true
mv EMAIL_IMPLEMENTATION.md .backup/ 2>/dev/null || true
mv FINAL_SETUP_CHECKLIST.md .backup/ 2>/dev/null || true
mv FINAL_STATUS.md .backup/ 2>/dev/null || true
mv FIXES_APPLIED.md .backup/ 2>/dev/null || true
mv FIX_DOCKER_MALWARE.md .backup/ 2>/dev/null || true
mv FIX_DOCKER_MALWARE_WARNING.md .backup/ 2>/dev/null || true
mv FIX_LOGOUT.md .backup/ 2>/dev/null || true
mv GMAIL_SETUP.md .backup/ 2>/dev/null || true
mv HACKATHON_READY.md .backup/ 2>/dev/null || true
mv HARDCODED_SOLUTION.md .backup/ 2>/dev/null || true
mv IMPROVEMENTS_SUMMARY.md .backup/ 2>/dev/null || true
mv INSTALL_DOCKER.md .backup/ 2>/dev/null || true
mv NEW_FLOW_IMPLEMENTATION.md .backup/ 2>/dev/null || true
mv PHONE_CONFIG.md .backup/ 2>/dev/null || true
mv PITCH_DECK.md .backup/ 2>/dev/null || true
mv QUICK_START_AUTH0.md .backup/ 2>/dev/null || true
mv ROLE_BASED_AUTH.md .backup/ 2>/dev/null || true
mv START_HERE.md .backup/ 2>/dev/null || true
mv SYSTEM_STATUS.md .backup/ 2>/dev/null || true
mv TESTING.md .backup/ 2>/dev/null || true
mv TESTING_SUMMARY.md .backup/ 2>/dev/null || true
mv TWILIO_SETUP.md .backup/ 2>/dev/null || true
mv DEPLOYMENT_CHECKLIST.md .backup/ 2>/dev/null || true
mv START_DEPLOYMENT.md .backup/ 2>/dev/null || true

# Keep these important files:
# - README.md (main project documentation)
# - LICENSE
# - ARCHITECTURE.md (technical architecture)
# - DEPLOYMENT_GUIDE.md (deployment instructions)
# - DEVPOST_SUBMISSION.md (submission info)
# - HACKATHON_WINNING_STRATEGY.md (presentation tips)

# Clean up old scripts
echo "🗑️  Removing old/redundant scripts..."
rm -f start.ps1 2>/dev/null || true
rm -f start.sh 2>/dev/null || true
rm -f docker-dev.sh 2>/dev/null || true
rm -f docker-start.sh 2>/dev/null || true
rm -f docker-stop.sh 2>/dev/null || true

# Clean up API directory
echo "🗑️  Cleaning API directory..."
mv api/PROJECT_STATUS.md .backup/ 2>/dev/null || true
mv api/HYBRID_RAG_SUMMARY.md .backup/ 2>/dev/null || true
mv api/LLM_OPTIMIZATION_GUIDE.md .backup/ 2>/dev/null || true
mv api/QUICK_START.md .backup/ 2>/dev/null || true

# Clean up infra directory
echo "🗑️  Cleaning infra directory..."
mv infra/deploy-notes.md .backup/ 2>/dev/null || true

# Remove temporary files
echo "🗑️  Removing temporary files..."
rm -rf web/node_modules/.cache 2>/dev/null || true
rm -rf api/__pycache__ 2>/dev/null || true
rm -rf api/app/__pycache__ 2>/dev/null || true
rm -rf api/venv/lib/python*/site-packages/__pycache__ 2>/dev/null || true

# Clean Python cache
find api -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find api -type f -name "*.pyc" -delete 2>/dev/null || true
find api -type f -name "*.pyo" -delete 2>/dev/null || true

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📁 Project structure:"
echo "   ├── README.md              (Main documentation)"
echo "   ├── ARCHITECTURE.md        (Technical details)"
echo "   ├── DEPLOYMENT_GUIDE.md    (How to deploy)"
echo "   ├── DEVPOST_SUBMISSION.md  (DevPost info)"
echo "   ├── LICENSE                (MIT License)"
echo "   ├── Dockerfile.api         (Backend container)"
echo "   ├── Dockerfile.web         (Frontend container)"
echo "   ├── local-start.sh         (Run locally)"
echo "   ├── local-stop.sh          (Stop local)"
echo "   ├── deploy.sh              (Deploy script)"
echo "   ├── devpost.sh             (DevPost helper)"
echo "   ├── api/                   (Backend code)"
echo "   ├── web/                   (Frontend code)"
echo "   └── infra/                 (Docker compose)"
echo ""
echo "📦 Old files backed up to: .backup/"
echo ""
echo "🎯 Next steps:"
echo "   1. Review cleaned project"
echo "   2. Test locally: ./local-start.sh"
echo "   3. Deploy: Follow DEPLOYMENT_GUIDE.md"
echo "   4. Submit to DevPost!"
echo ""
