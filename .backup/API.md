# API Documentation

Base URL: `http://localhost:8000` (development)

## Authentication

Most endpoints require Auth0 JWT token in header:
```
Authorization: Bearer <jwt_token>
```

For development, demo mode accepts any user without auth.

---

## Endpoints

### Health Check

**GET** `/health`

Returns API health status.

**Response**:
```json
{
  "status": "healthy"
}
```

---

### Triage

**POST** `/triage`

Classifies emergency and generates first-aid plan.

**Request**:
```json
{
  "text": "Person not breathing, unconscious",
  "locale": "en-US",
  "age_group": "adult"
}
```

**Parameters**:
- `text` (string, required): Emergency description
- `locale` (string, optional): Language code (default: "en-US")
- `age_group` (string, optional): "infant", "child", "adult", "elderly" (default: "adult")

**Response**:
```json
{
  "type": "cardiac_arrest",
  "severity": "critical",
  "steps": [
    {
      "num": 1,
      "title": "Check Responsiveness",
      "description": "Tap shoulders and shout 'Are you okay?'",
      "time_estimate_sec": 10,
      "cadence_bpm": null
    },
    {
      "num": 2,
      "title": "Call 911",
      "description": "Call emergency services immediately. State your location clearly.",
      "time_estimate_sec": 30,
      "cadence_bpm": null
    },
    {
      "num": 3,
      "title": "Start CPR",
      "description": "Place hands center of chest. Push hard and fast. 30 compressions, then 2 breaths.",
      "time_estimate_sec": 0,
      "cadence_bpm": 110
    }
  ],
  "bring": ["AED (if available)", "Warm blanket"],
  "next_actions": ["Continue CPR until help arrives"]
}
```

**Status Codes**:
- 200: Success
- 400: Invalid request (missing text)
- 500: AI service error (falls back to keyword matching)

---

### Alerts

**POST** `/alerts`

Sends SMS/voice alerts to contacts within radius.

**Request**:
```json
{
  "user_id": 1,
  "incident_id": 123,
  "latitude": 42.9634,
  "longitude": -78.7384
}
```

**Parameters**:
- `user_id` (int, required): User ID
- `incident_id` (int, required): Active incident ID
- `latitude` (float, required): User's current latitude
- `longitude` (float, required): User's current longitude

**Response**:
```json
{
  "sent": 2,
  "contacts": [
    {
      "id": 1,
      "name": "John Doe",
      "phone": "+1234567890",
      "distance_meters": 234
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "phone": "+1098765432",
      "distance_meters": 456
    }
  ]
}
```

**Status Codes**:
- 200: Success
- 400: Invalid coordinates
- 404: User or incident not found
- 500: Twilio API error

**Notes**:
- Only contacts within 500m receive alerts
- SMS template: "EMERGENCY ALERT: [Name] needs help at [Location]. View: [Link]"
- Voice call plays pre-recorded message

---

### Hospital Routing

**POST** `/route`

Finds nearest hospital with directions.

**Request**:
```json
{
  "latitude": 42.9634,
  "longitude": -78.7384
}
```

**Response**:
```json
{
  "hospital": {
    "name": "Buffalo General Medical Center",
    "address": "100 High St, Buffalo, NY 14203",
    "phone": "+17168598600",
    "distance_km": 2.3,
    "duration_minutes": 5
  },
  "directions_url": "https://maps.google.com/maps?saddr=42.9634,-78.7384&daddr=42.9850,-78.7450"
}
```

**Status Codes**:
- 200: Success
- 400: Invalid coordinates
- 404: No hospitals found within 50km
- 500: Maps API error

---

### Incidents

#### Create Incident

**POST** `/incidents`

Creates new emergency incident.

**Request**:
```json
{
  "user_id": 1,
  "latitude": 42.9634,
  "longitude": -78.7384,
  "emergency_type": "cardiac_arrest",
  "severity": "critical"
}
```

**Response**:
```json
{
  "id": 123,
  "user_id": 1,
  "status": "active",
  "emergency_type": "cardiac_arrest",
  "severity": "critical",
  "latitude": 42.9634,
  "longitude": -78.7384,
  "created_at": "2025-01-15T10:30:00Z"
}
```

#### Get Incident

**GET** `/incidents/{incident_id}`

Retrieves incident details.

**Response**:
```json
{
  "id": 123,
  "user_id": 1,
  "status": "active",
  "emergency_type": "cardiac_arrest",
  "severity": "critical",
  "latitude": 42.9634,
  "longitude": -78.7384,
  "created_at": "2025-01-15T10:30:00Z",
  "resolved_at": null,
  "events": [
    {
      "id": 1,
      "incident_id": 123,
      "event_type": "start",
      "detail": "Emergency reported: cardiac arrest",
      "timestamp": "2025-01-15T10:30:00Z"
    }
  ]
}
```

#### Add Event

**POST** `/incidents/{incident_id}/events`

Logs event to incident timeline.

**Request**:
```json
{
  "event_type": "step_completed",
  "detail": "CPR initiated at 120 bpm"
}
```

**Response**:
```json
{
  "id": 2,
  "incident_id": 123,
  "event_type": "step_completed",
  "detail": "CPR initiated at 120 bpm",
  "timestamp": "2025-01-15T10:31:00Z"
}
```

**Event Types**:
- `start`: Incident created
- `triage`: AI classification
- `alert_sent`: Contacts notified
- `step_completed`: User completed step
- `resolved`: Incident ended

#### Resolve Incident

**POST** `/incidents/{incident_id}/resolve`

Ends active incident.

**Response**:
```json
{
  "id": 123,
  "status": "resolved",
  "resolved_at": "2025-01-15T10:38:30Z",
  "duration_seconds": 510
}
```

#### Get Summary

**GET** `/incidents/{incident_id}/summary?format=json`

Generates incident report.

**Parameters**:
- `format` (string, optional): "json" or "text" (default: "json")

**Response (JSON)**:
```json
{
  "incident": {
    "id": 123,
    "type": "cardiac_arrest",
    "severity": "critical",
    "duration_seconds": 510,
    "created_at": "2025-01-15T10:30:00Z",
    "resolved_at": "2025-01-15T10:38:30Z"
  },
  "timeline": [
    {
      "elapsed_seconds": 0,
      "event": "Emergency reported: cardiac arrest"
    },
    {
      "elapsed_seconds": 30,
      "event": "AI triage: cardiac_arrest - critical"
    },
    {
      "elapsed_seconds": 45,
      "event": "Contacts notified: 2 within 500m"
    },
    {
      "elapsed_seconds": 75,
      "event": "CPR initiated at 120 bpm"
    },
    {
      "elapsed_seconds": 510,
      "event": "Incident resolved by user"
    }
  ]
}
```

**Response (Text)**:
```
EMERGENCY INCIDENT REPORT
=========================
Incident ID: 123
Type: Cardiac Arrest
Severity: Critical
Duration: 8min 30s
Start: 2025-01-15 10:30:00
End: 2025-01-15 10:38:30

TIMELINE
--------
+00:00 - Emergency reported: cardiac arrest
+00:30 - AI triage: cardiac_arrest - critical
+00:45 - Contacts notified: 2 within 500m
+01:15 - CPR initiated at 120 bpm
+08:30 - Incident resolved by user
```

---

### Contacts

#### List Contacts

**GET** `/contacts?user_id={user_id}`

Retrieves user's trusted contacts.

**Response**:
```json
[
  {
    "id": 1,
    "user_id": 1,
    "name": "John Doe",
    "phone": "+1234567890",
    "address": "123 Main St, Buffalo, NY",
    "latitude": 42.9650,
    "longitude": -78.7380
  }
]
```

#### Create Contact

**POST** `/contacts`

Adds new trusted contact.

**Request**:
```json
{
  "user_id": 1,
  "name": "John Doe",
  "phone": "+1234567890",
  "address": "123 Main St, Buffalo, NY"
}
```

**Response**:
```json
{
  "id": 1,
  "user_id": 1,
  "name": "John Doe",
  "phone": "+1234567890",
  "address": "123 Main St, Buffalo, NY",
  "latitude": 42.9650,
  "longitude": -78.7380
}
```

**Notes**:
- Address is geocoded to lat/lng using Maps API
- Phone must be E.164 format (+1XXXXXXXXXX)

#### Delete Contact

**DELETE** `/contacts/{contact_id}`

Removes contact.

**Response**:
```json
{
  "deleted": true
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common Status Codes**:
- 400: Bad Request (invalid parameters)
- 401: Unauthorized (missing/invalid JWT)
- 404: Not Found (resource doesn't exist)
- 500: Internal Server Error (server issue)

---

## Rate Limits

- Triage: 60 requests/minute per user
- Alerts: 10 requests/minute per user
- Other endpoints: 100 requests/minute per user

Exceeded limits return 429 Too Many Requests.

---

## Webhooks (Optional)

Configure webhook URL to receive incident updates:

**POST** `{your_webhook_url}`

Payload:
```json
{
  "event": "incident.resolved",
  "incident_id": 123,
  "timestamp": "2025-01-15T10:38:30Z",
  "data": { ... }
}
```

Events:
- `incident.created`
- `incident.resolved`
- `alert.sent`

---

## SDK Examples

### Python
```python
import requests

API_BASE = "http://localhost:8000"

# Triage
response = requests.post(f"{API_BASE}/triage", json={
    "text": "Person choking on food",
    "age_group": "adult"
})
result = response.json()
print(result["type"])  # "choking"

# Create incident
incident = requests.post(f"{API_BASE}/incidents", json={
    "user_id": 1,
    "latitude": 42.9634,
    "longitude": -78.7384,
    "emergency_type": result["type"],
    "severity": result["severity"]
}).json()

# Send alerts
alerts = requests.post(f"{API_BASE}/alerts", json={
    "user_id": 1,
    "incident_id": incident["id"],
    "latitude": 42.9634,
    "longitude": -78.7384
}).json()
print(f"Alerted {alerts['sent']} contacts")
```

### JavaScript
```javascript
const API_BASE = 'http://localhost:8000';

// Triage
const triageResponse = await fetch(`${API_BASE}/triage`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'Person choking on food',
    age_group: 'adult'
  })
});
const result = await triageResponse.json();
console.log(result.type);  // "choking"

// Create incident
const incident = await fetch(`${API_BASE}/incidents`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: 1,
    latitude: 42.9634,
    longitude: -78.7384,
    emergency_type: result.type,
    severity: result.severity
  })
}).then(r => r.json());

// Send alerts
const alerts = await fetch(`${API_BASE}/alerts`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: 1,
    incident_id: incident.id,
    latitude: 42.9634,
    longitude: -78.7384
  })
}).then(r => r.json());
console.log(`Alerted ${alerts.sent} contacts`);
```
