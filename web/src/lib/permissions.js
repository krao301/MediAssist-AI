// Get user's current location
export function getCurrentLocation() {
  return new Promise((resolve, reject) => {
    if (!('geolocation' in navigator)) {
      reject(new Error('Geolocation not supported'));
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        resolve({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        });
      },
      (error) => {
        reject(error);
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 10000,
      }
    );
  });
}

// Request location permission
export async function requestLocationPermission() {
  try {
    await getCurrentLocation();
    return true;
  } catch (error) {
    console.error('Location permission denied or failed:', error);
    return false;
  }
}

// Check if geolocation permission is already granted
export async function isLocationPermissionGranted() {
  if (!navigator.permissions || !navigator.geolocation) {
    return false;
  }
  try {
    const result = await navigator.permissions.query({ name: 'geolocation' });
    return result.state === 'granted';
  } catch {
    return false;
  }
}

// Check if notifications are allowed
export async function isNotificationPermissionGranted() {
  if (!('Notification' in window)) {
    return false;
  }
  return Notification.permission === 'granted';
}

// Request notification permission
export async function requestNotificationPermission() {
  if (!('Notification' in window)) {
    return false;
  }
  if (Notification.permission === 'granted') {
    return true;
  }
  const result = await Notification.requestPermission();
  return result === 'granted';
}

// Check if we can send SMS via server-side integration (placeholder)
export async function canSendSMSAlerts() {
  return true;
}

// Request microphone permission
export async function requestMicrophonePermission() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    stream.getTracks().forEach(track => track.stop());
    return true;
  } catch {
    return false;
  }
}
