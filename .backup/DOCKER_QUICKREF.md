# 🐳 Docker Quick Reference

## 🚀 Start Services

```bash
./docker-start.sh
```

**Opens:**
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Grafana: http://localhost:3001
- Prometheus: http://localhost:9090

---

## 🛑 Stop Services

```bash
./docker-stop.sh
```

---

## 🔧 Development Mode (Hot-Reload)

```bash
./docker-dev.sh
```

Press `Ctrl+C` to stop.

---

## 📊 View Logs

```bash
# All services
docker-compose -f infra/docker-compose.improved.yml logs -f

# Specific service
docker-compose -f infra/docker-compose.improved.yml logs -f api
docker-compose -f infra/docker-compose.improved.yml logs -f web
```

---

## ✅ Health Checks

```bash
# API health
curl http://localhost:8000/health

# Check all services status
docker-compose -f infra/docker-compose.improved.yml ps

# Check Redis
docker-compose -f infra/docker-compose.improved.yml exec redis redis-cli ping
```

---

## 🔄 Restart Services

```bash
# Restart all
./docker-stop.sh && ./docker-start.sh

# Restart specific service
docker-compose -f infra/docker-compose.improved.yml restart api
```

---

## 🧹 Clean Everything

```bash
# Stop and remove containers
docker-compose -f infra/docker-compose.improved.yml down

# Remove volumes too (WARNING: deletes data)
docker-compose -f infra/docker-compose.improved.yml down -v

# Clean unused Docker resources
docker system prune -a
```

---

## 🐛 Debugging

```bash
# Access container shell
docker-compose -f infra/docker-compose.improved.yml exec api bash
docker-compose -f infra/docker-compose.improved.yml exec web sh

# View resource usage
docker stats

# Rebuild without cache
docker-compose -f infra/docker-compose.improved.yml build --no-cache api
```

---

## 📁 Important Files

- **`api/.env.docker`** - Environment variables (API keys, DB URL)
- **`infra/docker-compose.improved.yml`** - Production config
- **`infra/docker-compose.dev.yml`** - Development config
- **`DOCKER_README.md`** - Full documentation
- **`DOCKER_SETUP_SUMMARY.md`** - Complete setup guide

---

## 🆘 Emergency Commands

```bash
# Quick restart
./docker-stop.sh && ./docker-start.sh

# Check what's broken
docker-compose -f infra/docker-compose.improved.yml ps
docker-compose -f infra/docker-compose.improved.yml logs --tail=50

# Nuclear option
docker-compose -f infra/docker-compose.improved.yml down -v
docker system prune -a
./docker-start.sh
```

---

## 🎯 Pre-Demo Checklist

```bash
# 1. Start services
./docker-start.sh

# 2. Check health
curl http://localhost:8000/health

# 3. Open frontend
open http://localhost:3000

# 4. Test emergency flow
# - CRITICAL: "chest pain"
# - MINOR: "small cut"

# 5. Check monitoring
open http://localhost:3001  # Grafana (admin/admin)
```

---

## 📞 Common Issues

**Port already in use:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Cannot connect to API:**
```bash
docker-compose -f infra/docker-compose.improved.yml logs api
```

**Database connection failed:**
```bash
# Check .env.docker has correct DB_URL
cat api/.env.docker | grep DB_URL
```

**Redis not working:**
```bash
docker-compose -f infra/docker-compose.improved.yml restart redis
```

---

**For full documentation, see `DOCKER_README.md`**
