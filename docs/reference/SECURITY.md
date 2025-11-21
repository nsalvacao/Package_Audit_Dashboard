# 🔒 Security Documentation

## Overview

The Package Audit Dashboard implements multiple layers of security to protect against common vulnerabilities when executing system commands and managing package managers.

## Security Architecture

### 1. Validation Layer (SEC-001)

**Location**: `backend/app/core/validation.py`

The `ValidationLayer` provides comprehensive input validation to prevent injection attacks:

#### Package Name Validation
- **Whitelist Pattern**: `^[a-zA-Z0-9._@/-]+$`
- **Max Length**: 256 characters
- **Prevents**: Command injection via malicious package names

```python
# ✅ Valid
ValidationLayer.validate_package_name("lodash")
ValidationLayer.validate_package_name("@types/node")

# ❌ Invalid (raises InvalidPackageNameError)
ValidationLayer.validate_package_name("pkg; rm -rf /")
ValidationLayer.validate_package_name("../../../etc/passwd")
```

#### Command Validation
- **Allowed Commands**: Strict whitelist per package manager
- **No Argument Injection**: Commands are built programmatically
- **Prevents**: Arbitrary command execution

```python
# Allowed commands (example for npm)
ALLOWED_COMMANDS = [
    "npm",
    "list", "--json", "--depth=0",
    "uninstall", "--force"
]
```

#### Path Validation
- **Base Directory**: `~/.package-audit/`
- **Path Traversal Prevention**: All paths must be within base directory
- **Canonical Resolution**: Uses `Path.resolve()` to prevent symbolic link exploits

```python
# ✅ Valid
ValidationLayer.validate_path("~/.package-audit/storage/data.json")

# ❌ Invalid (raises PathTraversalError)
ValidationLayer.validate_path("/etc/passwd")
ValidationLayer.validate_path("~/.package-audit/../../../etc/passwd")
```

---

### 2. Lock Manager (SEC-002)

**Location**: `backend/app/core/locking.py`

Prevents race conditions and concurrent modifications:

#### Features
- **Process Locking**: One operation at a time per resource
- **Stale Lock Detection**: Automatic cleanup after 5 minutes
- **Signal Handling**: Cleanup on SIGTERM/SIGINT
- **PID Tracking**: Validates lock ownership

#### Lock File Structure
```json
{
  "pid": 12345,
  "acquired_at": "2025-11-05T10:30:00Z",
  "operation": "uninstall_package"
}
```

#### Timeout Behavior
- **Default Wait**: 30 seconds
- **Stale Detection**: 300 seconds (5 minutes)
- **Force Release**: Available with explicit confirmation

---

### 3. Operation Queue (SEC-003)

**Location**: `backend/app/core/queue.py`

Serializes dangerous operations and allows safe concurrent reads:

#### Operation Types
- **READ**: Multiple concurrent reads allowed
- **MUTATION**: Serialized (one at a time)

#### Examples
```python
# Multiple reads can run concurrently
queue.enqueue(list_packages, OperationType.READ)
queue.enqueue(get_version, OperationType.READ)

# Mutations are serialized
queue.enqueue(uninstall_package, OperationType.MUTATION)  # Waits for lock
```

---

### 4. Command Executor (CORE-001)

**Location**: `backend/app/core/executor.py`

Safe subprocess execution with timeouts and isolation:

#### Features
- **Timeout Protection**: Default 30s, configurable per command
- **No Shell Execution**: Uses list-based arguments (prevents shell injection)
- **Async Support**: Non-blocking execution for long operations
- **Output Capture**: Separate stdout/stderr streams

#### Example
```python
result = CommandExecutor.run(
    ["npm", "list", "--json"],
    timeout=60
)
```

---

## Threat Model

### Protected Against

| Threat | Mitigation | Layer |
|--------|-----------|-------|
| Command Injection | Input validation, no shell=True | ValidationLayer |
| Path Traversal | Base directory enforcement | ValidationLayer |
| Race Conditions | Process locking | LockManager |
| Concurrent Mutations | Operation serialization | OperationQueue |
| Resource Exhaustion | Timeouts, limits | CommandExecutor |
| Privilege Escalation | No sudo, user-level only | System Design |
| Malicious Packages | Pre-operation snapshots | SnapshotManager |

### NOT Protected Against (Out of Scope)

| Threat | Reason | Mitigation |
|--------|--------|-----------|
| Compromised Package Registry | Upstream vulnerability | Use trusted registries |
| System-level Exploits | Requires elevated privileges | Run as non-root user |
| Network MITM | Package manager responsibility | Use HTTPS registries |
| Supply Chain Attacks | Registry-level issue | Verify checksums manually |

---

## Security Best Practices

### For Users

1. **Run as Non-Root**: Never run the dashboard with elevated privileges
2. **Review Operations**: Always check snapshot before uninstall
3. **Secure Backups**: Store snapshots in separate location
4. **Monitor Logs**: Check `~/.package-audit/logs/` regularly

### For Developers

1. **Never Bypass Validation**: Always use `ValidationLayer` before commands
2. **Use Operation Queue**: Wrap mutations in `OperationType.MUTATION`
3. **Set Timeouts**: Configure appropriate timeouts for all commands
4. **Audit Dependencies**: Regularly update `requirements.txt`

---

## Audit Trail

All operations are logged to `~/.package-audit/logs/operations.log`:

```
2025-11-05 10:30:00 [INFO] Operation started: uninstall package "lodash"
2025-11-05 10:30:00 [INFO] Snapshot created: snapshot-abc123
2025-11-05 10:30:05 [INFO] Command executed: npm uninstall lodash
2025-11-05 10:30:05 [INFO] Operation completed successfully
```

---

## Vulnerability Reporting

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email: [your-email@example.com]
3. Include: Steps to reproduce, impact assessment
4. Expected response time: 48 hours

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2025-11-03 | Initial security implementation (SEC-001, SEC-002, SEC-003) |

---

**Last Updated**: 2025-11-05
**Security Level**: MVP (Production-ready for personal use)
