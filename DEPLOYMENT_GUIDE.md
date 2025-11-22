# 🚀 MediAssist-AI Deployment Guide
## Domain: https://medi-assist.health

This guide will deploy your complete application to production for your hackathon.

---

## 📋 Architecture Overview

```
User → medi-assist.health (Cloudflare Pages)
              ↓
        Frontend (React)
              ↓
     api.medi-assist.health (Render.com)
              ↓
        Backend API (Docker Container)
              ↓
     Database (Neon PostgreSQL - Already Setup ✅)
```

---

## 🎯 Step 1: Push Docker Images to Docker Hub

**Status:** ✅ Already built! Now pushing...

```bash
docker push hrithikesh11/mediassist-api:latest
docker push hrithikesh11/mediassist-web:latest
```

Your images will be available at:
- https://hub.docker.com/r/hrithikesh11/mediassist-api
- https://hub.docker.com/r/hrithikesh11/mediassist-web

---

## 🎯 Step 2: Deploy Backend to Render.com

### A. Create Render Account
1. Go to: https://render.com
2. Sign up with GitHub (free account)

### B. Deploy Backend API

1. **Click "New +" → "Web Service"**

2. **Choose "Deploy an existing image from a registry"**

3. **Image URL:**
   ```
   docker.io/hrithikesh11/mediassist-api:latest
   ```

4. **Service Name:** `mediassist-api`

5. **Environment Variables** (Click "Add Environment Variable"):
   ```
   AUTH0_DOMAIN=dev-bv4rdiy74pj3ybge.us.auth0.com
   AUTH0_AUDIENCE=https://api.mediassistai
   AUTH0_JWKS=https://dev-bv4rdiy74pj3ybge.us.auth0.com/.well-known/jwks.json
   
   DB_URL=postgresql://neondb_owner:YOUR_NEON_PASSWORD_HERE@ep-withered-unit-ad1fm90p-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
   
   REDIS_URL=redis://red-ctc7c8dumphs73e6hfsg:6379
   
   TWILIO_ACCOUNT_SID=YOUR_TWILIO_SID_HERE
   TWILIO_AUTH_TOKEN=YOUR_TWILIO_TOKEN_HERE
   TWILIO_FROM_NUMBER=+16363317602
   
   GMAIL_ADDRESS=YOUR_GMAIL_ADDRESS
   GMAIL_APP_PASSWORD=YOUR_GMAIL_APP_PASSWORD_HERE
   
   MAPS_API_KEY=YOUR_MAPS_API_KEY_HERE
   GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
   ELEVENLABS_API_KEY=YOUR_ELEVENLABS_API_KEY_HERE
   
   BASE_URL=https://api.medi-assist.health
   ```

6. **Instance Type:** Free (for hackathon)

7. **Click "Deploy Web Service"**

8. **Wait 5-10 minutes** for deployment

9. **Copy your API URL** (will be something like: `https://mediassist-api.onrender.com`)

---

## 🎯 Step 3: Deploy Frontend to Cloudflare Pages

### A. Build Frontend for Production

1. **Update API URL in frontend:**
   ```bash
   cd /Users/hrithikeshsankineni/Documents/MediAssist-AI/web
   ```

2. **Create production environment file:**
   Create `web/.env.production`:
   ```env
   VITE_API_BASE=https://mediassist-api.onrender.com
   VITE_AUTH0_DOMAIN=dev-bv4rdiy74pj3ybge.us.auth0.com
   VITE_AUTH0_CLIENT_ID=k279MsPj5GZNhqEyNu5EhYpdPZu82krn
   VITE_AUTH0_AUDIENCE=https://api.mediassistai
   VITE_MAPS_API_KEY=YOUR_MAPS_API_KEY_HERE
   ```

3. **Build the frontend:**
   ```bash
   npm run build
   ```

### B. Deploy to Cloudflare Pages

**Option A: Direct Upload (Easiest)**

1. Go to: https://dash.cloudflare.com
2. Select your account → **Workers & Pages**
3. Click **"Create application"** → **"Pages"** → **"Upload assets"**
4. **Project name:** `mediassist`
5. **Drag and drop** the `web/dist` folder
6. Click **"Deploy site"**
7. **Wait 2-3 minutes**

**Option B: Using Wrangler CLI**

```bash
# Install Wrangler
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Deploy
cd web
npx wrangler pages deploy dist --project-name=mediassist
```

After deployment, you'll get a URL like: `https://mediassist.pages.dev`

---

## 🎯 Step 4: Configure Custom Domain

### A. Update Auth0 URLs

1. Go to: https://manage.auth0.com
2. Navigate to **Applications** → Your App
3. **Update these fields:**
   - **Allowed Callback URLs:**
     ```
     https://medi-assist.health, https://mediassist.pages.dev
     ```
   - **Allowed Logout URLs:**
     ```
     https://medi-assist.health, https://mediassist.pages.dev
     ```
   - **Allowed Web Origins:**
     ```
     https://medi-assist.health, https://mediassist.pages.dev
     ```
4. **Save Changes**

### B. Configure Cloudflare DNS

1. Go to **Cloudflare Dashboard** → **DNS** → **Records**

2. **Add these DNS records:**

   **For Frontend:**
   ```
   Type: CNAME
   Name: @
   Target: mediassist.pages.dev
   Proxy: ✅ Proxied (Orange cloud)
   ```

   ```
   Type: CNAME
   Name: www
   Target: mediassist.pages.dev
   Proxy: ✅ Proxied (Orange cloud)
   ```

   **For Backend API:**
   ```
   Type: CNAME
   Name: api
   Target: mediassist-api.onrender.com
   Proxy: ✅ Proxied (Orange cloud)
   ```

3. **Wait 5-10 minutes** for DNS propagation

### C. Configure Custom Domain in Cloudflare Pages

1. Go to **Cloudflare Pages** → Your Project → **Custom domains**
2. Click **"Set up a custom domain"**
3. Enter: `medi-assist.health`
4. Click **"Continue"** → **"Activate domain"**
5. Repeat for `www.medi-assist.health`

### D. Configure Custom Domain in Render

1. Go to **Render Dashboard** → Your Service → **Settings**
2. Scroll to **"Custom Domain"**
3. Click **"Add Custom Domain"**
4. Enter: `api.medi-assist.health`
5. Follow the verification steps

---

## 🎯 Step 5: Update Frontend to Use Custom Domain

After API is deployed to `api.medi-assist.health`:

1. **Update `web/.env.production`:**
   ```env
   VITE_API_BASE=https://api.medi-assist.health
   ```

2. **Rebuild and redeploy:**
   ```bash
   cd web
   npm run build
   npx wrangler pages deploy dist --project-name=mediassist
   ```

---

## 🎯 Step 6: Update Backend CORS

1. **Edit `api/app/main.py`:**
   Add your production domains to CORS:
   ```python
   origins = [
       "http://localhost:5173",
       "http://localhost:3000",
       "https://medi-assist.health",
       "https://www.medi-assist.health",
       "https://mediassist.pages.dev",
   ]
   ```

2. **Rebuild and push Docker image:**
   ```bash
   cd /Users/hrithikeshsankineni/Documents/MediAssist-AI
   docker build -f Dockerfile.api -t hrithikesh11/mediassist-api:latest .
   docker push hrithikesh11/mediassist-api:latest
   ```

3. **Trigger redeployment in Render:**
   - Go to Render Dashboard → Your Service
   - Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## ✅ Verification Checklist

After deployment, verify everything works:

### Frontend Checks:
- [ ] Visit: https://medi-assist.health
- [ ] Click "Sign In" → Auth0 login works
- [ ] After login, you see the home page
- [ ] User profile shows in top-right

### Backend Checks:
- [ ] Visit: https://api.medi-assist.health/docs
- [ ] API documentation loads
- [ ] Test endpoint: https://api.medi-assist.health/health

### Emergency Flow Checks:
- [ ] Click SOS button
- [ ] Grant microphone permission
- [ ] Speak or type emergency description
- [ ] Verify triage response appears
- [ ] Check phone for SMS/calls (if critical emergency)

---

## 🐛 Troubleshooting

### Frontend not loading?
- Check Cloudflare Pages build logs
- Verify DNS records are correct
- Clear browser cache (Cmd+Shift+R)

### Backend API errors?
- Check Render logs: Dashboard → Service → Logs
- Verify all environment variables are set
- Check database connection

### Auth0 errors?
- Verify callback URLs include your domain
- Check that client ID matches in frontend .env
- Clear localStorage and try again

### CORS errors?
- Update CORS origins in `api/app/main.py`
- Redeploy backend after changes

---

## 📊 Monitoring

### Render Dashboard:
- Monitor API health and logs
- View deployment history
- Check resource usage

### Cloudflare Analytics:
- View frontend traffic
- Monitor CDN performance
- Check security events

---

## 🎉 Post-Deployment

After successful deployment:

1. **Test all features:**
   - Emergency reporting
   - Voice input
   - SMS/Email notifications
   - Hospital routing

2. **Share your live demo:**
   ```
   🚀 MediAssist-AI Live Demo
   Frontend: https://medi-assist.health
   API Docs: https://api.medi-assist.health/docs
   ```

3. **Prepare for hackathon:**
   - Take screenshots
   - Record demo video
   - Test on mobile devices
   - Have backup (local) ready

---

## 💰 Cost Breakdown

**For Hackathon (Free Tier):**
- ✅ Cloudflare Pages: **FREE**
- ✅ Render.com: **FREE** (750 hours/month)
- ✅ Neon PostgreSQL: **FREE** (Already using)
- ✅ Domain: **Already purchased** ✅

**Total Monthly Cost: $0** 🎉

**To upgrade after hackathon:**
- Render Starter: $7/month (better performance)
- Cloudflare Pro: $20/month (advanced features)

---

## 🚀 Quick Commands Reference

```bash
# Build and push backend
docker build -f Dockerfile.api -t hrithikesh11/mediassist-api:latest .
docker push hrithikesh11/mediassist-api:latest

# Build and deploy frontend
cd web
npm run build
npx wrangler pages deploy dist --project-name=mediassist

# View logs
# Render: Dashboard → Logs
# Cloudflare: Dashboard → Analytics
```

---

## 🆘 Emergency Rollback

If something breaks during hackathon:

1. **Quick fix:** Run locally with `./local-start.sh`
2. **Show local version** while fixing production
3. **Redeploy:** Follow steps above

---

**Good luck with your hackathon! 🎉**

Questions? Check Render logs and Cloudflare dashboard for errors.
