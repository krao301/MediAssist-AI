# 🔧 Fix Auth0 Logout Error

## The Problem

When clicking "Sign Out", you're seeing an Auth0 error page instead of being redirected back to the sign-in page.

## ✅ Quick Fix

### Step 1: Configure Allowed Logout URLs in Auth0

1. **Go to your Auth0 Dashboard:**
   - Visit: https://manage.auth0.com
   - Log in to your account

2. **Navigate to your application:**
   - Click **Applications** → **Applications**
   - Select "MediAssist AI" (or your app name)

3. **Scroll to Application URIs section:**
   - Find **Allowed Logout URLs**
   - Add: `http://localhost:5173`
   - **Important:** No trailing slash!

4. **Also verify these are set:**
   - **Allowed Callback URLs:** `http://localhost:5173`
   - **Allowed Web Origins:** `http://localhost:5173`

5. **Click "Save Changes"** at the bottom

### Step 2: Test Logout

1. Refresh your app: http://localhost:5173
2. Click your profile avatar in the navbar
3. Click "Sign Out"
4. ✅ Should redirect to the sign-in page (with 3 role cards)

## 🎯 What We Changed

Updated `UserProfile.tsx` to:
1. Clear Auth0 cache before logout
2. Properly redirect to `window.location.origin`
3. Handle the logout flow cleanly

```typescript
// Clear all Auth0 cache
Object.keys(localStorage).forEach(key => {
  if (key.startsWith('@@auth0spajs@@')) {
    localStorage.removeItem(key);
  }
});

// Logout and redirect
logout({ 
  logoutParams: { 
    returnTo: window.location.origin 
  } 
});
```

## 🚨 Common Issues

### Issue 1: "Invalid logout URL"
**Cause:** Logout URL not configured in Auth0  
**Fix:** Add `http://localhost:5173` to **Allowed Logout URLs**

### Issue 2: Still seeing error after configuration
**Cause:** Auth0 cache not cleared  
**Fix:** 
1. Close all browser tabs
2. Open in incognito mode
3. Or clear browser cache (Ctrl+Shift+Delete)

### Issue 3: Works locally but not in production
**Cause:** Production URL not in Allowed Logout URLs  
**Fix:** Add your production domain:
```
https://yourdomain.com
```

## 📋 Full Auth0 Configuration Checklist

In your Auth0 application settings, make sure ALL these are set:

```
Allowed Callback URLs:
http://localhost:5173

Allowed Logout URLs:
http://localhost:5173

Allowed Web Origins:
http://localhost:5173

Allowed Origins (CORS):
http://localhost:5173
```

For production, add your production URLs to all of these fields.

## 🧪 Test Complete Flow

1. **Sign In:**
   - Visit http://localhost:5173
   - Click a role (Citizen, Hospital, First Responder)
   - Complete Auth0 login
   - ✅ Redirected to home page

2. **Sign Out:**
   - Click avatar in navbar
   - Click "Sign Out"
   - ✅ Redirected back to sign-in page (3-role cards)

3. **Sign In Again:**
   - Choose a different role
   - ✅ Shows full login page (not auto-login)

## 🎯 Production Setup

When deploying to production:

1. **Update Auth0 URLs:**
```
Allowed Callback URLs:
http://localhost:5173, https://yourdomain.com

Allowed Logout URLs:
http://localhost:5173, https://yourdomain.com

Allowed Web Origins:
http://localhost:5173, https://yourdomain.com
```

2. **Update .env.production:**
```
VITE_API_BASE=https://api.yourdomain.com
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your-client-id
VITE_AUTH0_AUDIENCE=https://api.mediassistai
```

---

**After configuring the Allowed Logout URLs, logout should work perfectly!** 🎉
