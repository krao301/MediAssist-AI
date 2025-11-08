# MediAssist AI 🚑

**Emergency First-Aid Coaching with AI-Powered Triage**

Built for UB Hacking Fall 2025

## 🎯 What It Does

MediAssist AI is a **Progressive Web App** that transforms bystanders into lifesavers during medical emergencies:

1. **SOS Button**: Tap the large red button → Describe emergency via voice or text
2. **AI Triage**: Google Gemini classifies emergency type & severity (cardiac arrest, choking, bleeding, burns, fainting)
3. **Step-by-Step Guidance**: Evidence-based first aid with timers and CPR metronome
4. **Auto-Alert Contacts**: Sends SMS/voice alerts to trusted contacts within 500m (geofence)
5. **Hospital Routing**: Shows nearest emergency room with Google Maps
6. **Incident Summary**: Generates timeline for EMS handoff

**Demo**: [Watch Video](#) | **Live**: [mediassistai.xyz](#)

---

## 🏆 Sponsor Prize Tracks

| Sponsor | Integration | Prize Track |
|---------|-------------|-------------|
| **Auth0** | SSO login with MFA | Best Use of Auth0 |
| **Google Gemini** | Emergency triage & classification | Best Use of Gemini API |
| **ElevenLabs** | Text-to-speech for step narration | Best AI Voice Integration |
| **DigitalOcean** | App Platform + GPU inference | Best Use of Gradient AI |
| **Vultr** | Backend hosting | Best Use of Vultr Cloud |
| **Cloudflare** | Edge workers for alerts | Best Use of Cloudflare |
| **GoDaddy** | Custom domain | Best Use of GoDaddy Registry |

---

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌────────────┐
│  React PWA  │─────▶│  FastAPI     │─────▶│ PostgreSQL │
│  (Vite +    │      │  (Python)    │      │            │
│   Tailwind) │      │              │      │            │
└─────────────┘      └──────────────┘      └────────────┘
      │                     │
      │                     ├─────▶ Google Gemini API
      │                     ├─────▶ Twilio SMS/Voice
      │                     ├─────▶ Google Maps API
      │                     └─────▶ Auth0 JWT
      │
      └─────▶ Web Speech API (browser TTS/STT)
```

### Tech Stack

**Frontend**:
- React 18 + TypeScript
- React Router v6
- Tailwind CSS
- Vite PWA (Service Workers)
- Web Speech API (TTS/STT)
- Axios (API client)

**Backend**:
- FastAPI 0.109
- SQLAlchemy 2.0
- PostgreSQL / SQLite
- Google Generative AI (Gemini)
- Twilio SDK
- python-jose (Auth0 JWT)

**Infrastructure**:
- Docker + docker-compose
- DigitalOcean App Platform
- Cloudflare Workers (optional)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or use SQLite for dev)
- API Keys: Gemini, Twilio, Google Maps, Auth0 (optional)

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/mediassist-ai.git
cd mediassist-ai
```

### 2. Backend (API)

```bash
cd api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
# Database
DB_URL=sqlite:///./mediassist.db  # or postgresql://user:pass@localhost/mediassist

# AI
GEMINI_API_KEY=your_gemini_api_key_here

# Twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_NUMBER=+1234567890

# Maps
MAPS_API_KEY=your_google_maps_key

# Optional: Auth0
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_AUDIENCE=https://mediassist-api
EOF

# Run server
uvicorn app.main:app --reload --port 8000
```

API will be available at: `http://localhost:8000`  
Docs: `http://localhost:8000/docs`

### 3. Frontend (Web)

```bash
cd ../web
npm install

# Create .env
echo "VITE_API_BASE_URL=http://localhost:8000" > .env

# Run dev server
npm run dev
```

App will be available at: `http://localhost:5173`

### 4. Docker (All Services)

```bash
cd ../infra
docker-compose up -d
```

Starts PostgreSQL, Redis, and API on ports 5432, 6379, 8000.

---

## 📖 How It Works

### 1. Emergency Flow

```
User taps SOS → Voice input → AI triage → Steps appear → Timer starts
                                              ↓
                            Contacts within 500m get SMS alert
                                              ↓
                           Hospital route displayed on map
                                              ↓
                            End incident → Summary timeline
```

### 2. AI Triage (Gemini API)

**Prompt Engineering**:
```python
"""
Analyze this emergency description: "{user_input}"
Location: {country}
Age group: {age_group}

Classify as:
- Type: cardiac_arrest, choking, severe_bleeding, burn, fainting, other
- Severity: critical, serious, moderate, minor

Provide step-by-step first aid instructions with time estimates.
"""
```

**Knowledge Base**: Backed by AHA (American Heart Association) protocols:
- **Cardiac Arrest**: Check responsiveness → Call 911 → Start CPR (30:2) → Use AED
- **Choking**: Encourage coughing → 5 back blows → 5 abdominal thrusts (Heimlich)
- **Severe Bleeding**: Apply pressure → Elevate limb → Use tourniquet if needed
- **Burns**: Cool with water → Cover with clean cloth → Monitor for shock
- **Fainting**: Lay flat → Elevate legs → Check pulse

### 3. Geofencing (500m Radius)

Uses **Haversine formula** to find contacts within 500 meters:

```python
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    φ1, φ2 = radians(lat1), radians(lat2)
    Δφ = radians(lat2 - lat1)
    Δλ = radians(lon2 - lon1)
    
    a = sin(Δφ/2)**2 + cos(φ1) * cos(φ2) * sin(Δλ/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c
```

### 4. CPR Metronome

Web Audio API generates 100-120 BPM tone (AHA-recommended compression rate):

```typescript
const audioContext = new AudioContext();
const oscillator = audioContext.createOscillator();
oscillator.frequency.value = 800; // Hz
oscillator.type = 'sine';
oscillator.start();

const interval = 60000 / bpm; // milliseconds per beat
setInterval(() => oscillator.connect(audioContext.destination), interval);
```

### 5. Incident Timeline

Every action is logged with timestamp:

```json
{
  "incident_id": "123",
  "events": [
    {"time": "00:00", "type": "start", "detail": "Emergency reported: cardiac arrest"},
    {"time": "00:30", "type": "alert_sent", "detail": "3 contacts notified within 500m"},
    {"time": "01:15", "type": "step_completed", "detail": "CPR initiated"},
    {"time": "08:45", "type": "resolved", "detail": "EMS arrived"}
  ]
}
```

---

## 🔑 API Endpoints

### Triage
```
POST /triage
{
  "text": "Person collapsed, not breathing",
  "locale": "en-US",
  "age_group": "adult"
}
→ { "type": "cardiac_arrest", "severity": "critical", "steps": [...] }
```

### Alerts
```
POST /alerts
{
  "user_id": 1,
  "incident_id": 123,
  "latitude": 42.9634,
  "longitude": -78.7384
}
→ { "sent": 3, "contacts": [...] }
```

### Hospital Routing
```
POST /route
{
  "latitude": 42.9634,
  "longitude": -78.7384
}
→ { "hospital": "Buffalo General", "distance": 2.3, "duration": "5 mins" }
```

### Incidents
```
POST /incidents
GET /incidents/{id}
POST /incidents/{id}/events
POST /incidents/{id}/resolve
GET /incidents/{id}/summary
```

### Contacts
```
GET /contacts?user_id=1
POST /contacts
DELETE /contacts/{id}
```

---

## 🎨 UI Components

### Home Screen (`routes/Home.tsx`)
- Large circular SOS button (emergency red, 256px)
- Permission status banners (geolocation, microphone)
- Quick access to contacts management

### Incident Screen (`routes/Incident.tsx`)
- Voice input with microphone button
- AI triage results (type, severity badge)
- Step cards with timers and completion tracking
- CPR metronome overlay (100-120 BPM)
- Alert status (contacts notified)
- Hospital card with distance/ETA

### StepCard Component
- Title, description, estimated time
- Start button → countdown timer
- Red pulsing animation when <10s remaining
- Shows CPR cadence (beats per minute)
- Completion checkmark

### Metronome Component
- Play/pause toggle
- Visual beat indicator (blue pulse)
- Adjustable BPM (100-120 for CPR)
- Web Audio API oscillator

---

## 🧪 Testing

### Backend Tests
```bash
cd api
pytest tests/ -v
```

### Frontend Tests
```bash
cd web
npm run test
```

### Demo Script (Judges)

1. **Show landing page** → Click SOS button
2. **Grant permissions** (geolocation, microphone)
3. **Voice input**: "Someone is choking on food"
4. **AI triage**: Shows "Choking - Serious" with 4 steps
5. **Start first step**: Timer begins, TTS narrates instructions
6. **Alert sent**: "2 contacts within 500m notified via SMS"
7. **Show hospital**: "Buffalo General - 2.3 km - 5 min ETA"
8. **End incident**: View summary timeline with timestamps

---

## 📦 Deployment

### DigitalOcean App Platform

1. **Create App** → Connect GitHub repo
2. **API Service**:
   - Source: `api/`
   - Build: `pip install -r requirements.txt`
   - Run: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - Environment variables (Gemini, Twilio, Maps, Auth0)
3. **Static Site** (web):
   - Source: `web/`
   - Build: `npm run build`
   - Output: `dist/`
4. **Add PostgreSQL Database** → Copy connection string to API env vars
5. **Optional**: Add Redis for caching

**Cost**: $5/mo for API + $0 for static site + $7/mo for database = **$12/mo**

### Vercel (Frontend Only)

```bash
cd web
npm install -g vercel
vercel --prod
```

Set environment variable: `VITE_API_BASE_URL=https://your-api.ondigitalocean.app`

### Custom Domain (GoDaddy)

1. Register: `mediassistai.xyz`
2. Add DNS records:
   - `A` → DigitalOcean IP
   - `CNAME api` → `your-app.ondigitalocean.app`
3. Update CORS in `api/app/main.py`:
```python
origins = [
    "https://mediassistai.xyz",
    "https://api.mediassistai.xyz"
]
```

---

## 🤝 Contributing

This is a hackathon project! Contributions welcome:

1. Fork the repo
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- **UB Hacking Fall 2025** organizers
- **American Heart Association** for first-aid protocols
- **PMC Emergency Medicine** for evidence-based guidelines
- **Sponsors**: Auth0, Google, ElevenLabs, DigitalOcean, Vultr, Cloudflare, GoDaddy

---

## 📧 Contact

**Team**: [Your Name]  
**Email**: your.email@example.com  
**Devpost**: [Project Link](#)  
**Demo**: [Video Link](#)

---

## 🏥 Disclaimer

**MediAssist AI is a hackathon prototype for educational purposes only.**

This app provides general first-aid guidance based on public health resources. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always call 911 or your local emergency number immediately in a medical emergency. The creators are not liable for any outcomes resulting from use of this application.

---

**Built with ❤️ in 36 hours for UB Hacking Fall 2025**
