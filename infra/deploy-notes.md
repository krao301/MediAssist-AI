# Deployment Notes

## Quick Start (Local Development)

### Backend (API)
```bash
cd api
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn app.main:app --reload --port 8000
```

### Frontend (Web)
```bash
cd web
npm install
cp .env.example .env
# Edit .env with API base URL
npm run dev
```

### Docker (All Services)
```bash
cd infra
docker-compose up -d
```

## Production Deployment

### DigitalOcean App Platform
1. Create new App
2. Connect GitHub repo
3. Add API service (Python):
   - Source: `api/`
   - Run Command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - Environment variables from `.env.example`
4. Add Static Site (web):
   - Source: `web/`
   - Build: `npm run build`
   - Output: `dist/`
5. Add PostgreSQL Database
6. Add Redis

### Vercel (Frontend Only)
```bash
cd web
npm install -g vercel
vercel --prod
```

### Render (Backend)
1. New Web Service
2. Connect repo
3. Build: `pip install -r requirements.txt`
4. Start: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. Add env vars

## Environment Variables

### Required
- `GEMINI_API_KEY` or `OPENAI_API_KEY`
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER`
- `MAPS_API_KEY` (Google Maps)
- `DB_URL` (PostgreSQL connection string)

### Optional (Auth0)
- `AUTH0_DOMAIN`
- `AUTH0_AUDIENCE`
- `AUTH0_CLIENT_ID` (frontend)

### Optional (Advanced)
- `ELEVENLABS_API_KEY` (TTS)
- `REDIS_URL` (caching)
- `BASE_URL` (for SMS links)

## Custom Domain (GoDaddy)
1. Register domain: `mediassistai.xyz`
2. Point A record to deployment IP
3. Add CNAME for `api.mediassistai.xyz`
4. Update CORS in `api/app/main.py`

## Cloudflare Workers (Optional)
Deploy alert webhook handler for edge processing:
```bash
cd infra
npx wrangler deploy worker.js
```
