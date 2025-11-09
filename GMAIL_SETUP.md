# Gmail SMTP Setup for Email Notifications

## 🚀 Quick Setup Guide

Your email notifications are ready! Just need to configure Gmail credentials.

---

## 📧 Email Configuration

**Configured Email Recipients:**
- **SOS Contact Email:** sankinenihrithikesh@gmail.com
- **Hospital Email:** shritikesh8999@gmail.com  
- **Nearby Responders Email:** sankinenihrithikesh@gmail.com

---

## 🔐 Step 1: Create Gmail App Password

You **cannot** use your regular Gmail password for this. You need an "App Password".

### How to Get App Password:

1. **Enable 2-Step Verification** (required first):
   - Go to: https://myaccount.google.com/security
   - Click **"2-Step Verification"**
   - Follow steps to enable it (if not already enabled)

2. **Create App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - OR Google Account → Security → 2-Step Verification → App passwords (at bottom)
   
3. **Generate Password**:
   - Select app: **"Mail"**
   - Select device: **"Other (Custom name)"**
   - Type: **"MediAssist Emergency System"**
   - Click **"Generate"**
   
4. **Copy the Password**:
   - You'll get a 16-character password like: `abcd efgh ijkl mnop`
   - ⚠️ **Copy it immediately** - you can't see it again!

---

## 📝 Step 2: Update .env File

Open `/api/.env` and replace these lines:

```env
# Gmail SMTP for Email Notifications
GMAIL_ADDRESS=YOUR_GMAIL_HERE
GMAIL_APP_PASSWORD=YOUR_APP_PASSWORD_HERE
```

**Replace with your actual values:**

```env
# Gmail SMTP for Email Notifications
GMAIL_ADDRESS=sankinenihrithikesh@gmail.com
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
```

**⚠️ IMPORTANT:** 
- Use the **16-character app password**, NOT your regular Gmail password
- You can keep the spaces in the app password (Gmail accepts both formats)
- Or remove spaces: `abcdefghijklmnop`

---

## ✅ Step 3: Save and Test

1. **Save** the `.env` file
2. **Backend will auto-reload** (if running with `--reload`)
3. **Test** by clicking SOS button

---

## 🎯 What You'll Get

### When CRITICAL Emergency is Triggered:

**Total Notifications: 7 SMS + 7 Emails**

#### 📱 SMS Notifications:
1. ✅ SOS SMS to 7166170427
2. ✅ Hospital SMS to 7169085212
3-7. ✅ 5 Responder SMS to 7166170427

#### 📧 Email Notifications (NEW!):
1. ✅ SOS Email to sankinenihrithikesh@gmail.com
2. ✅ Hospital Email to shritikesh8999@gmail.com
3-7. ✅ 5 Responder Emails to sankinenihrithikesh@gmail.com

---

## 📊 Email Content

### SOS Email:
```
Subject: 🚨 EMERGENCY ALERT - Immediate Response Required

Body:
- Emergency Type: Chest Pain Cardiac
- Severity: CRITICAL
- Incident ID: #0
- [View Location on Google Maps] (button)
- "Emergency Services Notified" box
```

### Hospital Email:
```
Subject: 🚨 INCOMING PATIENT - ETA 7 minutes

Body:
- Emergency Type: Chest Pain Cardiac
- Severity: CRITICAL
- Incident ID: #0
- [View Location on Google Maps] (button)
- Instructions: "Patient ETA: 7 minutes. Prepare emergency bay."
```

### Responder Email:
```
Subject: 🚨 HELP NEEDED - Medical Emergency 68.9m away

Body:
- Emergency Type: Chest Pain Cardiac
- Severity: CRITICAL
- Incident ID: #0
- [View Location on Google Maps] (button)
- First Aid Instructions:
  1. Keep person calm and still
  2. Loosen tight clothing
  3. Help them sit or lie down
  4. Give aspirin if available
```

All emails are **beautifully formatted HTML** with:
- 🎨 Professional styling
- 🚨 Red emergency header
- 📍 Clickable Google Maps link
- 📋 Clear, numbered instructions
- ✅ Status indicators

---

## 🐛 Troubleshooting

### "Username and Password not accepted"
- ❌ You're using regular Gmail password
- ✅ Use the 16-character App Password instead

### "Authentication failed"
- Make sure 2-Step Verification is enabled
- Create a new App Password
- Check for typos in .env file

### Not receiving emails
- Check spam/junk folder
- Verify email address is correct in .env
- Check backend logs for "✅ Email sent" messages

### "Gmail credentials not configured"
- Make sure GMAIL_ADDRESS and GMAIL_APP_PASSWORD are in .env
- Make sure no extra quotes around values
- Restart backend if you added them while running

---

## 🔒 Security Notes

1. **Never commit .env to Git** - Already in .gitignore
2. **App password is safer than main password** - Limited scope
3. **Can revoke app passwords anytime** - Won't affect main account
4. **Each project should have its own app password**

---

## 🚀 Ready to Test!

Once you've updated `.env` with your Gmail credentials:

```bash
# Backend should auto-reload
# If not, restart it:
cd /Users/hrithikeshsankineni/Documents/MediAssist-AI/api
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

Then:
1. Go to http://localhost:5173
2. Click SOS button
3. Say "severe chest pain"
4. Check your email! 📧

---

## 📧 Expected Backend Logs

```
🚨 CRITICAL EMERGENCY DETECTED: chest_pain_cardiac (CRITICAL)
   Initiating full emergency response...
   📞 Calling SOS contact: 7166170427
   💬 Sending SOS SMS to 7166170427
   📧 Sending SOS Email to sankinenihrithikesh@gmail.com
   🏥 Finding and notifying nearest hospital...
      Hospital: Millard Fillmore Suburban Hospital (calling 7169085212)
   👥 Finding nearby people to alert...
      DEBUG: Found 5 total contacts in database
      Found 5 people within 500m
      Alerting: John Responder (68.9m away) at 7166170427

✅ Emergency call initiated to 7166170427: CAxxxx
✅ SOS SMS sent: {...}
✅ Email sent to sankinenihrithikesh@gmail.com
✅ Hospital call initiated to 7169085212: CAxxxx
✅ Hospital SMS sent: SMxxxx
✅ Email sent to shritikesh8999@gmail.com
✅ Called John Responder
✅ SMS sent to John Responder: {...}
✅ Email sent to John Responder: {...}
... (4 more responders)
```

---

## 💡 Why Email is Better for Demo

1. **✅ Instant Delivery** - No carrier delays like SMS
2. **✅ Professional Formatting** - Beautiful HTML emails
3. **✅ More Reliable** - Not limited by Twilio trial
4. **✅ Detailed Information** - Can include formatted instructions
5. **✅ Clickable Maps** - Direct link to Google Maps
6. **✅ Easy to Show** - Open inbox and show judges

**Perfect for hackathon presentation!** 🏆

---

## 📱 Current Setup Summary

| Channel | SOS Contact | Hospital | Nearby People |
|---------|-------------|----------|---------------|
| **Call** | 7166170427 | 7169085212 | 7166170427 (5x) |
| **SMS** | 7166170427 | 7169085212 | 7166170427 (5x) |
| **Email** | sankinenihrithikesh@gmail.com | shritikesh8999@gmail.com | sankinenihrithikesh@gmail.com (5x) |

**Total per emergency:** 7 calls + 7 SMS + 7 emails = **21 notifications!** 🚨

---

Need help? Just ask! 🙋‍♂️
