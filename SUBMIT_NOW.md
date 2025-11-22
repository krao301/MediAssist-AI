# 🚀 DEVPOST SUBMISSION - 10 MINUTE CHECKLIST

## ✅ STEP 1: Deploy Backend (3 min)
1. Go to: https://render.com
2. Click "New +" → "Web Service"
3. Select "Deploy an existing image from a registry"
4. Image URL: `docker.io/hrithikesh11/mediassist-api:latest`
5. Name: `mediassist-api`
6. **PASTE THESE ENVIRONMENT VARIABLES** (they override .env in Docker):

```
DATABASE_URL=postgresql://neondb_owner:npg_zO4Pk9Ah1Mdo@ep-orange-truth-a5ktx0u4.us-east-2.aws.neon.tech/neondb?sslmode=require
JWT_SECRET=your-secret-key-change-in-production
AUTH0_DOMAIN=dev-bv4rdiy74pj3ybge.us.auth0.com
AUTH0_API_AUDIENCE=https://api.mediassistai
TWILIO_ACCOUNT_SID=ACea04dbf8586de660a5585e20d85c6668
TWILIO_AUTH_TOKEN=e5f2cd583b70a6e02ee36d84d30e7e50
TWILIO_PHONE_NUMBER=+18559395733
GMAIL_ADDRESS=mediassistai.hacks@gmail.com
GMAIL_APP_PASSWORD=yksk zpwp fqva abap
GOOGLE_MAPS_API_KEY=AIzaSyDSYNQz5tkIRJPTiSbly-ng8Odgcqevqp4
GEMINI_API_KEY=AIzaSyCEPUDlgsYj1i6MffQp_dxRGd4ztGCTtSE
ELEVENLABS_API_KEY=sk_70d4491d69eab0f41e5d1574263aa4b6b26510576835daab
```

7. Click "Create Web Service"
8. **COPY THE RENDER URL** (like https://mediassist-api-xxxx.onrender.com)

---

## ✅ STEP 2: Deploy Frontend (2 min)
1. Go to: https://dash.cloudflare.com
2. Click "Workers & Pages" → "Create application" → "Pages"
3. Click "Upload assets"
4. Name: `mediassist`
5. **DRAG AND DROP** the folder: `/Users/hrithikeshsankineni/Documents/MediAssist-AI/web/dist`
6. Click "Deploy site"
7. **COPY THE CLOUDFLARE URL** (like https://mediassist.pages.dev)

---

## ✅ STEP 3: Update Frontend Config (1 min)
1. Open: `/Users/hrithikeshsankineni/Documents/MediAssist-AI/web/.env.production`
2. Replace line 1 with YOUR RENDER URL:
   ```
   VITE_API_BASE=https://mediassist-api-xxxx.onrender.com
   ```
3. Run:
   ```bash
   cd /Users/hrithikeshsankineni/Documents/MediAssist-AI/web
   npm run build
   cd ..
   ```
4. **RE-UPLOAD** the `web/dist` folder to Cloudflare Pages (same project, new deployment)

---

## ✅ STEP 4: Configure Auth0 (1 min)
1. Go to: https://manage.auth0.com/dashboard/us/dev-bv4rdiy74pj3ybge/applications
2. Click your application
3. Add to **Allowed Callback URLs**:
   ```
   https://mediassist.pages.dev/callback,http://localhost:5173/callback
   ```
4. Add to **Allowed Logout URLs**:
   ```
   https://mediassist.pages.dev,http://localhost:5173
   ```
5. Add to **Allowed Web Origins**:
   ```
   https://mediassist.pages.dev,http://localhost:5173
   ```
6. Click "Save Changes"

---

## ✅ STEP 5: Submit to DevPost (3 min)
1. Go to: https://devpost.com/software/mediassist-ai?ref_content=user-portfolio&ref_feature=in_progress
2. Click "Edit Project"
3. Fill in:
   - **Try it out**: [YOUR CLOUDFLARE URL]
   - **Video Demo**: (upload if you have one, or skip)
   - **Links**: 
     - Website: https://mediassist.pages.dev
     - GitHub: https://github.com/krao301/MediAssist-AI
4. Click "Publish" or "Submit"

---

## 🎯 YOUR URLS (fill these in as you go):
- ✅ Backend: _______________________________________
- ✅ Frontend: _______________________________________
- ✅ DevPost: https://devpost.com/software/mediassist-ai

---

## ⚡ WHY YOUR SECRETS ARE SAFE:
- Environment variables in Render **OVERRIDE** the .env file in Docker
- Cloudflare Pages only has public frontend code (no secrets)
- Docker image .env is ignored when Render env vars are set

**START WITH STEP 1 NOW! GO GO GO! 🚀**
