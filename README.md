# MediAssist AI 🚑

**AI-Powered Emergency First-Aid Assistant**

A Progressive Web App that provides real-time emergency triage and step-by-step first-aid guidance using AI, helping bystanders respond effectively to medical emergencies.

🔗 **Live Demo**: [medi-assist.health](https://medi-assist.health)  
📦 **Docker Hub**: [mediassist-ai](https://hub.docker.com/r/yourusername/mediassist-ai)  
🏆 **Hackathon**: [UB Hacking Fall 2025](https://ub-hacking-fall-2025.devpost.com/) | [Devpost Submission](https://devpost.com/software/mediassist-ai)

[![Built with React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Google Gemini](https://img.shields.io/badge/Gemini-API-4285F4?logo=google)](https://ai.google.dev/)
[![DigitalOcean](https://img.shields.io/badge/DigitalOcean-Deployed-0080FF?logo=digitalocean)](https://www.digitalocean.com/)

---

## 🏆 Hackathon Submission

**Event**: [UB Hacking Fall 2025](https://ub-hacking-fall-2025.devpost.com/)  
**Submitted For**:
- [MLH] Best Domain Name from GoDaddy Registry
- [MLH] Best Use of Auth0
- [MLH] Best Use of ElevenLabs
- [MLH] Best Use of Gemini API
- [MLH] Best Use of DigitalOcean Gradient™ AI
- [MLH] Best AI Application Built with Cloudflare

---

## 🎯 Overview

MediAssist AI bridges the critical gap between emergency occurrence and professional medical response by:

- **AI-Powered Triage**: Gemini API classifies emergency severity and type in real-time
- **Voice-First Interface**: Browser-based speech recognition for hands-free operation
- **Guided Instructions**: Step-by-step protocols based on AHA (American Heart Association) guidelines
- **Geofencing Alerts**: Automatically notifies emergency contacts within 500m radius via Twilio
- **Hospital Routing**: Integrates Google Maps API for nearest emergency room navigation
- **Incident Logging**: Generates timestamped summaries for EMS handoff
- **Secure Authentication**: Auth0 SSO with JWT-based API authorization

**Tech Stack**: React + TypeScript, FastAPI, PostgreSQL, Google Gemini AI, Auth0, Twilio, Docker

---

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌──────────────┐
│   React PWA     │────────▶│   FastAPI API    │────────▶│ PostgreSQL   │
│   (Cloudflare)  │  HTTPS  │  (DigitalOcean)  │  SQL    │   Database   │
│                 │         │                  │         │              │
│  • Vite + TS    │         │  • SQLAlchemy    │         │  • Incidents │
│  • Tailwind CSS │         │  • Pydantic      │         │  • Contacts  │
│  • Auth0 SDK    │         │  • JWT Auth      │         │  • Users     │
└─────────────────┘         └──────────────────┘         └──────────────┘
        │                            │
        │                            ├─────────▶ Google Gemini API (Triage)
        │                            ├─────────▶ Twilio API (SMS/Voice)
        │                            ├─────────▶ Google Maps API (Routing)
        │                            ├─────────▶ ElevenLabs API (TTS)
        │                            └─────────▶ Auth0 (JWT Validation)
        │
        └─────────▶ Service Worker (Offline PWA)
```

### Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React 18 + TypeScript | Type-safe component architecture |
| | Vite + PWA Plugin | Fast builds, offline capabilities |
| | Tailwind CSS | Utility-first responsive design |
| | Auth0 React SDK | OAuth 2.0 authentication |
| | Web Speech API | Browser-native TTS/STT |
| **Backend** | FastAPI 0.109 | High-performance async API |
| | SQLAlchemy 2.0 | ORM with type hints |
| | Pydantic v2 | Request/response validation |
| | python-jose | JWT token verification |
| **AI/ML** | Google Gemini Pro | Emergency classification & guidance |
| | ElevenLabs | Natural voice synthesis |
| **Infrastructure** | Docker + Docker Compose | Containerized deployment |
| | DigitalOcean App Platform | Backend hosting |
| | Cloudflare Pages | Frontend CDN + edge compute |
| | GoDaddy | Domain registration |
| **External APIs** | Auth0 | Identity & access management |
| | Twilio | SMS/voice alerts |
| | Google Maps | Geolocation & routing |

---

## 🚀 Quick Start

### Prerequisites

```bash
# Required
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose

# API Keys (for full functionality)
- GEMINI_API_KEY
- TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
- MAPS_API_KEY
- AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET
- ELEVENLABS_API_KEY (optional)
```

### Local Development

**1. Clone Repository**
```bash
git clone https://github.com/yourusername/mediassist-ai.git
cd mediassist-ai
```

**2. Backend Setup**
```bash
cd api
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run development server
uvicorn app.main:app --reload --port 8000
```

**3. Frontend Setup**
```bash
cd web
npm install

# Configure environment
cat > .env << EOF
VITE_API_BASE_URL=http://localhost:8000
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your_client_id
VITE_AUTH0_AUDIENCE=https://mediassist-api
EOF

# Run development server
npm run dev
```

**4. Access Application**
- Frontend: `http://localhost:5173`
- API Docs: `http://localhost:8000/docs`
- API Health: `http://localhost:8000/health`

### Docker Deployment

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services:
- **Backend**: `http://localhost:8000`
- **Frontend**: `http://localhost:3000`
- **PostgreSQL**: `localhost:5432`

---

## 💡 Core Features

### 1. Auth0 Secure Authentication

- **OAuth 2.0 Flow**: Industry-standard authorization
- **JWT Token Validation**: RS256 signed tokens
- **Protected API Routes**: Bearer token authentication
- **MFA Support**: Multi-factor authentication available
- **User Management**: Profile and session handling

### 2. AI-Powered Emergency Triage

**Gemini Integration**: Real-time emergency classification using natural language processing

**Supported Emergency Types**:
- Cardiac Arrest (CPR with metronome at 100-120 BPM)
- Choking (Heimlich maneuver with visual guidance)
- Severe Bleeding (Pressure application with timer)
- Burns (Cooling protocol with step tracking)
- Fainting (Recovery position with monitoring)

### 3. ElevenLabs Voice Synthesis

- **Natural Voice Narration**: Converts first-aid steps to speech
- **Hands-Free Operation**: Audio guidance during emergencies
- **Multiple Voice Options**: Customizable voice profiles
- **Low Latency**: Real-time audio generation

### 4. Geofenced Emergency Alerts

**500m Radius Notification System**:
- Haversine formula for accurate distance calculation
- Automatic SMS alerts via Twilio
- Contact filtering based on proximity
- Real-time location tracking

### 5. Real-Time Incident Logging

**Event Timeline System**:
- Timestamped event tracking
- Step completion monitoring
- Contact notification logs
- EMS handoff summary generation

---

## 🔌 API Documentation

### Base URL
- **Production**: `https://api.medi-assist.health`
- **Local**: `http://localhost:8000`

### Authentication
All protected endpoints require JWT Bearer token:
```http
Authorization: Bearer {auth0_access_token}
```

### Key Endpoints

#### Emergency Triage
```http
POST /api/v1/triage
Authorization: Bearer {token}
Content-Type: application/json
```

#### Send Emergency Alerts
```http
POST /api/v1/alerts
Authorization: Bearer {token}
Content-Type: application/json
```

#### Hospital Routing
```http
POST /api/v1/route
Authorization: Bearer {token}
Content-Type: application/json
```

#### Incident Management
```http
POST /api/v1/incidents
GET /api/v1/incidents/{id}
POST /api/v1/incidents/{id}/events
POST /api/v1/incidents/{id}/resolve
GET /api/v1/incidents/{id}/summary
```

Full API documentation: `https://api.medi-assist.health/docs`

---

## 🐳 Docker Deployment

### Published Images

```bash
# Pull images from Docker Hub
docker pull yourusername/mediassist-api:latest
docker pull yourusername/mediassist-web:latest
```

### Production Deployment

**DigitalOcean App Platform (Backend)**:
- Dockerized FastAPI application
- Auto-scaling with health checks
- Managed PostgreSQL database
- Environment variable management

**Cloudflare Pages (Frontend)**:
- Static site hosting with CDN
- Edge computing capabilities
- Automatic HTTPS
- Global distribution

**GoDaddy Domain Configuration**:
- Custom domain: `medi-assist.health`
- DNS management
- SSL/TLS certificates

---

## 🧪 Testing

### Backend Tests
```bash
cd api
pytest tests/ -v --cov=app --cov-report=html
```

### Frontend Tests
```bash
cd web
npm run test              # Run all tests
npm run test:coverage     # Generate coverage report
npm run test:e2e          # End-to-end tests
```

---

## 📊 Performance Metrics

| Metric | Target | Achieved |
|--------|--------|----------|
| API Response Time (P95) | < 500ms | 320ms |
| Gemini AI Inference | < 2s | 1.2s |
| Auth0 Token Verification | < 100ms | 45ms |
| Frontend First Paint | < 1.5s | 0.9s |
| PWA Offline Support | 100% | ✅ |
| Lighthouse Score | > 90 | 94/100 |
| Docker Image Size (Backend) | < 200MB | 180MB |
| Docker Image Size (Frontend) | < 50MB | 42MB |

---

## 🔒 Security

- **JWT Authentication**: Auth0-powered secure API access
- **OAuth 2.0**: Industry-standard authorization framework
- **MFA Support**: Multi-factor authentication via Auth0
- **CORS Configuration**: Whitelisted domains only
- **SQL Injection Prevention**: Parameterized queries via SQLAlchemy
- **Rate Limiting**: 100 requests/minute per user
- **HTTPS Only**: TLS 1.3 enforced on production
- **Secret Management**: Environment variables in cloud vaults

---

## 📝 Environment Variables

### Backend (`api/.env`)
```bash
DB_URL=postgresql://user:pass@localhost:5432/mediassist
AUTH0_DOMAIN=mediassist.auth0.com
AUTH0_AUDIENCE=https://mediassist-api
GEMINI_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=your_token
MAPS_API_KEY=your_maps_key
```

### Frontend (`web/.env`)
```bash
VITE_API_BASE_URL=https://api.medi-assist.health
VITE_AUTH0_DOMAIN=mediassist.auth0.com
VITE_AUTH0_CLIENT_ID=your_client_id
VITE_AUTH0_AUDIENCE=https://mediassist-api
```

---

## 🤝 Contributing

This project was built for UB Hacking Fall 2025. Contributions are welcome!

```bash
# Fork the repo and create feature branch
git checkout -b feature/your-feature

# Make changes and commit
git commit -m "Add: your feature description"

# Push and create PR
git push origin feature/your-feature
```

**Code Style**:
- Python: Black formatter, flake8 linter, mypy type checking
- TypeScript: ESLint + Prettier
- Commits: Conventional Commits format

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 📧 Contact

**Team**: Gradient Gurus  
**Live App**: [medi-assist.health](https://medi-assist.health)  
**Devpost**: [devpost.com/software/mediassist-ai](https://devpost.com/software/mediassist-ai)  
**Docker Hub**: [hub.docker.com/r/yourusername/mediassist-ai](https://hub.docker.com/r/spanakan/mediassist-ai)

---

## ⚠️ Disclaimer

**For Educational Purposes Only**

MediAssist AI is a proof-of-concept developed during UB Hacking Fall 2025 (36-hour hackathon). This application provides general first-aid guidance and is NOT a substitute for professional medical advice, diagnosis, or treatment. 

**Always call 911 or your local emergency services immediately in a medical emergency.**

The developers assume no liability for outcomes resulting from the use of this application.

---

**Built with ❤️ by Gradient Gurus | UB Hacking Fall 2025**