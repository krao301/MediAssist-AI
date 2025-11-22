# ⚡ ULTRA-FAST DEPLOYMENT FOR DEVPOST SUBMISSION
## Time: 15-20 minutes | For: UB Hacking Fall 2025

---

## 🎯 STEP 1: Deploy Backend (5 minutes)

### A. Go to Render.com
1. Open: **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (fastest)

### B. Deploy API
1. Click **"New +"** → **"Web Service"**
2. Select **"Deploy an existing image from a registry"**
3. **Image URL:** 
   ```
   docker.io/hrithikesh11/mediassist-api:latest
   ```
4. **Name:** `mediassist-api`
5. **Region:** Oregon (US West)
6. **Instance Type:** Free
7. **Click "Add Environment Variable"** and paste this (as individual variables):
   ```
   AUTH0_DOMAIN=dev-bv4rdiy74pj3ybge.us.auth0.com
   AUTH0_AUDIENCE=https://api.mediassistai
   AUTH0_JWKS=https://dev-bv4rdiy74pj3ybge.us.auth0.com/.well-known/jwks.json
   DB_URL=postgresql://neondb_owner:YOUR_NEON_PASSWORD_HERE@ep-withered-unit-ad1fm90p-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
   TWILIO_ACCOUNT_SID=YOUR_TWILIO_SID_HERE
   TWILIO_AUTH_TOKEN=YOUR_TWILIO_TOKEN_HERE
   TWILIO_FROM_NUMBER=+16363317602
   GMAIL_ADDRESS=YOUR_GMAIL_ADDRESS
   GMAIL_APP_PASSWORD=YOUR_GMAIL_APP_PASSWORD_HERE
   MAPS_API_KEY=YOUR_MAPS_API_KEY_HERE
   GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
   ELEVENLABS_API_KEY=YOUR_ELEVENLABS_API_KEY_HERE
   ```
8. Click **"Create Web Service"**
9. **WAIT 5 minutes** for deployment
10. **COPY YOUR URL** (example: `https://mediassist-api.onrender.com`)

---

## 🎯 STEP 2: Deploy Frontend (5 minutes)

### Option A: Cloudflare Pages (Recommended - Fastest)

1. **Go to:** https://dash.cloudflare.com
2. Click **"Workers & Pages"**
3. Click **"Create application"** → **"Pages"** → **"Upload assets"**
4. **Project name:** `mediassist`
5. **Drag folder:** `/Users/hrithikeshsankineni/Documents/MediAssist-AI/web/dist`
6. **Deploy!** (takes 2 minutes)
7. **COPY YOUR URL** (example: `https://mediassist.pages.dev`)

### Option B: Vercel (Alternative)

```bash
cd /Users/hrithikeshsankineni/Documents/MediAssist-AI/web
npm install -g vercel
vercel --prod
```

---

## 🎯 STEP 3: Update Frontend to Use Backend (3 minutes)

### Update Environment and Rebuild:

1. **Edit:** `web/.env.production`
   ```env
   VITE_API_BASE=https://mediassist-api.onrender.com
   ```
   (Replace with YOUR actual Render URL)

2. **Rebuild:**
   ```bash
   cd /Users/hrithikeshsankineni/Documents/MediAssist-AI/web
   npm run build
   ```

3. **Redeploy to Cloudflare:**
   - Go back to Cloudflare Pages
   - Upload the NEW `dist` folder again
   - Or use: `npx wrangler pages deploy dist --project-name=mediassist`

---

## 🎯 STEP 4: Update Auth0 (2 minutes)

1. **Go to:** https://manage.auth0.com
2. **Applications** → Your App
3. **Add your URLs:**
   
   **Allowed Callback URLs:**
   ```
   https://mediassist.pages.dev,https://mediassist-api.onrender.com
   ```
   
   **Allowed Logout URLs:**
   ```
   https://mediassist.pages.dev
   ```
   
   **Allowed Web Origins:**
   ```
   https://mediassist.pages.dev
   ```

4. **Save Changes**

---

## 🎯 STEP 5: Submit to DevPost (5 minutes)

### Go to: https://ub-hacking-fall-2025.devpost.com/

### Submission Info:

**Project Name:** MediAssist AI

**Tagline:** AI-Powered Emergency First-Aid Coach with Hyperlocal Alerts

**Live Demo URL:**
```
https://mediassist.pages.dev
```

**Demo Video:** (Optional - can skip for now)

**GitHub Repo:**
```
https://github.com/krao301/MediAssist-AI
```

**Built With (select these):**
- Python
- React
- FastAPI
- PostgreSQL
- Docker
- Cloudflare
- Google Cloud (Gemini AI)
- Twilio
- Auth0

**Description:**
```
MediAssist AI is an emergency first-aid coach that provides:

🚑 AI-Powered Triage
- Voice-guided emergency assessment using Google Gemini
- Severity classification (CRITICAL/MODERATE/MINOR)
- Real-time first-aid instructions

📍 Hyperlocal Emergency Response
- Automatic SOS calls to emergency contacts
- SMS/Email alerts to nearby trusted people
- Hospital routing with ETA calculation

🤖 Intelligent Features
- RAG (Retrieval-Augmented Generation) for medical knowledge
- Voice input/output for hands-free operation
- Progressive Web App (works offline)
- Real-time notifications via Twilio

💡 Technology Stack
- Backend: FastAPI + Python (Docker container)
- Frontend: React + TypeScript + Vite
- Database: PostgreSQL (Neon)
- AI: Google Gemini Pro
- Deployment: Render.com + Cloudflare Pages
- Auth: Auth0

✨ Key Innovation
Combines AI-powered medical triage with hyperlocal community response, enabling faster emergency assistance while waiting for professional help.

Try it: Click SOS → Describe emergency → Get instant guidance + automatic alerts
```

---

## ✅ TEST YOUR DEPLOYMENT

Before submitting:

1. **Visit:** Your Cloudflare Pages URL
2. **Login** with Auth0
3. **Click SOS button**
4. **Test emergency flow**

If it works → **SUBMIT TO DEVPOST!** ✅

---

## 🆘 BACKUP PLAN

If deployment fails:

### Deploy with Vercel (2 minutes):
```bash
cd web
npm install -g vercel
vercel --prod
```

### Or submit with local deployment + video:
1. Run `./local-start.sh`
2. Record quick demo video
3. Submit video instead of live URL

---

## 📋 QUICK REFERENCE

**Your URLs to submit:**
- Frontend: `https://mediassist.pages.dev` (or your Cloudflare URL)
- Backend: `https://mediassist-api.onrender.com` (or your Render URL)
- GitHub: `https://github.com/krao301/MediAssist-AI`
- DevPost: `https://ub-hacking-fall-2025.devpost.com/`

**Submission Deadline:** Check DevPost!

---

## 🎉 DONE!

Once deployed and tested:
1. ✅ Go to DevPost
2. ✅ Fill out submission form
3. ✅ Add your live URLs
4. ✅ Submit!

**Good luck! 🚀**
