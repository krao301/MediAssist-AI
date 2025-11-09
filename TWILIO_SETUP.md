# Twilio Voice Call Setup Guide

This guide will help you set up Twilio for automated emergency voice calling in MediAssist AI.

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Create Twilio Account

1. Go to **[https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio)**
2. Sign up for a **free trial account**
   - You'll get **$15.00 in free credit**
   - No credit card required for trial
3. Verify your email and phone number

---

### Step 2: Get Your Credentials

Once logged in, you'll see your **Account Dashboard**:

1. **Account SID**: Copy this (looks like `ACxxxxxxxxxxxxxxxxxxxx`)
2. **Auth Token**: Click "Show" and copy it

---

### Step 3: Get a Phone Number

1. In the Twilio Console, go to **Phone Numbers** → **Manage** → **Buy a number**
2. Search for a number in your country
3. Filter by **Voice** capability
4. Click **Buy** (free with trial credit)
5. Copy your new phone number (format: `+1234567890`)

---

### Step 4: Update .env File

Open `/api/.env` and replace the placeholders:

```bash
# Twilio credentials for voice calling (get from https://console.twilio.com)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx  # Your Account SID from Step 2
TWILIO_AUTH_TOKEN=your_auth_token_here      # Your Auth Token from Step 2
TWILIO_FROM_NUMBER=+1234567890              # Your Twilio phone number from Step 3
```

**Example:**
```bash
TWILIO_ACCOUNT_SID=AC1234567890abcdef1234567890abcdef
TWILIO_AUTH_TOKEN=abcd1234efgh5678ijkl9012mnop3456
TWILIO_FROM_NUMBER=+15551234567
```

---

### Step 5: Configure TwiML Webhook URLs

When Twilio makes a call, it needs to know what to say. We need to tell Twilio where to find our voice scripts.

1. **Get Your Public URL**:
   - For **production**: Use your deployed API URL (e.g., `https://api.mediassistai.com`)
   - For **local testing**: Use **ngrok** to expose your local server:
     ```bash
     # Install ngrok (macOS)
     brew install ngrok
     
     # Expose your local API (port 8000)
     ngrok http 8000
     
     # Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
     ```

2. **Update TwiML URLs** in `/api/app/services/voice_call.py`:
   
   Replace `https://api.mediassistai.com` with your URL:
   
   ```python
   # Line 48-49
   url=f"https://YOUR_URL_HERE/voice/sos-message?incident_id={incident_id}",
   
   # Line 95-96
   url=f"https://YOUR_URL_HERE/voice/contact-alert?incident_id={incident_id}&contact_id={contact_id}",
   ```

---

### Step 6: Test the Setup

1. **Restart your API server**:
   ```bash
   cd api
   source venv/bin/activate  # or .\venv\Scripts\activate on Windows
   uvicorn app.main:app --reload
   ```

2. **Test with a simple emergency**:
   - Open the web app at `http://localhost:5173`
   - Click "New Emergency"
   - Type: **"elderly grandfather collapsed and is not breathing"**
   - The system should:
     - ✅ Detect cardiac arrest with high confidence
     - ✅ Mark as CRITICAL severity
     - ✅ Detect unresponsiveness
     - ✅ Auto-trigger SOS call to `7166170427`

3. **Check backend logs** for:
   ```
   🚨 CRITICAL EMERGENCY DETECTED: cardiac_arrest (CRITICAL)
      Auto-triggering SOS call to 7166170427
   ✅ SOS call initiated successfully
   ```

---

## 📋 When SOS Calls Are Triggered

The system triggers SOS for **ANY severe/critical emergency**:

### ✅ SOS **WILL** be triggered when:
- Emergency is **CRITICAL or SEVERE** (cardiac arrest, severe bleeding, stroke, etc.)
- Regardless of whether the person is:
  - Helping themselves (first-person: "I have chest pain")
  - Being helped by someone else ("My grandfather has chest pain")
  - Responsive or unresponsive

### ❌ SOS **WILL NOT** be triggered when:
- Emergency is **MODERATE** severity (minor cuts, sprains, mild pain)
- Confidence is too low (ambiguous symptoms → asks clarifying questions)

### Examples:

| Input | SOS Triggered? | Reason |
|-------|---------------|--------|
| "elderly man collapsed and not breathing" | ✅ YES | CRITICAL cardiac arrest |
| "I have severe chest pain" | ✅ YES | CRITICAL heart attack |
| "my grandfather is having a stroke" | ✅ YES | CRITICAL stroke |
| "someone is choking and can't breathe" | ✅ YES | CRITICAL choking |
| "I cut my finger while cooking" | ❌ NO | MODERATE injury |

---

## 🔧 Troubleshooting

### Problem: "Call failed" error

**Solution:**
1. Check your Twilio credentials in `.env`
2. Verify your Twilio account has credit
3. Check backend logs for error messages

---

### Problem: "Unable to reach TwiML endpoint"

**Solution:**
1. Verify your webhook URL is publicly accessible
2. If using ngrok, make sure it's running
3. Check that your API server is running on port 8000
4. Test the endpoint directly: `https://YOUR_URL/voice/sos-message?incident_id=1`

---

### Problem: Twilio trial limitations

**Trial accounts have restrictions:**
- ⚠️ Can only call **verified phone numbers**
- To call any number, **upgrade to paid account** ($20+ minimum)

**To verify a number during trial:**
1. Go to **Phone Numbers** → **Verified Caller IDs**
2. Click **Add a new number**
3. Enter the emergency contact number
4. Verify with the code sent via SMS

---

### Problem: Voice call not working but SMS works

**Solution:**
- Ensure your Twilio phone number has **Voice** capability enabled
- Check **Phone Numbers** → **Manage** → **Active Numbers** → Click your number
- Under **Capabilities**, verify **Voice** is checked

---

## 🎯 Advanced Configuration

### Customize Voice Messages

Edit `/api/app/routes/voice.py` to customize what Twilio says:

```python
# SOS message (line 20-25)
message = f"Emergency alert from MediAssist AI. " \
          f"A {emergency_type.replace('_', ' ')} emergency has been reported. " \
          f"Location: {latitude}, {longitude}. " \
          f"Caller requires immediate assistance. This is a critical emergency."

# Contact alert message (line 48-52)
message = "Emergency alert. Your help is needed for a nearby medical emergency. " \
          "Press 1 to confirm you can help, or press 2 if you cannot assist."
```

### Change Voice Settings

In `/api/app/services/voice_call.py`, line 48-51:

```python
call = client.calls.create(
    to=to_number,
    from_=twilio_from_number,
    url=f"https://YOUR_URL/voice/sos-message?incident_id={incident_id}",
    method="GET",
    status_callback=f"https://YOUR_URL/voice/call-status",  # Optional: track call status
    timeout=30,  # Ring for 30 seconds before timeout
    record=True   # Record the call for quality assurance
)
```

---

## 🌐 Production Deployment

When deploying to production:

1. **Replace ngrok URL** with your actual domain
2. **Add SSL certificate** (required for Twilio webhooks)
3. **Set up call logging** to track emergency calls
4. **Configure error alerts** (email/Slack when calls fail)
5. **Add call recording** for quality assurance
6. **Upgrade to Twilio paid plan** to call any number

---

## 📞 Testing Checklist

- [ ] Twilio credentials added to `.env`
- [ ] API server restarted
- [ ] TwiML webhook URLs updated
- [ ] Test emergency: "person collapsed and unconscious"
- [ ] SOS call received at emergency number
- [ ] Backend logs show successful call
- [ ] Voice message is clear and audible
- [ ] Contact alert system works (press 1/2 response)

---

## 🎉 Success!

If you've completed all steps, your MediAssist AI system can now:

✅ Automatically detect CRITICAL emergencies  
✅ Identify when a person is unresponsive  
✅ Trigger voice calls to emergency services  
✅ Alert nearby emergency contacts  
✅ Play automated voice messages with incident details  

**Your AI-powered emergency response system is now fully operational!** 🚑

---

## 📚 Additional Resources

- [Twilio Voice API Documentation](https://www.twilio.com/docs/voice)
- [TwiML Reference](https://www.twilio.com/docs/voice/twiml)
- [Twilio Python SDK](https://www.twilio.com/docs/libraries/python)
- [ngrok Documentation](https://ngrok.com/docs)

---

## 💡 Pro Tips

1. **Use environment-specific URLs**: 
   ```python
   TWIML_BASE_URL = os.getenv("TWIML_BASE_URL", "http://localhost:8000")
   ```

2. **Add retry logic** for failed calls:
   ```python
   max_retries = 3
   for attempt in range(max_retries):
       try:
           call = client.calls.create(...)
           break
       except Exception as e:
           if attempt == max_retries - 1:
               raise
   ```

3. **Log all calls** to database for analytics:
   ```python
   db.add(CallLog(
       incident_id=incident_id,
       to_number=to_number,
       status="initiated",
       call_sid=call.sid
   ))
   ```

---

**Need help?** Check the backend logs for detailed error messages or open an issue on GitHub.
