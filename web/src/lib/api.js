import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;

export const triageEmergency = (text, locale = 'en', ageGroup) => {
  return api.post('/triage', { text, locale, age_group: ageGroup });
};

export const createIncident = (lat, lng) => {
  return api.post('/incidents/', { lat, lng });
};

export const addIncidentEvent = (incidentId, eventDescription) => {
  return api.post(`/incidents/${incidentId}/events`, { 
    event: eventDescription 
  });
};

export const sendAlerts = (incidentId, lat, lng, message) => {
  return api.post(`/incidents/${incidentId}/alerts`, {
    lat,
    lng,
    message
  });
};

export const getNearestHospital = (lat, lng) => {
  return api.get('/nearest-hospital', { params: { lat, lng } });
};

export const resolveIncident = (incidentId) => {
  return api.post(`/incidents/${incidentId}/resolve`);
};

export const getIncidentSummary = (incidentId, format = 'short') => {
  return api.get(`/incidents/${incidentId}/summary`, { params: { format } });
};

export const getContacts = () => {
  return api.get('/contacts/');
};

export const createContact = (name, phone, lat, lng, radiusM = 500) => {
  return api.post('/contacts/', { name, phone, lat, lng, radius_m: radiusM });
};

export const deleteContact = (contactId) => {
  return api.delete(`/contacts/${contactId}`);
};
