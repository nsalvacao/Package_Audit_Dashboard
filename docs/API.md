# 📡 API Documentation

## Base URL

```
http://localhost:8000
```

## Interactive Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Endpoints

### 1. Discover Package Managers

Detects installed package managers on the system.

**Endpoint**: `POST /api/discover`

**Request**:
```bash
curl -X POST http://localhost:8000/api/discover
```

**Response** (200 OK):
```json
{
  "managers": [
    {
      "id": "npm",
      "name": "npm",
      "version": "10.2.4"
    },
    {
      "id": "pip",
      "name": "pip",
      "version": "23.3.1"
    }
  ]
}
```

**Empty Response** (no managers found):
```json
{
  "managers": []
}
```

---

### 2. Get Manager Details

Retrieves detailed information about detected package managers.

**Endpoint**: `GET /api/managers`

**Request**:
```bash
curl http://localhost:8000/api/managers
```

**Response** (200 OK):
```json
{
  "managers": [
    {
      "id": "npm",
      "name": "npm",
      "version": "10.2.4",
      "capabilities": {
        "list_packages": true,
        "uninstall": true,
        "audit": false,
        "update": false,
        "export_manifest": true
      }
    }
  ]
}
```

---

### 3. List Packages (Coming in Phase 2)

Lists all packages installed by a specific package manager.

**Endpoint**: `GET /api/managers/{manager_id}/packages`

**Status**: Not yet implemented

---

### 4. Uninstall Package

Uninstalls a package using the specified package manager.

**Endpoint**: `DELETE /api/managers/{manager_id}/packages/{package_name}`

**Query Parameters**:
- `force` (optional): Force uninstall without dependencies check

**Request**:
```bash
curl -X DELETE "http://localhost:8000/api/managers/npm/packages/lodash?force=false"
```

**Response** (200 OK):
```json
{
  "success": true,
  "package": "lodash",
  "manager": "npm",
  "snapshot_id": "snapshot-abc123",
  "operation_time": "2025-11-05T10:30:00Z"
}
```

**Error Response** (400 Bad Request):
```json
{
  "detail": "Invalid package name: pkg; rm -rf /"
}
```

**Error Response** (409 Conflict):
```json
{
  "detail": "Another operation is in progress. Please wait."
}
```

**Error Response** (404 Not Found):
```json
{
  "detail": "Package manager 'invalid' not found"
}
```

---

### 5. Create Snapshot (Coming in Phase 2)

Creates a snapshot of currently installed packages.

**Endpoint**: `POST /api/snapshot`

**Status**: Backend implemented, endpoint not yet exposed

---

### 6. Health Check

Checks if the API is running.

**Endpoint**: `GET /api/health` (To be implemented)

**Response** (200 OK):
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "uptime": 3600
}
```

---

## Error Handling

### Error Response Format

All errors follow this structure:

```json
{
  "detail": "Human-readable error message"
}
```

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Package uninstalled |
| 400 | Bad Request | Invalid package name |
| 404 | Not Found | Manager not found |
| 409 | Conflict | Operation in progress |
| 500 | Server Error | Unexpected error |

---

## Rate Limiting

**Current**: No rate limiting implemented (MVP)

**Planned (Phase 2)**:
- 60 requests per minute per client
- 10 concurrent operations max

---

## Authentication

**Current**: None (local-only application)

**Planned (Phase 3)**:
- Optional API key for remote access
- JWT tokens for multi-user mode

---

## CORS Configuration

**Allowed Origins**:
```python
allow_origins=["http://localhost:5173"]
```

**Note**: Only the frontend at port 5173 can access the API.

---

## WebSocket / SSE Endpoints (Planned Phase 2)

### Real-Time Logs

**Endpoint**: `GET /api/logs/stream`

**Type**: Server-Sent Events (SSE)

**Response Stream**:
```
data: {"level": "info", "message": "Operation started", "timestamp": "2025-11-05T10:30:00Z"}

data: {"level": "info", "message": "Package uninstalled", "timestamp": "2025-11-05T10:30:05Z"}
```

---

## Example Integration

### JavaScript/TypeScript

```typescript
import axios from 'axios'

const API_BASE = 'http://localhost:8000'

// Discover managers
const discoverManagers = async () => {
  const response = await axios.post(`${API_BASE}/api/discover`)
  return response.data.managers
}

// Uninstall package
const uninstallPackage = async (managerId: string, packageName: string) => {
  const response = await axios.delete(
    `${API_BASE}/api/managers/${managerId}/packages/${packageName}`
  )
  return response.data
}
```

### Python

```python
import requests

API_BASE = "http://localhost:8000"

# Discover managers
response = requests.post(f"{API_BASE}/api/discover")
managers = response.json()["managers"]

# Uninstall package
response = requests.delete(
    f"{API_BASE}/api/managers/npm/packages/lodash"
)
result = response.json()
```

### cURL

```bash
# Discover managers
curl -X POST http://localhost:8000/api/discover

# Uninstall package
curl -X DELETE "http://localhost:8000/api/managers/npm/packages/lodash"

# With force flag
curl -X DELETE "http://localhost:8000/api/managers/npm/packages/lodash?force=true"
```

---

## Versioning

**Current**: v0.1.0 (MVP)

**API Versioning Strategy** (Planned Phase 2):
- Endpoints will be versioned: `/api/v1/discover`
- Breaking changes will increment major version
- Backward compatibility maintained for 2 versions

---

**Last Updated**: 2025-11-05
**API Version**: 0.1.0 (MVP)
