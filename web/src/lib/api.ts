import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;

// API functions
export const triageEmergency = (
  text: string,
  locale = 'en',
  ageGroup?: string,
  latitude?: number,
  longitude?: number
) => {
  return api.post('/triage', {
    text,
    locale,
    age_group: ageGroup,
    latitude,
    longitude
  });
};

export const sendAlerts = (incidentId: number, lat: number, lng: number, message: string, radiusM = 500) => {
  return api.post('/alerts', { incident_id: incidentId, lat, lng, message, radius_m: radiusM });
};

export const getNearestHospital = (lat: number, lng: number) => {
  return api.post('/route', { lat, lng });
};

export const createIncident = (lat: number, lng: number, type?: string, severity?: string) => {
  return api.post('/incidents/create', { lat, lng, type, severity });
};

export const addIncidentEvent = (incidentId: number, step: string, metadata?: any) => {
  return api.post(`/incidents/${incidentId}/event`, { step, metadata });
};

export const resolveIncident = (incidentId: number) => {
  return api.post(`/incidents/${incidentId}/resolve`);
};

export const getIncidentSummary = (incidentId: number, format = 'json') => {
  return api.get(`/incidents/${incidentId}/summary`, { params: { format } });
};

export const getContacts = () => {
  return api.get('/contacts/');
};

export const createContact = (name: string, phone: string, lat: number, lng: number, radiusM = 500) => {
  return api.post('/contacts/', { name, phone, lat, lng, radius_m: radiusM });
};

export const deleteContact = (contactId: number) => {
  return api.delete(`/contacts/${contactId}`);
};
