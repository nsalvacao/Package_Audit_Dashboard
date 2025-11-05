# Docker Setup Guide

## Overview

Package Audit Dashboard can be run using Docker and Docker Compose for simplified development and deployment.

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

**Installation:**
- Linux: https://docs.docker.com/engine/install/
- macOS: Docker Desktop
- Windows: Docker Desktop with WSL2

## Quick Start

### Development Mode (Recommended)

```bash
# Clone the repository
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard

# Start all services
docker-compose up

# Or run in background
docker-compose up -d
```

**Services will be available at:**
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Frontend Dashboard: http://localhost:5173
- Health Check: http://localhost:8000/health

### Stop Services

```bash
# Stop services (keep data)
docker-compose stop

# Stop and remove containers (keep data)
docker-compose down

# Stop, remove containers, and delete data
docker-compose down -v
```

## Docker Compose Configuration

### Default Configuration

The `docker-compose.yml` includes:
- **Backend**: Python 3.11 with FastAPI
- **Frontend**: Node 18 with Vite
- **Networking**: Bridge network for service communication
- **Volumes**: Persistent storage for snapshots

### Environment Variables

Override defaults by creating a `.env` file in the project root:

```bash
# Backend Configuration
API_PORT=8000
LOG_LEVEL=INFO
DEBUG=false

# Frontend Configuration
VITE_API_URL=http://localhost:8000
```

### Volume Mounts

**Development:**
- `./backend:/app` - Hot-reload backend changes
- `./frontend:/app` - Hot-reload frontend changes
- `package-audit-data:/app/data` - Persistent storage

**Production:**
- Remove code mounts for security
- Keep data volume for persistence

## Building Images

### Build All Services

```bash
docker-compose build
```

### Build Specific Service

```bash
docker-compose build backend
docker-compose build frontend
```

### Rebuild Without Cache

```bash
docker-compose build --no-cache
```

## Running Commands

### Backend Commands

```bash
# Run tests
docker-compose exec backend pytest tests/ -v

# Access Python shell
docker-compose exec backend python

# Install additional packages
docker-compose exec backend pip install package-name

# View logs
docker-compose logs backend
docker-compose logs -f backend  # Follow logs
```

### Frontend Commands

```bash
# Run linter
docker-compose exec frontend npm run lint

# Build production bundle
docker-compose exec frontend npm run build

# View logs
docker-compose logs frontend
docker-compose logs -f frontend  # Follow logs
```

### Database/Storage Commands

```bash
# View data volume contents
docker-compose exec backend ls -la /app/data

# Backup data
docker run --rm -v package-audit-data:/data -v $(pwd):/backup alpine tar czf /backup/data-backup.tar.gz -C /data .

# Restore data
docker run --rm -v package-audit-data:/data -v $(pwd):/backup alpine tar xzf /backup/data-backup.tar.gz -C /data
```

## Production Deployment

### Using Docker Compose

```bash
# Create production docker-compose
cp docker-compose.yml docker-compose.prod.yml
```

Edit `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - API_RELOAD=false
      - LOG_LEVEL=WARNING
      - DEBUG=false
      - CORS_ORIGINS=https://yourdomain.com
    volumes:
      - package-audit-data:/app/data
    # Remove code mounts for security
    restart: always

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    ports:
      - "80:80"
    restart: always
```

Run production:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Environment-Specific Configs

**Staging:**
```bash
docker-compose -f docker-compose.staging.yml up -d
```

**Testing:**
```bash
docker-compose -f docker-compose.test.yml up -d
```

## Advanced Configuration

### Custom Network

```yaml
networks:
  package-audit-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

### Resource Limits

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### Health Checks

Backend includes automatic health checks:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

Check health status:
```bash
docker-compose ps
```

## Troubleshooting

### Port Already in Use

```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead of 8000
```

### Container Won't Start

```bash
# Check logs
docker-compose logs backend

# Check container status
docker-compose ps

# Restart specific service
docker-compose restart backend
```

### Permission Issues

```bash
# Fix data directory permissions
docker-compose exec backend chown -R $(id -u):$(id -g) /app/data
```

### Network Issues

```bash
# Recreate network
docker-compose down
docker network prune
docker-compose up
```

### Database/Storage Issues

```bash
# Check volume
docker volume inspect package-audit-data

# Remove and recreate volume (WARNING: deletes data)
docker-compose down -v
docker-compose up
```

### Build Fails

```bash
# Clean build
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## Performance Optimization

### Use BuildKit

```bash
# Enable BuildKit for faster builds
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1
docker-compose build
```

### Multi-Stage Builds

For production, use multi-stage builds in Dockerfile:

```dockerfile
# Build stage
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Layer Caching

Order Dockerfile commands for optimal caching:
1. Install system dependencies (rarely changes)
2. Copy package files (changes occasionally)
3. Install packages (changes occasionally)
4. Copy application code (changes frequently)

## Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Resource Usage

```bash
# View container stats
docker stats

# Specific container
docker stats package-audit-backend
```

### Inspect Containers

```bash
# Container details
docker inspect package-audit-backend

# Network details
docker network inspect package-audit_package-audit-network
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Docker Build

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build images
        run: docker-compose build
      - name: Run tests
        run: docker-compose run backend pytest tests/ -v
```

### GitLab CI

```yaml
stages:
  - build
  - test

docker-build:
  stage: build
  script:
    - docker-compose build

docker-test:
  stage: test
  script:
    - docker-compose up -d
    - docker-compose exec -T backend pytest tests/ -v
    - docker-compose down
```

## Security Best Practices

1. **Don't run as root**
   ```dockerfile
   RUN useradd -m -u 1000 appuser
   USER appuser
   ```

2. **Use specific versions**
   ```dockerfile
   FROM python:3.11.7-slim  # Not just :3.11
   ```

3. **Scan images**
   ```bash
   docker scan package-audit-backend
   ```

4. **Limit capabilities**
   ```yaml
   security_opt:
     - no-new-privileges:true
   ```

5. **Use secrets**
   ```yaml
   secrets:
     - db_password
   ```

## Next Steps

- Review [ENV_SETUP.md](ENV_SETUP.md) for environment configuration
- Check [SECURITY.md](SECURITY.md) for security guidelines
- See [API.md](API.md) for API documentation

## Support

- Docker Documentation: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- Issues: https://github.com/nsalvacao/Package_Audit_Dashboard/issues
