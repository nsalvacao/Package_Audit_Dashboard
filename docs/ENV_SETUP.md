# Environment Setup Guide

## Overview

The Package Audit Dashboard uses environment variables to configure the backend server. This guide will help you set up your environment correctly.

## Quick Setup

### 1. Create .env file

```bash
# From the project root
cp .env.example backend/.env
```

### 2. Edit configuration (optional)

The default values in `.env.example` work out of the box for local development. You only need to modify them if:
- You want to change the API port
- You're deploying to production
- You need custom security timeouts
- You want to enable debug mode

## Configuration Reference

### API Configuration

```bash
# Host address (0.0.0.0 allows external connections, 127.0.0.1 for local only)
API_HOST=0.0.0.0

# Port for the API server
API_PORT=8000

# Auto-reload on code changes (set to false in production)
API_RELOAD=true
```

**Production Recommendation:**
- Set `API_RELOAD=false` in production
- Use `API_HOST=0.0.0.0` to allow external connections
- Consider using a reverse proxy (nginx/traefik)

### CORS Configuration

```bash
# Allowed origins for CORS (comma-separated for multiple origins)
CORS_ORIGINS=http://localhost:5173
```

**Examples:**
```bash
# Multiple origins
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,https://yourdomain.com

# Allow all origins (NOT recommended for production)
CORS_ORIGINS=*
```

### Storage Configuration

```bash
# Directory where snapshots and data are stored
DATA_DIR=~/.package-audit

# Maximum number of snapshots to retain per package manager
SNAPSHOT_RETENTION=10
```

**Notes:**
- `DATA_DIR` supports `~` expansion (will resolve to your home directory)
- Snapshots are automatically cleaned up when limit is exceeded
- Increase `SNAPSHOT_RETENTION` if you need more rollback history

### Security Configuration

```bash
# Maximum time (seconds) to wait for a lock
LOCK_TIMEOUT=30

# Time (seconds) before considering a lock stale
STALE_LOCK_TIMEOUT=300

# Maximum time (seconds) for command execution
COMMAND_TIMEOUT=60
```

**Tuning Guidelines:**

| Configuration | Default | Use Case |
|--------------|---------|----------|
| `LOCK_TIMEOUT=30` | Standard | Most environments |
| `LOCK_TIMEOUT=60` | Slow systems | VMs, containers with limited resources |
| `COMMAND_TIMEOUT=60` | Standard | npm, pip operations |
| `COMMAND_TIMEOUT=120` | Large projects | Projects with many dependencies |
| `STALE_LOCK_TIMEOUT=300` | Standard | Prevents deadlocks |

### Logging Configuration

```bash
# Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO
```

**Log Levels:**
- `DEBUG`: Verbose output, includes all operations
- `INFO`: Normal operations (recommended for development)
- `WARNING`: Only warnings and errors
- `ERROR`: Only errors and critical issues
- `CRITICAL`: Only critical failures

**Production Recommendation:** Use `INFO` or `WARNING`

### Development Configuration

```bash
# Enable debug mode (detailed error messages)
DEBUG=false

# Use mock adapters instead of real package managers (for testing)
MOCK_ADAPTERS=false
```

**When to use:**
- `DEBUG=true`: During development to see detailed stack traces
- `MOCK_ADAPTERS=true`: When running tests without package managers installed

⚠️ **NEVER set `DEBUG=true` in production** - exposes sensitive information

## Environment-Specific Configurations

### Local Development

```bash
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
CORS_ORIGINS=http://localhost:5173
LOG_LEVEL=INFO
DEBUG=false
```

### Production

```bash
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=false
CORS_ORIGINS=https://yourdomain.com
LOG_LEVEL=WARNING
DEBUG=false
LOCK_TIMEOUT=60
COMMAND_TIMEOUT=120
```

### Testing

```bash
API_HOST=127.0.0.1
API_PORT=8001
API_RELOAD=false
CORS_ORIGINS=*
LOG_LEVEL=DEBUG
DEBUG=true
MOCK_ADAPTERS=true
```

## Validation

### Check Configuration

Run this command to validate your `.env` file:

```bash
cd backend
python3 -c "
from pydantic_settings import BaseSettings
from pathlib import Path

# This will raise an error if .env is invalid
class Settings(BaseSettings):
    class Config:
        env_file = '.env'

print('✅ .env configuration is valid')
"
```

### Test Backend Startup

```bash
cd backend
source .venv/bin/activate  # If using virtual environment
uvicorn app.main:app --host 0.0.0.0 --port 8000

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## Troubleshooting

### Issue: "Port already in use"

**Solution:** Change `API_PORT` to a different port:
```bash
API_PORT=8001
```

### Issue: "Permission denied" on DATA_DIR

**Solution:** Use a writable directory:
```bash
DATA_DIR=/tmp/package-audit
# or
DATA_DIR=./data
```

### Issue: Frontend can't connect to backend

**Solution:** Check CORS configuration:
```bash
# Make sure frontend URL is allowed
CORS_ORIGINS=http://localhost:5173
```

### Issue: Commands timing out

**Solution:** Increase timeouts:
```bash
COMMAND_TIMEOUT=120  # 2 minutes
LOCK_TIMEOUT=60      # 1 minute
```

## Security Best Practices

1. **Never commit `.env` files** - Already in `.gitignore`
2. **Use environment-specific configs** - Separate dev/staging/prod
3. **Restrict CORS in production** - Never use `*` wildcard
4. **Disable DEBUG in production** - Prevents information leakage
5. **Use strong timeouts** - Prevent resource exhaustion
6. **Limit DATA_DIR permissions** - Only accessible by API user

## Docker/Container Environments

When using Docker, you can pass environment variables directly:

```bash
docker run -e API_HOST=0.0.0.0 -e API_PORT=8000 -e CORS_ORIGINS=* ...
```

Or use a `.env` file:

```bash
docker run --env-file backend/.env ...
```

## Next Steps

After configuring your environment:

1. ✅ Review [SECURITY.md](SECURITY.md) for security guidelines
2. ✅ Check [API.md](API.md) for API documentation
3. ✅ Run tests: `pytest tests/ -v`
4. ✅ Start the backend: `uvicorn app.main:app --reload`
5. ✅ Start the frontend: `cd frontend && npm run dev`

## Support

If you encounter issues:
- Check [Troubleshooting](#troubleshooting) section above
- Review backend logs for error messages
- Open an issue: https://github.com/nsalvacao/Package_Audit_Dashboard/issues
