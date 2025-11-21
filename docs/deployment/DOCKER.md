# Docker Setup Guide

## Overview

Package Audit Dashboard can be run using Docker and Docker Compose in two modes:

1. **Standard Mode** (`docker-compose.yml`) - Isolated container environment
2. **Host Access Mode** (`docker-compose.host.yml`) - Container with full host system access ⭐ NEW!

## 🚀 Docker Installation Modes

### Mode 1: Docker with Host Access (⭐ Recommended)

**Perfect for**: Auditing your actual host system from Docker with container isolation

This mode gives you the best of both worlds:
- ✅ Container isolation and easy management
- ✅ Full access to host system packages (npm, pip, brew, winget)
- ✅ Execute commands on host (PowerShell, CMD, bash)
- ✅ Persistent data on host filesystem
- ✅ Invoke CLI tools on host (gemini-cli, claude, codex, etc.)

**Quick Start:**
```bash
# Linux/macOS/WSL
./scripts/install-docker-host.sh

# Windows (PowerShell)
.\scripts\install-docker-host.ps1
```

**See [INSTALLATION.md](INSTALLATION.md) for complete setup guide.**

### Mode 2: Docker Standard (Container Only)

**Perfect for**: Testing, isolated development, learning

- ✅ Complete isolation from host
- ✅ No host system access
- ✅ Only audits packages inside container
- ❌ Cannot audit host system packages

**When to use each mode:**

| Feature | Host Access Mode | Standard Mode |
|---------|-----------------|---------------|
| Audit host packages | ✅ Yes | ❌ No |
| Container isolation | ✅ Yes | ✅ Yes |
| Host command execution | ✅ Yes | ❌ No |
| CLI tools on host | ✅ Yes | ❌ No |
| Windows support | ✅ Full | ⚠️ Limited |
| Security consideration | ⚠️ High trust | ✅ Isolated |

### Choosing the Right Mode

**Use Host Access Mode if you want to:**
- Audit and manage packages on your actual system
- Execute commands on your host OS
- Use CLI tools installed on your host
- Access both Windows and Linux packages (WSL2)

**Use Standard Mode if you want to:**
- Test the application safely
- Learn without affecting your system
- Develop in complete isolation
- Don't need host package management

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

**Installation:**
- Linux: https://docs.docker.com/engine/install/
- macOS: Docker Desktop
- Windows: Docker Desktop with WSL2

## Quick Start

### Host Access Mode (Recommended)

```bash
# Clone the repository
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard

# Linux/macOS/WSL: Run installation script
./scripts/install-docker-host.sh

# Windows: Run PowerShell script
.\scripts\install-docker-host.ps1

# Or manually start with host access
docker-compose -f docker-compose.host.yml up -d
```

### Standard Mode (Container Only)

```bash
# Clone the repository
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard

# Start all services
docker-compose up -d
```

**Services will be available at:**
- Frontend Dashboard: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Stop Services

**Standard Mode:**
```bash
# Stop services (keep data)
docker-compose stop

# Stop and remove containers (keep data)
docker-compose down

# Stop, remove containers, and delete data
docker-compose down -v
```

**Host Access Mode:**
```bash
# Stop services (keep data)
docker-compose -f docker-compose.host.yml stop

# Stop and remove containers (keep data)
docker-compose -f docker-compose.host.yml down

# Stop, remove containers, and delete data
docker-compose -f docker-compose.host.yml down -v
```

---

## Host Access Features

When using `docker-compose.host.yml`, the following features are enabled:

### 1. Host Package Manager Access

The container can interact with package managers installed on your host:

```bash
# From container, these access HOST packages
docker-compose -f docker-compose.host.yml exec backend bash
$ npm list -g         # Lists host npm packages
$ pip list            # Lists host pip packages
$ brew list           # Lists host brew packages (macOS/Linux)
```

### 2. Host Command Execution

Execute commands on your host system from the container:

```python
# Via API
POST /api/v1/host/execute
{
  "command": ["npm", "list", "-g"],
  "shell": "bash"
}
```

### 3. CLI Tool Integration

Invoke AI coding assistants and other CLI tools on your host:

```bash
# If gemini-cli is installed on host
POST /api/v1/host/cli-tool
{
  "tool": "gemini-cli",
  "args": ["analyze", "code.py"]
}

# Supported tools (if installed):
# - gemini-cli
# - claude (Anthropic CLI)
# - codex (OpenAI Codex)
# - aider
# - cursor
# - Any custom CLI tool
```

### 4. Windows PowerShell/CMD Support

Execute Windows commands from the container:

```python
# PowerShell
POST /api/v1/host/execute
{
  "command": "Get-Package | Where-Object {$_.Name -like '*node*'}",
  "shell": "powershell"
}

# CMD
POST /api/v1/host/execute
{
  "command": "dir C:\\Windows\\System32",
  "shell": "cmd"
}
```

### 5. WSL2 Interoperability

On WSL2, access both Windows and Linux:

```bash
# Linux packages
docker-compose -f docker-compose.host.yml exec backend bash
$ apt list --installed

# Windows packages (via WSL interop)
$ /mnt/c/Windows/System32/cmd.exe /c winget list
```

### 6. Persistent Data Storage

Data is stored on the host filesystem:

```bash
# Default location: ./data
# Configured in .env: HOST_DATA_DIR=./data

# Access data from host
ls -la ./data/

# Snapshots stored here
ls -la ./data/snapshots/
```

### Security Considerations

⚠️ **Important**: Host access mode requires careful security considerations:

1. **Review `.env.host` configuration** before enabling
2. **Only enable privileged mode if absolutely necessary**
3. **Monitor logs regularly** for suspicious activity
4. **Limit volume mounts** to only necessary directories
5. **Use non-root user** in container (configured in Dockerfile.host)
6. **Audit command execution** with proper logging

See [SECURITY.md](SECURITY.md) for complete security guidelines.

---

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
