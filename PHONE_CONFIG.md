# Phone Number Configuration for Testing

## Updated Phone Numbers

For testing purposes, we're now using **different phone numbers** for each type of notification:

### 📱 Phone Number Mapping

| Notification Type | Phone Number | Who Receives |
|------------------|--------------|--------------|
| **SOS Call** | 7166170427 | Emergency contact call |
| **SOS SMS** | 7166170427 | Emergency contact text |
| **Hospital Call** | 7169085212 | Hospital voice alert |
| **Hospital SMS** | 7169085212 | Hospital text details |
| **Nearby People Calls** | 7166170427 | First responder calls (up to 5) |
| **Nearby People SMS** | 7166170427 | First responder texts with instructions (up to 5) |

---

## 🎯 Expected Behavior

### When CRITICAL Emergency is Triggered:

**Phone: 7166170427 will receive:**
1. ✅ **1 SOS Call** - Emergency alert voice message
2. ✅ **1 SOS SMS** - Emergency details with location
3. ✅ **5 Responder Calls** - Nearby people alert calls
4. ✅ **5 Responder SMS** - Instructions on how to help

**Total for 7166170427: 6 calls + 6 SMS = 12 notifications**

**Phone: 7169085212 will receive:**
1. ✅ **1 Hospital Call** - Incoming patient alert
2. ✅ **1 Hospital SMS** - Patient details and ETA

**Total for 7169085212: 1 call + 1 SMS = 2 notifications**

---

## 📞 Call Content

### SOS Call (to 7166170427):
```
"Emergency alert. Medical emergency detected. 
Type: chest pain cardiac. 
Severity: CRITICAL. 
Check your messages for location and details. 
This is incident number 0."
```

### Hospital Call (to 7169085212):
```
"Hospital alert. Incoming patient. 
Emergency type: chest pain cardiac. 
Severity: CRITICAL. 
Estimated time of arrival: 7 minutes. 
Incident number 0. 
Check emergency dispatch system for details."
```

### Responder Calls (to 7166170427, 5 times):
```
"Emergency alert. Medical emergency detected. 
Type: chest pain cardiac. 
Severity: CRITICAL. 
Check your messages for location and details. 
This is incident number 0."
```

---

## 💬 SMS Content

### SOS SMS (to 7166170427):
```
🚨 EMERGENCY ALERT
Type: Chest Pain Cardiac
Severity: CRITICAL
Location: https://www.google.com/maps?q=42.96,-78.73

Emergency services have been notified.
```

### Hospital SMS (to 7169085212):
```
🏥 INCOMING PATIENT
Type: chest pain cardiac
Severity: CRITICAL
ETA: ~7 min
Location: https://www.google.com/maps?q=42.96,-78.73
Incident #0
```

### Responder SMS (to 7166170427, 5 times):
```
🚨 MEDICAL EMERGENCY
Type: Chest Pain Cardiac
Severity: CRITICAL
Location: https://www.google.com/maps?q=42.96,-78.73

HELP NEEDED:
1. Keep person calm and still
2. Loosen tight clothing
3. Help them sit or lie down
4. Give aspirin if available

Ambulance dispatched. Reply ETA if you can help.
```

---

## 🔍 Backend Logs to Expect

```
🚨 CRITICAL EMERGENCY DETECTED: chest_pain_cardiac (CRITICAL)
   Initiating full emergency response...
   📞 Calling SOS contact: 7166170427
   💬 Sending SOS SMS to 7166170427
   🏥 Finding and notifying nearest hospital...
      Hospital: Millard Fillmore Suburban Hospital (calling 7169085212)
   👥 Finding nearby people to alert...
      DEBUG: Found 5 total contacts in database
      DEBUG: John Responder is 68.9m away (radius=500m)
      DEBUG: Jane Helper is 68.9m away (radius=500m)
      DEBUG: Bob Neighbor is 137.8m away (radius=500m)
      DEBUG: Alice Nearby is 137.8m away (radius=500m)
      DEBUG: Mike Close is 206.7m away (radius=500m)
      Found 5 people within 500m
      Alerting: John Responder (68.9m away) at 7166170427
      Alerting: Jane Helper (68.9m away) at 7166170427
      Alerting: Bob Neighbor (137.8m away) at 7166170427
      Alerting: Alice Nearby (137.8m away) at 7166170427
      Alerting: Mike Close (206.7m away) at 7166170427
   ✅ Emergency response initiated successfully

✅ Emergency call initiated to 7166170427: CA...
   ✅ SOS SMS sent: {'success': True, 'message_sid': 'SM...', 'to': '7166170427'}
🏥 Hospital notified (to 7169085212): CA...
✅ Hospital SMS sent (to 7169085212): SM...
      ✅ Called John Responder
      ✅ SMS sent to John Responder: {...}
      ✅ Called Jane Helper
      ✅ SMS sent to Jane Helper: {...}
      ✅ Called Bob Neighbor
      ✅ SMS sent to Bob Neighbor: {...}
      ✅ Called Alice Nearby
      ✅ SMS sent to Alice Nearby: {...}
      ✅ Called Mike Close
      ✅ SMS sent to Mike Close: {...}
```

---

## ✅ Testing Checklist

### Before Testing:
- [ ] Make sure both phones are available:
  - 7166170427 (will get 6 calls + 6 SMS)
  - 7169085212 (will get 1 call + 1 SMS)
- [ ] Verify both numbers are verified in Twilio console
- [ ] Backend server is running on port 8000
- [ ] Frontend server is running on port 5173
- [ ] Database has 5 test contacts with GPS coordinates

### During Testing:
1. [ ] Click SOS button on http://localhost:5173
2. [ ] Say: **"I'm having severe chest pain"**
3. [ ] Watch backend logs for all ✅ success messages
4. [ ] Count calls on 7166170427 (expect 6)
5. [ ] Count SMS on 7166170427 (expect 6)
6. [ ] Count calls on 7169085212 (expect 1)
7. [ ] Count SMS on 7169085212 (expect 1)
8. [ ] Verify frontend shows "Help is on the way" screen

### After Testing:
- [ ] Check Twilio console for all call/SMS records
- [ ] Verify no error messages in backend logs
- [ ] Confirm nearby people debug logs show 5 people found

---

## 🐛 Troubleshooting

### If 7166170427 doesn't receive all calls/SMS:
- **Twilio Rate Limiting**: Multiple rapid calls to same number may be throttled
- **Solution**: Wait 30 seconds between tests
- **Check**: Twilio console for queued/failed messages

### If 7169085212 doesn't receive hospital call/SMS:
- **Not Verified**: Number must be verified in Twilio trial account
- **Solution**: Verify the number at https://console.twilio.com/
- **Check**: Backend logs for error messages

### If nearby people still shows 0:
- **Database Issue**: Contacts not loading properly
- **Solution**: Check DEBUG logs showing contact distances
- **Verify**: Run `python -c "..."` command to check database directly

---

## 📊 Success Metrics

| Metric | Target | How to Verify |
|--------|--------|---------------|
| SOS call to 7166170427 | 1 call | Phone rings once |
| SOS SMS to 7166170427 | 1 text | Check messages |
| Hospital call to 7169085212 | 1 call | Phone rings once |
| Hospital SMS to 7169085212 | 1 text | Check messages |
| Responder calls to 7166170427 | 5 calls | Phone rings 5 times |
| Responder SMS to 7166170427 | 5 texts | Check messages |
| Nearby people found | 5 people | Backend DEBUG logs |
| Frontend UI | "Help is on the way" | Visual check |

**Grand Total: 7 calls + 7 SMS across 2 phone numbers**

---

## 🚀 Ready to Test!

Both phone numbers are now configured. Backend has auto-reloaded. 

**Test it now:**
1. Go to http://localhost:5173
2. Click SOS button
3. Say "I'm having severe chest pain"
4. Watch the magic happen! ✨

---

## 📝 Notes

- **7166170427**: Primary emergency contact + first responders (6 calls + 6 SMS)
- **7169085212**: Hospital notifications only (1 call + 1 SMS)
- **Debug logs**: Now show why contacts are found/not found
- **Twilio Trial**: Both numbers must be verified
- **Rate Limits**: May throttle rapid calls to same number
- **SMS Delivery**: May have slight delay on trial accounts

Backend is running with updated configuration! 🎉
