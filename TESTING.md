# Testing Guide

## 🔄 Auth0 Login Testing (NEW)

### Force Fresh Login Every Time

**What Changed:**
- Every role selection now shows the **full Auth0 login/signup page**
- No auto-login with cached credentials
- Users can freely choose accounts or sign up new

**Test Steps:**
1. Visit http://localhost:5173
2. Click any role (Citizen, Hospital, or First Responder)
3. ✅ Should see full Auth0 login page (not "Authorize as abc@gmail.com")
4. Can sign up or login with any account
5. After auth, redirected to home page

**If You See Auto-Login:**
- Click the yellow "🔄 Click here to sign out..." button on login page
- Or use incognito mode (Ctrl+Shift+N)
- Or clear browser cache

**Parameters Used:**
```typescript
authorizationParams: {
  prompt: 'login',      // Force login screen
  max_age: 0,           // Ignore existing sessions
  screen_hint: 'signup' // Show signup tab
}
```

---

## Manual Testing Checklist

### 1. Backend API Tests

**Health Check**
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy"}
```

**Triage Endpoint**
```bash
curl -X POST http://localhost:8000/triage \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Person not breathing, unconscious",
    "locale": "en-US",
    "age_group": "adult"
  }'
# Expected: { "type": "cardiac_arrest", "severity": "critical", ... }
```

**Create Incident**
```bash
curl -X POST http://localhost:8000/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "latitude": 42.9634,
    "longitude": -78.7384,
    "emergency_type": "cardiac_arrest"
  }'
# Expected: { "id": 1, "status": "active", ... }
```

**Send Alerts** (requires contacts)
```bash
curl -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "incident_id": 1,
    "latitude": 42.9634,
    "longitude": -78.7384
  }'
# Expected: { "sent": 2, "contacts": [...] }
```

**Hospital Routing**
```bash
curl -X POST http://localhost:8000/route \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 42.9634,
    "longitude": -78.7384
  }'
# Expected: { "hospital": "...", "distance": ..., ... }
```

### 2. Frontend Tests

**Permissions Check**
- Open http://localhost:5173
- Click "Grant Permissions"
- Should prompt for geolocation and microphone access
- Status banner should turn green after granting

**SOS Button Flow**
1. Click large red SOS button
2. Should navigate to incident screen
3. Microphone button should appear
4. Text input should be available

**Voice Input**
1. Click microphone icon
2. Say: "Someone is choking on food"
3. Should see transcription appear
4. Click "Analyze" or press Enter

**AI Triage Response**
- Should show emergency type badge (e.g., "Choking - Serious")
- Should display 4 steps for choking
- Each step should have "Start" button

**Step Timer**
1. Click "Start" on first step
2. Timer should count down (e.g., 60s → 59s → ...)
3. When <10s, card should pulse red
4. At 0s, should show completion checkmark

**CPR Metronome**
- For cardiac arrest emergency
- Click "Start Metronome"
- Should hear 800Hz beep every ~0.5s (120 BPM)
- Blue circle should pulse with beat

**Contacts Management**
1. Navigate to /contacts
2. Fill form: Name, Phone, Address
3. Click "Add Contact"
4. Should appear in list
5. Click "Delete" → confirm prompt

**Incident Summary**
1. Complete emergency flow
2. Click "End Incident"
3. Should show timeline with timestamps
4. Click "Download Report" → JSON file downloads

### 3. Integration Tests

**Full Emergency Scenario**
```
1. User clicks SOS → grants permissions
2. Speaks: "Heart attack, person unconscious"
3. AI classifies: "Cardiac Arrest - Critical"
4. User starts Step 1: "Check Responsiveness" (10s)
5. User starts Step 2: "Call 911" (30s)
6. User starts Step 3: "Start CPR" (ongoing)
   - Metronome plays at 120 BPM
7. Alert sent to 2 contacts within 500m
8. Hospital shown: "Buffalo General - 2.3km - 5min"
9. User clicks "End Incident"
10. Summary shows 8min 30s duration, 3/4 steps completed
```

**Geofencing Test**
```python
# In api/tests/test_geo.py
def test_geofence():
    # User location: Buffalo, NY
    user_lat, user_lon = 42.9634, -78.7384
    
    # Contact 1: 200m away (should receive alert)
    contact1 = Contact(latitude=42.9654, longitude=-78.7384)
    distance1 = haversine(user_lat, user_lon, contact1.latitude, contact1.longitude)
    assert distance1 < 500
    
    # Contact 2: 700m away (should NOT receive alert)
    contact2 = Contact(latitude=42.9700, longitude=-78.7384)
    distance2 = haversine(user_lat, user_lon, contact2.latitude, contact2.longitude)
    assert distance2 > 500
```

### 4. Edge Cases

**No Contacts Nearby**
- Start emergency with no contacts within 500m
- Should show: "No contacts nearby to alert"

**Voice Input Failure**
- Deny microphone permission
- Should show text input fallback
- Type emergency description manually

**AI Triage Failure**
- Invalid Gemini API key
- Should fall back to keyword matching
- Still classifies basic emergencies

**Offline Mode** (PWA)
- Load app online first
- Turn off network
- App should still work (service worker cache)
- API calls will fail gracefully

### 5. Performance Tests

**API Response Times**
- Triage: <2s (Gemini API call)
- Alerts: <1s (Twilio SMS)
- Route: <1s (Maps API)
- Incidents: <100ms (database)

**Frontend Load Time**
- Initial load: <2s
- Route navigation: <100ms
- PWA install prompt: appears on 2nd visit

### 6. Security Tests

**Auth0 JWT Validation**
```bash
# Invalid token
curl http://localhost:8000/incidents \
  -H "Authorization: Bearer invalid_token"
# Expected: 401 Unauthorized

# Valid token (get from Auth0)
curl http://localhost:8000/incidents \
  -H "Authorization: Bearer eyJ..."
# Expected: 200 OK with incidents
```

**CORS Check**
```bash
curl -H "Origin: https://evil.com" http://localhost:8000/health
# Expected: CORS error (not in allowed origins)
```

### 7. Automated Tests

**Backend**
```bash
cd api
pytest tests/ -v --cov=app
```

**Frontend**
```bash
cd web
npm run test
npm run test:coverage
```

### 8. Lighthouse Audit (PWA Score)

```bash
cd web
npm run build
npx serve dist -p 5173

# Open Chrome DevTools → Lighthouse
# Run audit with:
# - Performance
# - PWA
# - Accessibility
# Target scores: 90+ on all categories
```

**Expected PWA Checklist**:
- ✅ Registers a service worker
- ✅ Provides a manifest.json
- ✅ Uses HTTPS (in production)
- ✅ Responsive design
- ✅ Fast load time (<3s)
- ✅ Works offline

---

## Common Issues

### Backend

**Issue**: `ModuleNotFoundError: No module named 'app'`
```bash
# Solution: Run from api/ directory
cd api
python -m pytest
```

**Issue**: Gemini API quota exceeded
```bash
# Solution: Switch to keyword fallback
# In .env, remove GEMINI_API_KEY
# Will use built-in FIRST_AID_KB
```

**Issue**: Twilio auth error
```bash
# Solution: Check credentials
echo $TWILIO_ACCOUNT_SID
echo $TWILIO_AUTH_TOKEN
# Get from: https://console.twilio.com
```

### Frontend

**Issue**: `Failed to fetch` from API
```bash
# Solution: Check API is running
curl http://localhost:8000/health

# Check CORS allowed origins in api/app/main.py
origins = ["http://localhost:5173"]
```

**Issue**: Microphone not working
- Chrome: Settings → Privacy → Microphone → Allow
- Firefox: about:preferences#privacy → Permissions → Microphone
- Safari: Preferences → Websites → Microphone

**Issue**: PWA not installing
- Must use HTTPS in production
- Requires service worker registration
- Check manifest.json is valid
- Visit site twice (triggers install prompt)

---

## Demo Script for Judges

**Time: 3 minutes**

1. **Intro** (15s)
   > "MediAssist AI turns bystanders into lifesavers with AI-powered emergency coaching."

2. **Show SOS Button** (10s)
   > "Tap the big red button in a medical emergency."

3. **Voice Input** (20s)
   > *Click microphone* "Someone collapsed, not breathing"
   > Shows transcription, click Analyze

4. **AI Triage** (30s)
   > "Gemini API classifies this as Cardiac Arrest - Critical"
   > Shows 4 steps: Check → Call 911 → CPR → AED

5. **Start Step 3** (40s)
   > Click "Start CPR", timer begins
   > Metronome plays at 120 BPM (AHA-recommended)
   > "Audio helps maintain correct compression rate"

6. **Auto-Alerts** (20s)
   > "App automatically texts contacts within 500m"
   > Show SMS screenshot on phone

7. **Hospital Routing** (20s)
   > "Shows nearest ER with distance and ETA"
   > Google Maps integration

8. **End & Summary** (25s)
   > Click "End Incident"
   > Shows timeline: 8min 30s, 3 steps completed
   > "Download for EMS handoff"

9. **Sponsor Integrations** (20s)
   > "Built with Auth0 login, Gemini API, ElevenLabs TTS"
   > "Hosted on DigitalOcean with Cloudflare edge workers"
   > "Custom domain from GoDaddy: mediassistai.xyz"

10. **Closing** (10s)
    > "Thank you! Questions?"

---

## Load Testing

```bash
# Install Apache Bench
sudo apt install apache2-utils

# Test triage endpoint
ab -n 100 -c 10 -p triage.json -T application/json \
   http://localhost:8000/triage

# Expected: 50-100 requests/sec
```

```json
// triage.json
{
  "text": "Person choking",
  "locale": "en-US",
  "age_group": "adult"
}
```

---

## Debugging Tips

**Enable verbose logging**:
```python
# In api/app/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Check database state**:
```bash
sqlite3 api/mediassist.db
sqlite> .tables
sqlite> SELECT * FROM incidents;
```

**Frontend console errors**:
```javascript
// In browser console
localStorage.clear()  // Reset state
navigator.permissions.query({name: 'geolocation'})  // Check perms
```

**Network inspection**:
- Chrome DevTools → Network tab
- Filter by Fetch/XHR
- Check request/response payloads
- Look for 4xx/5xx errors
