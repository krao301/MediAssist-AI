# Project Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MediAssist AI System                          │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                          Frontend (PWA)                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Home.tsx   │  │ Incident.tsx │  │ Contacts.tsx │             │
│  │              │  │              │  │              │             │
│  │ • SOS Button │  │ • Voice STT  │  │ • Add/Delete │             │
│  │ • Permissions│  │ • AI Triage  │  │ • Geofence   │             │
│  │              │  │ • Step Cards │  │ • 500m Radius│             │
│  └──────────────┘  │ • Metronome  │  └──────────────┘             │
│                     │ • Hospital   │                                 │
│                     └──────────────┘                                 │
│                                                                       │
│  Components:                                                          │
│  • StepCard.tsx (Timer, Completion)                                 │
│  • Metronome.tsx (CPR Audio, 100-120 BPM)                          │
│                                                                       │
│  Libraries:                                                           │
│  • React Router v6 (Navigation)                                      │
│  • Axios (API Client)                                                │
│  • Web Speech API (Browser TTS/STT)                                 │
│  • Vite PWA (Service Workers)                                        │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ HTTPS
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Backend API (FastAPI)                         │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                        Routes                                 │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ • /triage      → AI emergency classification                │   │
│  │ • /alerts      → Geofenced SMS/voice alerts                 │   │
│  │ • /route       → Nearest hospital routing                    │   │
│  │ • /incidents   → CRUD operations, timeline                   │   │
│  │ • /contacts    → Trusted contacts management                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                       Services                                │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ • llm.py       → Gemini API triage + knowledge base         │   │
│  │ • geo.py       → Haversine distance, Maps API               │   │
│  │ • notify.py    → Twilio SMS/voice alerts                    │   │
│  │ • summary.py   → Timeline generation, text export           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                        Models                                 │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ • User         → auth0_sub, consent, timezone               │   │
│  │ • Contact      → name, phone, lat/lng, radius               │   │
│  │ • Incident     → type, severity, status, timestamps         │   │
│  │ • IncidentEvent → timeline tracking                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
          ┌──────────────┐ ┌──────────┐ ┌──────────────┐
          │  PostgreSQL  │ │  Redis   │ │   Auth0      │
          │              │ │          │ │              │
          │ • Users      │ │ • Cache  │ │ • JWT Tokens │
          │ • Contacts   │ │ • Sessions│ │ • SSO/MFA   │
          │ • Incidents  │ └──────────┘ └──────────────┘
          │ • Events     │
          └──────────────┘

External APIs:
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ Google Gemini    │ │ Twilio           │ │ Google Maps      │
│                  │ │                  │ │                  │
│ • Emergency      │ │ • SMS Alerts     │ │ • Hospital       │
│   Classification │ │ • Voice Calls    │ │   Search         │
│ • Step Plans     │ │ • E.164 Format   │ │ • Geocoding      │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

## Data Flow: Emergency Scenario

```
1. User Action
   ├─ Click SOS Button → getCurrentLocation()
   └─ Grant Permissions → Geolocation + Microphone

2. Voice Input
   ├─ startListening() → Web Speech API
   ├─ Transcription: "Person collapsed, not breathing"
   └─ POST /triage { text, locale, age_group }

3. AI Triage (Backend)
   ├─ llm.classify_and_plan() → Gemini API
   ├─ Fallback → Keyword matching (FIRST_AID_KB)
   └─ Return: { type: "cardiac_arrest", severity: "critical", steps: [...] }

4. Create Incident
   ├─ POST /incidents { user_id, lat, lng, type, severity }
   ├─ Database INSERT into incidents table
   └─ Return: { id: 123, status: "active" }

5. Display Steps
   ├─ Render StepCard for each step
   ├─ User clicks "Start" on Step 1
   └─ Timer countdown begins (useEffect)

6. Send Alerts
   ├─ POST /alerts { user_id, incident_id, lat, lng }
   ├─ geo.contacts_within_radius() → Haversine calc
   ├─ Filter contacts <500m
   ├─ notify.send_sms() → Twilio API
   └─ Return: { sent: 2, contacts: [...] }

7. Hospital Routing
   ├─ POST /route { lat, lng }
   ├─ geo.find_nearest_hospital() → Maps API
   └─ Return: { hospital: "...", distance: 2.3, duration: 5 }

8. CPR Metronome (Cardiac Arrest only)
   ├─ User clicks "Start Metronome"
   ├─ Web Audio API → Oscillator at 800Hz
   ├─ Interval = 60000 / 120 BPM = 500ms
   └─ Beep every 500ms with visual indicator

9. Timeline Logging
   ├─ POST /incidents/{id}/events { type: "step_completed", detail: "..." }
   ├─ Database INSERT into incident_events
   └─ Timestamp recorded (UTC)

10. Resolve Incident
    ├─ User clicks "End Incident"
    ├─ POST /incidents/{id}/resolve
    ├─ Database UPDATE incidents SET status='resolved', resolved_at=NOW()
    └─ Navigate to /summary/{id}

11. Summary Report
    ├─ GET /incidents/{id}/summary
    ├─ Calculate duration, format timeline (+MM:SS)
    ├─ Display: Type, Severity, Duration, Steps Completed
    └─ Download JSON for EMS handoff
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Security Layers                              │
└─────────────────────────────────────────────────────────────────┘

Frontend (web/)
├─ HTTPS Only (production)
├─ Content Security Policy
├─ JWT Storage (localStorage or cookies)
└─ Permission Requests (Geolocation, Microphone)

Backend (api/)
├─ Auth0 JWT Verification
│  ├─ Signature validation (RS256)
│  ├─ Expiration check
│  └─ Audience/Issuer validation
│
├─ Demo Mode Fallback (development)
│  └─ Bypasses auth for rapid testing
│
├─ CORS Configuration
│  └─ Allowed origins: [localhost:5173, mediassistai.xyz]
│
├─ Rate Limiting
│  ├─ 60 req/min for /triage
│  └─ 100 req/min for other endpoints
│
├─ Input Validation
│  ├─ Pydantic schemas
│  ├─ Phone number validation (E.164)
│  └─ Coordinate bounds checking
│
└─ API Key Security
   ├─ Environment variables only
   ├─ Never committed to git
   └─ Rotate keys regularly

Database
├─ PostgreSQL with SSL (production)
├─ Prepared statements (SQLAlchemy ORM)
├─ Foreign key constraints
└─ Encrypted backups

External APIs
├─ HTTPS for all requests
├─ API key rotation
└─ Error handling (no key leakage)
```

## Deployment Topology

```
┌────────────────────────────────────────────────────────────────┐
│                      Production Stack                           │
└────────────────────────────────────────────────────────────────┘

DNS (GoDaddy)
├─ mediassistai.xyz           → Vercel (Frontend)
└─ api.mediassistai.xyz       → DigitalOcean (Backend)

Frontend (Vercel)
├─ CDN Edge Nodes (Global)
├─ Automatic HTTPS (Let's Encrypt)
├─ Service Worker Caching
└─ Gzip Compression

Backend (DigitalOcean App Platform)
├─ Container: Python 3.12 + FastAPI
├─ Auto-scaling: 1-3 instances
├─ Health checks: /health endpoint
└─ Zero-downtime deployments

Database (DigitalOcean Managed PostgreSQL)
├─ Version: PostgreSQL 15
├─ Backups: Daily automated
├─ Connection pooling
└─ Read replicas (optional)

Cache (DigitalOcean Managed Redis)
├─ Version: Redis 7
├─ Used for: Session storage, rate limiting
└─ Eviction: LRU

Monitoring
├─ DigitalOcean Insights (metrics, logs)
├─ Sentry (error tracking)
└─ Uptime checks (PagerDuty)

CDN (Cloudflare - Optional)
├─ Edge workers for alert webhooks
├─ DDoS protection
└─ Web Application Firewall
```

## File Structure

```
mediassist-ai/
│
├── api/                        # Backend FastAPI application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app, CORS, routes
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── database.py        # Database session management
│   │   │
│   │   ├── deps/
│   │   │   └── auth.py        # Auth0 JWT verification
│   │   │
│   │   ├── routes/
│   │   │   ├── triage.py      # POST /triage
│   │   │   ├── alerts.py      # POST /alerts
│   │   │   ├── route.py       # POST /route
│   │   │   ├── incidents.py   # Incident CRUD
│   │   │   └── contacts.py    # Contact management
│   │   │
│   │   └── services/
│   │       ├── llm.py         # Gemini API integration
│   │       ├── geo.py         # Haversine, Maps API
│   │       ├── notify.py      # Twilio SMS/voice
│   │       └── summary.py     # Report generation
│   │
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Container definition
│   └── .env.example          # Environment template
│
├── web/                       # Frontend React PWA
│   ├── src/
│   │   ├── main.tsx          # Entry point
│   │   ├── App.tsx           # Router setup
│   │   │
│   │   ├── routes/
│   │   │   ├── Home.tsx      # Landing + SOS button
│   │   │   ├── Incident.tsx  # Active emergency
│   │   │   ├── Contacts.tsx  # Contact management
│   │   │   └── Summary.tsx   # Post-incident report
│   │   │
│   │   ├── components/
│   │   │   ├── StepCard.tsx  # Step display + timer
│   │   │   └── Metronome.tsx # CPR audio metronome
│   │   │
│   │   ├── lib/
│   │   │   ├── api.ts        # Axios API client
│   │   │   ├── tts.ts        # Web Speech API
│   │   │   └── permissions.ts# Geolocation/mic perms
│   │   │
│   │   └── styles/
│   │       └── index.css     # Tailwind + animations
│   │
│   ├── public/
│   │   ├── manifest.json     # PWA manifest
│   │   └── icon-*.png        # PWA icons
│   │
│   ├── package.json          # Node dependencies
│   ├── vite.config.ts        # Vite + PWA plugin
│   ├── tailwind.config.js    # Tailwind config
│   ├── index.html            # HTML entry
│   └── .env.example          # Frontend env template
│
├── infra/                     # Infrastructure
│   ├── docker-compose.yml    # Local dev stack
│   └── deploy-notes.md       # Deployment guide
│
├── README.md                  # Main documentation
├── TESTING.md                 # Testing guide
├── API.md                     # API reference
├── LICENSE                    # MIT license
├── .gitignore                # Git ignore rules
├── start.sh                  # Unix startup script
└── start.ps1                 # Windows startup script
```

## Technology Decisions

### Why FastAPI?
- Fast (async/await support)
- Automatic API docs (Swagger UI)
- Type hints with Pydantic
- Easy testing with pytest

### Why React + Vite?
- Fast development with HMR
- Modern build tool (faster than CRA)
- PWA plugin for service workers
- TypeScript support

### Why PostgreSQL?
- Relational data (users, contacts, incidents)
- JSONB for flexible incident data
- PostGIS for geospatial queries (future)
- Managed hosting available

### Why Gemini API?
- Free tier (15 req/min)
- Good at medical reasoning
- Handles context well
- Multimodal (text + future image input)

### Why Twilio?
- Reliable SMS/voice delivery
- E.164 phone number support
- Programmable Voice API
- Global coverage

### Why Auth0?
- Free tier (7000 users)
- SSO/MFA built-in
- JWT standard
- Easy frontend SDKs

## Performance Characteristics

### Response Times (p95)
- `/triage`: 1.5s (Gemini API latency)
- `/alerts`: 800ms (Twilio API latency)
- `/route`: 600ms (Maps API latency)
- `/incidents`: 50ms (database query)

### Scaling Limits
- Database: 10,000 concurrent users
- API: 100 req/sec per instance
- Frontend: CDN-backed (unlimited)

### Bottlenecks
1. Gemini API rate limit (15 req/min free tier)
   - Solution: Upgrade to paid tier or cache common queries
2. Twilio SMS cost ($0.0075 per message)
   - Solution: Rate limit alerts to prevent abuse
3. Maps API quota (free tier: 28,000 req/month)
   - Solution: Cache hospital locations

## Future Enhancements

### Phase 2 (Post-Hackathon)
- [ ] ElevenLabs TTS integration (multilingual)
- [ ] Whisper STT for better voice recognition
- [ ] Image upload (Gemini Vision API for injury assessment)
- [ ] Video call support (WebRTC)
- [ ] Offline mode with IndexedDB
- [ ] Push notifications (Firebase Cloud Messaging)

### Phase 3 (Production-Ready)
- [ ] HIPAA compliance (encrypted storage)
- [ ] EMS dispatch integration
- [ ] Insurance verification
- [ ] Medical history integration
- [ ] Telemedicine consult
- [ ] Wearable device support (Apple Watch, Fitbit)

---

**Last Updated**: January 2025  
**Version**: 1.0.0 (Hackathon Submission)
