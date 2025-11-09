# 🚑 MediAssist AI - Auth0 Authentication Setup

## ✅ What's Been Implemented

Your MediAssist AI frontend now has **complete Auth0 authentication**:

1. ✅ **Sign-in page** - Beautiful branded login screen
2. ✅ **Protected routes** - All pages require authentication
3. ✅ **User profile** - Shows user info with logout button
4. ✅ **Secure API calls** - Automatic token attachment to backend requests
5. ✅ **Token management** - Auto-refresh and secure storage

## 🚀 Setup Instructions

### Step 1: Configure Auth0

1. **Create Auth0 Account**
   - Go to https://auth0.com and sign up (free)
   - Create a new tenant (e.g., `mediassist-dev`)

2. **Create Application**
   - Dashboard → Applications → Create Application
   - Choose **Single Page Web Application**
   - Name: "MediAssist AI"

3. **Configure Settings**
   
   Add these URLs to your application settings:
   
   **Allowed Callback URLs:**
   ```
   http://localhost:5173
   ```
   
   **Allowed Logout URLs:**
   ```
   http://localhost:5173
   ```
   
   **Allowed Web Origins:**
   ```
   http://localhost:5173
   ```

   Click **Save Changes**

4. **Get Credentials**
   - Copy your **Domain** (e.g., `mediassist-dev.us.auth0.com`)
   - Copy your **Client ID**

5. **Create API (Optional)**
   - Dashboard → Applications → APIs → Create API
   - Name: `MediAssist API`
   - Identifier: `https://api.mediassistai`

### Step 2: Configure Frontend

```powershell
cd C:\Users\shrav\Desktop\Hackathon\MediAssist-AI\web

# The .env file has been created, now edit it:
notepad .env
```

Update with your Auth0 credentials:
```env
VITE_API_BASE=http://localhost:8000
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your-client-id-here
VITE_AUTH0_AUDIENCE=https://api.mediassistai
```

### Step 3: Install Dependencies (if needed)

Open **Command Prompt** (not PowerShell) or use Git Bash:

```bash
cd C:\Users\shrav\Desktop\Hackathon\MediAssist-AI\web
npm install
```

### Step 4: Run the Application

**Terminal 1 - Backend:**
```powershell
cd C:\Users\shrav\Desktop\Hackathon\MediAssist-AI\api
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend (use Command Prompt or Git Bash):**
```bash
cd C:\Users\shrav\Desktop\Hackathon\MediAssist-AI\web
npm run dev
```

### Step 5: Test Authentication

1. Open http://localhost:5173
2. You should see the **sign-in page**
3. Click "Sign In to Continue"
4. Complete Auth0 login
5. You'll be redirected to the home page with your profile in the top-right

## 📁 Files Created/Modified

### New Files:
- `web/src/components/Auth0Provider.tsx` - Auth0 wrapper
- `web/src/components/ProtectedRoute.tsx` - Route protection
- `web/src/components/UserProfile.tsx` - User info display
- `web/src/lib/useApiAuth.ts` - API token management
- `web/src/vite-env.d.ts` - TypeScript definitions
- `AUTH0_SETUP.md` - Detailed setup guide
- `AUTH0_IMPLEMENTATION.md` - This file

### Modified Files:
- `web/src/main.tsx` - Added Auth0Provider wrapper
- `web/src/App.tsx` - Added ProtectedRoute and useApiAuth
- `web/src/routes/Home.tsx` - Added UserProfile component
- `web/src/lib/api.ts` - Added token management
- `web/.env.example` - Updated with Auth0 fields

## 🎨 Features

### Sign-In Page
- Beautiful branded interface
- Clear call-to-action
- Error handling for missing config
- Responsive design

### User Profile
- Displays user photo, name, and email
- Logout button
- Positioned in top-right corner
- Appears on all pages

### Protected Routes
- All pages require authentication
- Smooth loading states
- Automatic redirect to login
- Preserves navigation after login

### API Security
- Automatic token attachment to all API calls
- Token refresh handling
- Secure localStorage caching
- Works with backend JWT validation

## 🔧 Troubleshooting

### "Auth0 Configuration Missing" Error
- Make sure you've created the `.env` file
- Verify VITE_AUTH0_DOMAIN and VITE_AUTH0_CLIENT_ID are set
- Restart the dev server after changing .env

### "Callback URL mismatch" Error
- Ensure `http://localhost:5173` is in Auth0 Allowed Callback URLs
- No trailing slash

### Backend 401 Errors
- Backend needs to validate Auth0 JWT tokens
- Check `api/app/deps/auth.py` for JWT validation
- Ensure VITE_AUTH0_AUDIENCE matches backend configuration

### PowerShell Script Execution Error
- Use **Command Prompt** or **Git Bash** instead
- Or enable scripts: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## 🎯 Next Steps

1. **Configure Auth0** with your credentials
2. **Test authentication** flow
3. **Update backend** to validate Auth0 tokens (if not already done)
4. **Add user roles** (optional) for admin features
5. **Enable social login** (Google, Facebook, etc.) in Auth0

## 📚 Resources

- [Auth0 Quick Start](https://auth0.com/docs/quickstart/spa/react)
- [Auth0 React SDK Docs](https://auth0.com/docs/libraries/auth0-react)
- [JWT Validation](https://auth0.com/docs/secure/tokens/json-web-tokens/validate-json-web-tokens)

---

**Authentication is now ready!** Just configure Auth0 and you're good to go! 🎉
