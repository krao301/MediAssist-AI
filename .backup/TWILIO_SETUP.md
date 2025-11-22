# Twilio Trial Account Setup & SMS Debug Guide# Twilio Voice Call Setup Guide



## 🚨 Current IssuesThis guide will help you set up Twilio for automated emergency voice calling in MediAssist AI.



1. ✅ **Nearby contacts showing 0** - FIXED! (removed user_id filter)---

2. ⚠️ **SMS sent but not received** - Common with Twilio trial accounts

3. ❌ **Hospital number unverified** - `+17169085212` needs verification## 🚀 Quick Setup (5 minutes)



---### Step 1: Create Twilio Account



## 📱 How to Verify Phone Numbers in Twilio1. Go to **[https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio)**

2. Sign up for a **free trial account**

### Quick Steps:   - You'll get **$15.00 in free credit**

1. Go to: **https://console.twilio.com/us1/develop/phone-numbers/manage/verified**   - No credit card required for trial

2. Click **"+ Add new Caller ID"**3. Verify your email and phone number

3. Enter: **+17169085212**

4. Choose: **"Call me"** or **"Text me"**---

5. Enter the 6-digit code you receive

6. ✅ Done!### Step 2: Get Your Credentials



### Verify BOTH Numbers:Once logged in, you'll see your **Account Dashboard**:

- ✅ **+17166170427** (SOS + Responders) - check if verified

- ⚠️ **+17169085212** (Hospital) - NEEDS verification1. **Account SID**: Copy this (looks like `ACxxxxxxxxxxxxxxxxxxxx`)

2. **Auth Token**: Click "Show" and copy it

---

---

## 🔍 Why SMS Says "Sent" But You Don't Receive It

### Step 3: Get a Phone Number

### Check Your SMS Status

1. In the Twilio Console, go to **Phone Numbers** → **Manage** → **Buy a number**

Your recent SMS: `SM64d3883ab8771ce4cfee69216bb6a11e`2. Search for a number in your country

3. Filter by **Voice** capability

**Check status here:**4. Click **Buy** (free with trial credit)

https://console.twilio.com/us1/monitor/logs/sms5. Copy your new phone number (format: `+1234567890`)



Look for the status:---

- ✅ `delivered` - Message was delivered successfully

- ⏳ `sent` - Sent to carrier (may take 30-60 seconds on trial)### Step 4: Update .env File

- ⚠️ `queued` - Waiting to send

- ❌ `failed` - Delivery failed (see error code)Open `/api/.env` and replace the placeholders:

- ❌ `undelivered` - Carrier rejected message

```bash

### Common Reasons for Non-Delivery:# Twilio credentials for voice calling (get from https://console.twilio.com)

TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx  # Your Account SID from Step 2

1. **Carrier blocking** - Some carriers block trial account messagesTWILIO_AUTH_TOKEN=your_auth_token_here      # Your Auth Token from Step 2

2. **Number not verified** - MUST verify receiving number firstTWILIO_FROM_NUMBER=+1234567890              # Your Twilio phone number from Step 3

3. **Trial account limits** - Limited to verified numbers only```

4. **SMS delay** - Can take 30-60 seconds

5. **Rate limiting** - Too many SMS to same number quickly**Example:**

```bash

---TWILIO_ACCOUNT_SID=AC1234567890abcdef1234567890abcdef

TWILIO_AUTH_TOKEN=abcd1234efgh5678ijkl9012mnop3456

## 🔧 Email Backup (Recommended for Hackathon Demo)TWILIO_FROM_NUMBER=+15551234567

```

For maximum reliability during demo, let's add **email notifications** as backup!

---

### Option 1: Gmail SMTP (Easiest - 2 min setup)

### Step 5: Configure TwiML Webhook URLs

**Pros:** Free, instant setup, no API keys needed  

**Cons:** Need app password (not your Gmail password)When Twilio makes a call, it needs to know what to say. We need to tell Twilio where to find our voice scripts.



```python1. **Get Your Public URL**:

import smtplib   - For **production**: Use your deployed API URL (e.g., `https://api.mediassistai.com`)

from email.mime.text import MIMEText   - For **local testing**: Use **ngrok** to expose your local server:

from email.mime.multipart import MIMEMultipart     ```bash

     # Install ngrok (macOS)

def send_emergency_email(     brew install ngrok

    to_email: str,     

    subject: str,     # Expose your local API (port 8000)

    emergency_type: str,     ngrok http 8000

    severity: str,     

    location_link: str,     # Copy the HTTPS URL (e.g., https://abc123.ngrok.io)

    instructions: str = None     ```

):

    """Send emergency email via Gmail SMTP"""2. **Update TwiML URLs** in `/api/app/services/voice_call.py`:

       

    # Create message   Replace `https://api.mediassistai.com` with your URL:

    msg = MIMEMultipart('alternative')   

    msg['Subject'] = f"🚨 {subject}"   ```python

    msg['From'] = os.getenv('GMAIL_ADDRESS')   # Line 48-49

    msg['To'] = to_email   url=f"https://YOUR_URL_HERE/voice/sos-message?incident_id={incident_id}",

       

    # HTML content   # Line 95-96

    html = f"""   url=f"https://YOUR_URL_HERE/voice/contact-alert?incident_id={incident_id}&contact_id={contact_id}",

    <html>   ```

      <body style="font-family: Arial, sans-serif;">

        <h2 style="color: #dc2626;">🚨 EMERGENCY ALERT</h2>---

        <p><strong>Type:</strong> {emergency_type}</p>

        <p><strong>Severity:</strong> <span style="color: #dc2626;">{severity}</span></p>### Step 6: Test the Setup

        <p><strong>Location:</strong> <a href="{location_link}">View on Google Maps</a></p>

        {f'<h3>Instructions:</h3><p>{instructions}</p>' if instructions else ''}1. **Restart your API server**:

        <hr>   ```bash

        <p style="color: #666; font-size: 12px;">Sent by MediAssist AI Emergency System</p>   cd api

      </body>   source venv/bin/activate  # or .\venv\Scripts\activate on Windows

    </html>   uvicorn app.main:app --reload

    """   ```

    

    msg.attach(MIMEText(html, 'html'))2. **Test with a simple emergency**:

       - Open the web app at `http://localhost:5173`

    # Send via Gmail   - Click "New Emergency"

    try:   - Type: **"elderly grandfather collapsed and is not breathing"**

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:   - The system should:

            server.login(     - ✅ Detect cardiac arrest with high confidence

                os.getenv('GMAIL_ADDRESS'),     - ✅ Mark as CRITICAL severity

                os.getenv('GMAIL_APP_PASSWORD')     - ✅ Detect unresponsiveness

            )     - ✅ Auto-trigger SOS call to `7166170427`

            server.send_message(msg)

        return {"success": True, "method": "email"}3. **Check backend logs** for:

    except Exception as e:   ```

        print(f"❌ Email failed: {e}")   🚨 CRITICAL EMERGENCY DETECTED: cardiac_arrest (CRITICAL)

        return {"success": False, "error": str(e)}      Auto-triggering SOS call to 7166170427

```   ✅ SOS call initiated successfully

   ```

**Setup Gmail App Password:**

1. Go to: https://myaccount.google.com/apppasswords---

2. Select app: "Mail"

3. Select device: "Other" → type "MediAssist"## 📋 When SOS Calls Are Triggered

4. Click "Generate"

5. Copy the 16-character passwordThe system triggers SOS for **ANY severe/critical emergency**:

6. Add to `.env`:

   ```### ✅ SOS **WILL** be triggered when:

   GMAIL_ADDRESS=your_email@gmail.com- Emergency is **CRITICAL or SEVERE** (cardiac arrest, severe bleeding, stroke, etc.)

   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx- Regardless of whether the person is:

   ```  - Helping themselves (first-person: "I have chest pain")

  - Being helped by someone else ("My grandfather has chest pain")

### Option 2: SendGrid (Professional)  - Responsive or unresponsive



**Pros:** Free 100 emails/day, professional, detailed analytics  ### ❌ SOS **WILL NOT** be triggered when:

**Cons:** Requires signup and API key- Emergency is **MODERATE** severity (minor cuts, sprains, mild pain)

- Confidence is too low (ambiguous symptoms → asks clarifying questions)

```bash

pip install sendgrid### Examples:

```

| Input | SOS Triggered? | Reason |

```python|-------|---------------|--------|

from sendgrid import SendGridAPIClient| "elderly man collapsed and not breathing" | ✅ YES | CRITICAL cardiac arrest |

from sendgrid.helpers.mail import Mail| "I have severe chest pain" | ✅ YES | CRITICAL heart attack |

| "my grandfather is having a stroke" | ✅ YES | CRITICAL stroke |

def send_emergency_email(to_email, subject, html_content):| "someone is choking and can't breathe" | ✅ YES | CRITICAL choking |

    message = Mail(| "I cut my finger while cooking" | ❌ NO | MODERATE injury |

        from_email=('emergency@mediassist.ai', 'MediAssist Emergency'),

        to_emails=to_email,---

        subject=subject,

        html_content=html_content## 🔧 Troubleshooting

    )

    ### Problem: "Call failed" error

    try:

        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))**Solution:**

        response = sg.send(message)1. Check your Twilio credentials in `.env`

        return {"success": True, "status_code": response.status_code}2. Verify your Twilio account has credit

    except Exception as e:3. Check backend logs for error messages

        return {"success": False, "error": str(e)}

```---



**Setup:**### Problem: "Unable to reach TwiML endpoint"

1. Sign up: https://signup.sendgrid.com/

2. Verify email**Solution:**

3. Create API key: https://app.sendgrid.com/settings/api_keys1. Verify your webhook URL is publicly accessible

4. Add to `.env`: `SENDGRID_API_KEY=SG.xxxxx`2. If using ngrok, make sure it's running

3. Check that your API server is running on port 8000

---4. Test the endpoint directly: `https://YOUR_URL/voice/sos-message?incident_id=1`



## ✅ Quick Action Plan---



### 1. Verify Hospital Number (2 minutes)### Problem: Twilio trial limitations

```

Visit: https://console.twilio.com/us1/develop/phone-numbers/manage/verified**Trial accounts have restrictions:**

Add: +17169085212- ⚠️ Can only call **verified phone numbers**

Verify via call or text- To call any number, **upgrade to paid account** ($20+ minimum)

```

**To verify a number during trial:**

### 2. Test Nearby Contacts Fix (NOW!)1. Go to **Phone Numbers** → **Verified Caller IDs**

The backend has auto-reloaded with the fix. Test again:2. Click **Add a new number**

- Click SOS button3. Enter the emergency contact number

- Say "severe chest pain"4. Verify with the code sent via SMS

- **Should now see:** "DEBUG: Found 5 total contacts in database"

- **Should now see:** "Found 5 people within 500m"---



### 3. Check SMS Delivery Status### Problem: Voice call not working but SMS works

```

Visit: https://console.twilio.com/us1/monitor/logs/sms**Solution:**

Find: SM64d3883ab8771ce4cfee69216bb6a11e- Ensure your Twilio phone number has **Voice** capability enabled

Check: Why it didn't deliver- Check **Phone Numbers** → **Manage** → **Active Numbers** → Click your number

```- Under **Capabilities**, verify **Voice** is checked



### 4. Add Email Backup (Optional but Recommended)---

**Want me to add Gmail email notifications?**

## 🎯 Advanced Configuration

Just tell me:

- [ ] Yes, add Gmail email backup### Customize Voice Messages

- [ ] No, Twilio SMS is enough

- [ ] Yes, but use SendGrid insteadEdit `/api/app/routes/voice.py` to customize what Twilio says:



---```python

# SOS message (line 20-25)

## 🎯 What Should Work Nowmessage = f"Emergency alert from MediAssist AI. " \

          f"A {emergency_type.replace('_', ' ')} emergency has been reported. " \

After verifying the hospital number, you should see:          f"Location: {latitude}, {longitude}. " \

          f"Caller requires immediate assistance. This is a critical emergency."

```

🚨 CRITICAL EMERGENCY DETECTED: chest_pain_cardiac (CRITICAL)# Contact alert message (line 48-52)

   Initiating full emergency response...message = "Emergency alert. Your help is needed for a nearby medical emergency. " \

   📞 Calling SOS contact: 7166170427          "Press 1 to confirm you can help, or press 2 if you cannot assist."

   💬 Sending SOS SMS to 7166170427```

   🏥 Finding and notifying nearest hospital...

      Hospital: Millard Fillmore Suburban Hospital (calling 7169085212)### Change Voice Settings

   👥 Finding nearby people to alert...

      DEBUG: Querying database for contacts...In `/api/app/services/voice_call.py`, line 48-51:

      DEBUG: Found 5 total contacts in database (user_id filter: OFF)

      DEBUG: John Responder is 68.9m away (radius=500m)```python

      DEBUG: Jane Helper is 68.9m away (radius=500m)call = client.calls.create(

      DEBUG: Bob Neighbor is 137.8m away (radius=500m)    to=to_number,

      DEBUG: Alice Nearby is 137.8m away (radius=500m)    from_=twilio_from_number,

      DEBUG: Mike Close is 206.7m away (radius=500m)    url=f"https://YOUR_URL/voice/sos-message?incident_id={incident_id}",

      Found 5 people within 500m    method="GET",

      Alerting: John Responder (68.9m away) at 7166170427    status_callback=f"https://YOUR_URL/voice/call-status",  # Optional: track call status

      Alerting: Jane Helper (68.9m away) at 7166170427    timeout=30,  # Ring for 30 seconds before timeout

      Alerting: Bob Neighbor (137.8m away) at 7166170427    record=True   # Record the call for quality assurance

      Alerting: Alice Nearby (137.8m away) at 7166170427)

      Alerting: Mike Close (206.7m away) at 7166170427```

   ✅ Emergency response initiated successfully

---

✅ Emergency call initiated to 7166170427: CAxxxx

✅ SOS SMS sent: {...}## 🌐 Production Deployment

✅ Hospital call initiated to 7169085212: CAxxxx

✅ Hospital SMS sent: SMxxxxWhen deploying to production:

✅ Called John Responder: CAxxxx

✅ SMS sent to John Responder: SMxxxx1. **Replace ngrok URL** with your actual domain

✅ Called Jane Helper: CAxxxx2. **Add SSL certificate** (required for Twilio webhooks)

✅ SMS sent to Jane Helper: SMxxxx3. **Set up call logging** to track emergency calls

... (3 more responders)4. **Configure error alerts** (email/Slack when calls fail)

```5. **Add call recording** for quality assurance

6. **Upgrade to Twilio paid plan** to call any number

**Total:** 7 calls + 7 SMS 🎉

---

---

## 📞 Testing Checklist

## 💡 My Recommendation

- [ ] Twilio credentials added to `.env`

For the **hackathon demo**, I suggest:- [ ] API server restarted

- [ ] TwiML webhook URLs updated

1. ✅ **Verify both phone numbers** (required - 2 min)- [ ] Test emergency: "person collapsed and unconscious"

2. ✅ **Test nearby contacts fix** (should work now!)- [ ] SOS call received at emergency number

3. ✅ **Add Gmail email backup** (5 min setup)- [ ] Backend logs show successful call

   - More reliable for demo- [ ] Voice message is clear and audible

   - Judges can see notification instantly- [ ] Contact alert system works (press 1/2 response)

   - Professional multi-channel approach

   - Shows good engineering (fallback system)---



**Ready to add email notifications? Just say the word!** 📧## 🎉 Success!


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
