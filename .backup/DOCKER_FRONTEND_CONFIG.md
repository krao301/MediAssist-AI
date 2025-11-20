# 🌐 Frontend Configuration for Docker

## Current Setup

Your frontend is configured to connect to the API. When running in Docker, ensure the API URL is correct.

---

## Environment Variables

Create `web/.env.production`:

```env
VITE_API_URL=http://localhost:8000
```

Or if deploying to cloud:

```env
VITE_API_URL=https://api.yourdomain.com
```

---

## Vite Configuration

Your `web/vite.config.ts` should have:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',  // Allow external connections (Docker)
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://api:8000',  // Use Docker service name
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
```

---

## API Client Configuration

Check your `web/src/lib/api.ts`:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

---

## Docker Networking

When services run in Docker:

- **Frontend → API (internal):** `http://api:8000`
- **Browser → API (external):** `http://localhost:8000`
- **Frontend → API (browser request):** `http://localhost:8000`

Since browser makes requests (not the container), use `localhost:8000` for API calls.

---

## Testing

```bash
# Start services
./docker-start.sh

# Check frontend can reach API
curl http://localhost:3000
curl http://localhost:8000/health

# Open browser
open http://localhost:3000
```

---

## Production Deployment

For production (e.g., on a server):

1. **Update API URL:**
   ```env
   VITE_API_URL=https://api.yourdomain.com
   ```

2. **Rebuild frontend:**
   ```bash
   docker-compose -f infra/docker-compose.improved.yml build web
   ```

3. **Deploy:**
   ```bash
   docker-compose -f infra/docker-compose.improved.yml up -d
   ```

---

## Troubleshooting

**Issue: Frontend shows "Network Error"**

```bash
# Check if API is running
curl http://localhost:8000/health

# Check frontend console for API URL
# Should be http://localhost:8000
```

**Issue: CORS errors**

Check `api/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: ["https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

Your current setup should work fine! If you see any API connection issues, check these configurations.
