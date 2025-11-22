# Auth0 Setup Guide for MediAssist AI

## Quick Setup Steps

### 1. Create Auth0 Account
1. Go to [Auth0](https://auth0.com) and sign up for a free account
2. Create a new tenant (e.g., `mediassist-dev`)

### 2. Create Application
1. In Auth0 Dashboard, go to **Applications** → **Applications**
2. Click **Create Application**
3. Choose **Single Page Web Applications**
4. Name it "MediAssist AI"
5. Click **Create**

### 3. Configure Application Settings

In your application settings:

**Allowed Callback URLs:**
```
http://localhost:5173, http://localhost:5173/callback
```

**Allowed Logout URLs:**
```
http://localhost:5173
```

**Allowed Web Origins:**
```
http://localhost:5173
```

**Allowed Origins (CORS):**
```
http://localhost:5173
```

Click **Save Changes**

### 4. Get Your Credentials

From the application settings page, copy:
- **Domain** (e.g., `mediassist-dev.us.auth0.com`)
- **Client ID** (e.g., `abc123xyz456...`)

### 5. Create API (Optional but Recommended)

1. Go to **Applications** → **APIs**
2. Click **Create API**
3. Name: `MediAssist API`
4. Identifier: `https://api.mediassistai`
5. Click **Create**

### 6. Configure Your .env File

```bash
cd web
copy .env.example .env
notepad .env
```

Update with your Auth0 credentials:
```bash
VITE_API_BASE=http://localhost:8000
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your-client-id-here
VITE_AUTH0_AUDIENCE=https://api.mediassistai
```

### 7. Test Authentication

```powershell
# Start the frontend
cd web
npm install
npm run dev
```

Visit http://localhost:5173 and you should see the sign-in page!

## Troubleshooting

### "Callback URL mismatch" error
- Make sure `http://localhost:5173` is in **Allowed Callback URLs**

### "Origin not allowed" error
- Make sure `http://localhost:5173` is in **Allowed Web Origins**

### Configuration missing error
- Check that your `.env` file has the correct Auth0 domain and client ID
- Restart the dev server after changing `.env`

## Features Implemented

✅ Sign in with Auth0  
✅ Protected routes (requires authentication)  
✅ User profile display with logout  
✅ Secure token storage in localStorage  
✅ Automatic token refresh  
✅ Beautiful sign-in page  

## Production Setup

For production, update the URLs to your production domain:
```
https://yourdomain.com
```

And update your `.env.production`:
```bash
VITE_API_BASE=https://api.yourdomain.com
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your-production-client-id
VITE_AUTH0_AUDIENCE=https://api.mediassistai
```
