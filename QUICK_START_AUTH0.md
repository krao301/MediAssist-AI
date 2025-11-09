# 🚀 Quick Start - MediAssist AI with Auth0

## ⚡ TL;DR

1. **Get Auth0 Credentials** → https://auth0.com (free account)
2. **Configure `.env`** → `web/.env` with your Auth0 domain and client ID
3. **Run Backend** → `cd api; venv\Scripts\activate; uvicorn app.main:app --reload`
4. **Run Frontend** → `cd web; npm install; npm run dev`
5. **Visit** → http://localhost:5173 and sign in!

## 📋 Auth0 Quick Config

### In Auth0 Dashboard:
1. Create SPA Application
2. Add to **Allowed Callback URLs**: `http://localhost:5173`
3. Add to **Allowed Logout URLs**: `http://localhost:5173`
4. Add to **Allowed Web Origins**: `http://localhost:5173`
5. Copy **Domain** and **Client ID**

### In Your `.env` File:
```env
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your-client-id
VITE_AUTH0_AUDIENCE=https://api.mediassistai
```

## 🎯 What You Get

✅ **Sign-in page** - Users must authenticate first  
✅ **User profile** - Photo, name, email, logout button  
✅ **Protected routes** - All pages secured  
✅ **Secure API calls** - Tokens automatically attached  

---

For detailed setup, see: **AUTH0_SETUP.md** or **AUTH0_IMPLEMENTATION.md**
