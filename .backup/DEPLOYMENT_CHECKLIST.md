# 🚀 Quick Deployment Checklist for Hackathon

## ✅ Pre-Deployment (Complete!)
- [x] Docker images built
- [x] Frontend configured for production
- [x] Backend CORS updated for production domain
- [x] Deployment scripts created

---

## 🎯 Deployment Steps (30-45 minutes)

### Step 1: Deploy Backend API (15 min)

1. Go to **Render.com**: https://render.com
2. Sign up/Login (use GitHub)
3. Click **"New +" → "Web Service"**
4. Select **"Deploy an existing image from a registry"**
5. **Image URL:** `docker.io/hrithikesh11/mediassist-api:latest`
6. **Service Name:** `mediassist-api`
7. **Region:** Oregon (US West)
8. **Instance Type:** Free
9. **Add Environment Variables** (copy from below):

```
AUTH0_DOMAIN=dev-bv4rdiy74pj3ybge.us.auth0.com
AUTH0_AUDIENCE=https://api.mediassistai
AUTH0_JWKS=https://dev-bv4rdiy74pj3ybge.us.auth0.com/.well-known/jwks.json
DB_URL=postgresql://neondb_owner:npg_TJOy0MUH8YiA@ep-withered-unit-ad1fm90p-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
REDIS_URL=redis://red-ctc7c8dumphs73e6hfsg:6379
TWILIO_ACCOUNT_SID=ACea04dbf8586de660a5585e20d85c6668
TWILIO_AUTH_TOKEN=600665820ff037b203b653bfa9832550
TWILIO_FROM_NUMBER=+16363317602
GMAIL_ADDRESS=shritikesh8999@gmail.com
GMAIL_APP_PASSWORD=kxzfnaeizmkqibhb
MAPS_API_KEY=AIzaSyDSYNQz5tkIRJPTiSbly-ng8Odgcqevqp4
GEMINI_API_KEY=AIzaSyCEPUDlgsYj1i6MffQp_dxRGd4ztGCTtSE
ELEVENLABS_API_KEY=sk_70d4491d69eab0f41e5d1574263aa4b6b26510576835daab
BASE_URL=https://api.medi-assist.health
```

10. Click **"Create Web Service"**
11. **Wait 5-10 minutes** for deployment
12. **Copy your API URL** (example: `https://mediassist-api.onrender.com`)

---

### Step 2: Build and Deploy Frontend (10 min)

**Run this command:**
```bash
cd /Users/hrithikeshsankineni/Documents/MediAssist-AI
./deploy-frontend.sh
```

**Then deploy to Cloudflare:**

1. Go to: https://dash.cloudflare.com
2. Click **"Workers & Pages"**
3. Click **"Create application"** → **"Pages"** → **"Upload assets"**
4. **Project name:** `mediassist`
5. **Drag and drop** the `web/dist` folder
6. Click **"Deploy site"**
7. Wait 2-3 minutes
8. **Copy your Pages URL** (example: `https://mediassist.pages.dev`)

---

### Step 3: Configure Custom Domain (10 min)

#### A. Cloudflare DNS

1. Go to **Cloudflare** → **DNS** → **Records**
2. **Add these records:**

   **Frontend:**
   ```
   Type: CNAME
   Name: @
   Target: mediassist.pages.dev
   Proxy: ✅ ON (orange cloud)
   TTL: Auto
   ```

   **Backend API:**
   ```
   Type: CNAME
   Name: api
   Target: mediassist-api.onrender.com
   Proxy: ✅ ON (orange cloud)
   TTL: Auto
   ```

3. **Save** and wait 5 minutes

#### B. Connect Custom Domain in Cloudflare Pages

1. Go to **Workers & Pages** → **mediassist project**
2. Click **"Custom domains"**
3. Click **"Set up a custom domain"**
4. Enter: `medi-assist.health`
5. Click **"Continue"** → **"Activate domain"**

#### C. Connect Custom Domain in Render

1. Go to **Render Dashboard** → **mediassist-api service**
2. Click **"Settings"** tab
3. Scroll to **"Custom Domain"**
4. Click **"Add Custom Domain"**
5. Enter: `api.medi-assist.health`
6. Follow verification (may take 10-15 min)

---

### Step 4: Update Auth0 (5 min)

1. Go to: https://manage.auth0.com
2. **Applications** → Your App
3. **Add these URLs:**

   **Allowed Callback URLs:**
   ```
   https://medi-assist.health,https://mediassist.pages.dev
   ```

   **Allowed Logout URLs:**
   ```
   https://medi-assist.health,https://mediassist.pages.dev
   ```

   **Allowed Web Origins:**
   ```
   https://medi-assist.health,https://mediassist.pages.dev
   ```

4. **Save Changes**

---

## ✅ Testing Your Deployment

### 1. Test Frontend
- Visit: https://medi-assist.health
- Should see login page
- Click "Sign In" → Auth0 should work

### 2. Test Backend
- Visit: https://api.medi-assist.health/docs
- Should see API documentation (Swagger UI)
- Try: https://api.medi-assist.health/health
- Should return: `{"status":"healthy"}`

### 3. Test Emergency Flow
- Login to: https://medi-assist.health
- Click SOS button
- Grant permissions
- Speak or type emergency
- Verify response appears

---

## 🐛 Troubleshooting

### Backend not deploying?
- Check Render logs for errors
- Verify all environment variables are set
- Make sure Docker image is public

### Frontend not loading?
- Check Cloudflare Pages build
- Clear browser cache (Cmd+Shift+R)
- Check browser console for errors

### Auth0 errors?
- Verify callback URLs include your domain
- Check client ID in .env.production
- Try logout and login again

### API CORS errors?
- Verify main.py has your domain in origins
- Rebuild and redeploy Docker image
- Check Render logs

---

## 📊 Monitor Your Deployment

### Render Dashboard
- View API logs in real-time
- Monitor CPU/Memory usage
- Check deployment status

### Cloudflare Analytics
- View frontend traffic
- Check global CDN performance
- Monitor security events

---

## 🎉 Success Criteria

Your app is live when:
- ✅ https://medi-assist.health loads
- ✅ Auth0 login works
- ✅ SOS button creates emergency session
- ✅ Voice/text input works
- ✅ API returns triage responses
- ✅ SMS/Calls sent for critical emergencies

---

## 💾 Backup Plan

If deployment fails during hackathon:

1. **Run locally:**
   ```bash
   ./local-start.sh
   ```

2. **Show local version** to judges/attendees

3. **Fix production issues** after demo

4. **Use ngrok** for temporary public URL:
   ```bash
   ngrok http 5173
   ```

---

## 📞 Resources

- **Deployment Guide:** DEPLOYMENT_GUIDE.md
- **Render Docs:** https://render.com/docs
- **Cloudflare Docs:** https://developers.cloudflare.com/pages
- **Auth0 Docs:** https://auth0.com/docs

---

**Estimated Total Time: 30-45 minutes**

Good luck with your hackathon! 🚀
