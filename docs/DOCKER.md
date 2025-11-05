# 🐳 Docker Deployment Guide

## Overview

This guide explains how to deploy the Package Audit Dashboard using Docker and Docker Compose.

---

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 2GB RAM minimum
- 5GB disk space

---

## Quick Start

### 1. Build and Run with Docker Compose

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

**Access the application:**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 2. Stop and Remove

```bash
# Stop services
docker-compose down

# Remove volumes (WARNING: deletes all data)
docker-compose down -v
```

---

## Development with Docker

### Hot Reload (Development Mode)

For development with hot reload, use volume mounts:

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
    volumes:
      - ./backend/app:/app/app  # Hot reload
    command: uvicorn app.main:app --host 0.0.0.0 --reload

  frontend:
    build:
      context: ./frontend
      target: builder  # Use builder stage
    volumes:
      - ./frontend/src:/app/src  # Hot reload
    command: npm run dev
    ports:
      - "5173:5173"
```

Run with:
```bash
docker-compose -f docker-compose.dev.yml up
```

---

## Production Deployment

### Environment Variables

Create `.env` file:

```bash
# Backend
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO

# Data persistence
DATA_DIR=/data/.package-audit

# CORS (adjust for your domain)
CORS_ORIGINS=http://localhost,https://yourdomain.com
```

### Build for Production

```bash
# Build with no cache
docker-compose build --no-cache

# Run in detached mode
docker-compose up -d

# Check health
docker-compose ps
docker inspect package-audit-backend --format='{{.State.Health.Status}}'
```

### Scaling (if needed in future)

```bash
# Scale backend replicas
docker-compose up -d --scale backend=3
```

---

## Image Details

### Backend Image

**Base:** `python:3.11-slim`
**Size:** ~500MB
**Exposed Port:** 8000

**Security features:**
- Non-root user (`appuser`)
- Read-only file system where possible
- Health checks configured
- Minimal system dependencies

**Build command:**
```bash
cd backend
docker build -t package-audit-backend:latest .
```

### Frontend Image

**Base:** `nginx:alpine`
**Size:** ~50MB
**Exposed Port:** 80

**Features:**
- Multi-stage build (smaller image)
- Gzip compression
- Security headers
- API proxy to backend
- Static asset caching

**Build command:**
```bash
cd frontend
docker build -t package-audit-frontend:latest .
```

---

## Networking

### Internal Network

Services communicate via `package-audit-network`:

- **Backend:** `http://backend:8000`
- **Frontend:** `http://frontend:80`

### Port Mapping

| Service | Container Port | Host Port |
|---------|---------------|-----------|
| Backend | 8000 | 8000 |
| Frontend | 80 | 80 |

---

## Data Persistence

### Volumes

```yaml
volumes:
  backend_data:
    driver: local
```

**Location:** `/var/lib/docker/volumes/package-audit_backend_data/_data`

**Contents:**
- Package snapshots
- Storage data
- Logs

### Backup Data

```bash
# Backup volume
docker run --rm \
  -v package-audit_backend_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup-$(date +%Y%m%d).tar.gz /data

# Restore volume
docker run --rm \
  -v package-audit_backend_data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/backup-20251105.tar.gz -C /
```

---

## Health Checks

### Backend Health Check

```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "phase": "MVP Phase 1"
}
```

### Frontend Health Check

```bash
curl http://localhost/
# Should return 200 OK
```

### Docker Health Status

```bash
# Check backend
docker inspect package-audit-backend --format='{{.State.Health.Status}}'

# Check frontend
docker inspect package-audit-frontend --format='{{.State.Health.Status}}'
```

---

## Logs

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100
```

### Log Rotation

Configure in `docker-compose.yml`:

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs backend

# Check health
docker-compose ps

# Restart service
docker-compose restart backend
```

### Port Already in Use

```bash
# Check what's using port 8000
sudo lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Host:Container
```

### Permission Issues

```bash
# Fix volume permissions
docker-compose down
sudo chown -R 1000:1000 /var/lib/docker/volumes/package-audit_backend_data
docker-compose up -d
```

### Image Build Fails

```bash
# Clean build cache
docker builder prune -a

# Rebuild with no cache
docker-compose build --no-cache
```

---

## Security Best Practices

### 1. Use Secrets (for production)

```yaml
# docker-compose.prod.yml
services:
  backend:
    secrets:
      - api_key
    environment:
      - API_KEY_FILE=/run/secrets/api_key

secrets:
  api_key:
    file: ./secrets/api_key.txt
```

### 2. Limit Resources

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### 3. Network Isolation

```yaml
networks:
  frontend-network:
    driver: bridge
  backend-network:
    driver: bridge
    internal: true  # No external access
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Push Docker Images

on:
  push:
    tags:
      - 'v*'

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build images
        run: docker-compose build

      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker-compose push
```

---

## Alternative Deployments

### Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml package-audit

# Check services
docker stack services package-audit
```

### Kubernetes

See `k8s/` directory for Kubernetes manifests (Phase 3).

---

## Performance Tuning

### Backend Optimization

```dockerfile
# Use uvicorn workers
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--workers", "4"]
```

### Frontend Optimization

```nginx
# Enable caching
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

---

## Monitoring

### Prometheus Metrics (Future)

```yaml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

### Grafana Dashboard (Future)

```yaml
services:
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
```

---

## FAQ

**Q: Can I run without Docker Compose?**
A: Yes, but you'll need to manually manage networking and volumes.

**Q: How do I update the application?**
A:
```bash
git pull
docker-compose build
docker-compose up -d
```

**Q: Where is data stored?**
A: In Docker volume `package-audit_backend_data`

**Q: Can I use this in production?**
A: Yes, but add proper secrets management, monitoring, and backups.

---

**Last Updated**: 2025-11-05
**Docker Compose Version**: 3.8
**Tested On**: Docker 24.0+
