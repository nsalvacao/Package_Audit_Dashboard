# Docker Host Access Feature

## Overview

This document describes the new **Docker Host Access** feature that allows the containerized Package Audit Dashboard to access and manage packages on your host system while maintaining container isolation.

## What's New

Previously, Docker installation could only audit packages **inside the container**. Now, with Docker Host Access mode, you can:

✅ **Audit host system packages** (npm, pip, brew, winget)  
✅ **Execute commands on host** (bash, PowerShell, CMD)  
✅ **Invoke CLI tools on host** (gemini-cli, claude, codex, etc.)  
✅ **Persistent data on host** filesystem  
✅ **Full Windows/macOS/Linux/WSL2 support**  

## Architecture

### Standard Docker Mode (Container Only)
```
┌─────────────────────────┐
│   Docker Container      │
│                         │
│  ┌──────────────────┐   │
│  │ Package Manager  │   │ ← Only sees container packages
│  │   (npm, pip)     │   │
│  └──────────────────┘   │
│                         │
└─────────────────────────┘
```

### Docker Host Access Mode
```
┌─────────────────────────┐
│   Docker Container      │
│                         │
│  ┌──────────────────┐   │
│  │ Host Executor    │───┼──→ Execute commands on host
│  └──────────────────┘   │
│           ↓             │
│  ┌──────────────────┐   │
│  │ Volume Mounts    │───┼──→ Access host filesystem
│  └──────────────────┘   │
│           ↓             │
│  ┌──────────────────┐   │
│  │ Docker Socket    │───┼──→ Create containers on host
│  └──────────────────┘   │
│                         │
└─────────────────────────┘
           ↓
    ┌──────────────┐
    │  Host System │
    │              │
    │  npm, pip,   │ ← Full access to host packages
    │  brew, winget│
    │              │
    │  gemini-cli, │ ← Can invoke host CLI tools
    │  claude, etc │
    └──────────────┘
```

## Components

### 1. Enhanced Docker Compose (`docker-compose.host.yml`)

Key features:
- Volume mounts for host filesystem access
- Docker socket access for host command execution
- Environment variables for host configuration
- Optional privileged mode for advanced operations

### 2. Host-Enabled Dockerfile (`backend/Dockerfile.host`)

Additions to standard Dockerfile:
- SSH client for remote execution
- Docker CLI for container-based execution
- PowerShell Core for Windows interop
- Python packages for host interaction (paramiko, docker, psutil)

### 3. Host Command Executor (`backend/app/core/host_executor.py`)

Python module providing:
- Three execution modes: Docker socket, SSH, Direct
- PowerShell and CMD execution for Windows
- CLI tool invocation framework
- Security validation and logging

### 4. Configuration Template (`.env.host`)

Environment variables for:
- Host access settings
- Execution mode selection
- Windows/WSL2 specific paths
- CLI tool configuration
- Security options

### 5. Installation Scripts

Automated setup:
- `scripts/install-docker-host.sh` - Bash script for Linux/macOS/WSL
- `scripts/install-docker-host.ps1` - PowerShell script for Windows

### 6. Comprehensive Documentation

New documentation:
- `docs/INSTALLATION.md` - Complete installation guide (16KB)
- `docs/USAGE.md` - Comprehensive usage instructions (18KB)
- Updated `docs/DOCKER.md` - Docker-specific details
- Updated `README.md` - Quick start and links

## How It Works

### Execution Modes

#### 1. Docker Socket Mode (Default)
```python
# Executes commands by spawning containers on host
docker run --rm --network=host -v /:/host alpine sh -c "npm list -g"
```

**Pros:**
- Works on all platforms
- No SSH configuration needed
- Good isolation

**Cons:**
- Requires Docker socket access
- Slight overhead from container creation

#### 2. SSH Mode
```python
# Executes commands via SSH to host
ssh user@host.docker.internal "npm list -g"
```

**Pros:**
- More direct execution
- Works with remote hosts
- Standard protocol

**Cons:**
- Requires SSH server on host
- Need SSH keys configured
- More complex setup

#### 3. Direct Mode
```python
# Direct execution (when running natively, not in Docker)
subprocess.run(["npm", "list", "-g"])
```

**Pros:**
- Fastest execution
- No overhead

**Cons:**
- Only works when running natively
- Not applicable for Docker mode

## Security Model

### Multi-Layer Security

1. **Environment-based enablement**
   ```bash
   ENABLE_HOST_ACCESS=true  # Must be explicitly enabled
   ```

2. **Execution mode selection**
   ```bash
   HOST_EXECUTION_MODE=docker  # Controlled execution method
   ```

3. **Privileged mode (optional)**
   ```bash
   DOCKER_PRIVILEGED=false  # Default is non-privileged
   ```

4. **Volume mount restrictions**
   - Only specific directories mounted
   - Read-only mounts where possible
   - No root filesystem write access by default

5. **Non-root container user**
   ```dockerfile
   USER appuser  # Runs as non-root user
   ```

6. **Command validation**
   - Input validation before execution
   - Whitelist of allowed commands
   - Logging of all executions

### Security Considerations

⚠️ **Host access is powerful and requires trust:**

1. **Review `.env.host` carefully** before deployment
2. **Only enable privileged mode if absolutely necessary**
3. **Monitor logs** for suspicious activity
4. **Limit volume mounts** to necessary directories only
5. **Use non-root user** (already configured)
6. **Audit command executions** regularly
7. **Keep Docker and tools updated**
8. **Implement network policies** if using in production

## Usage Examples

### Example 1: List Host NPM Packages

```bash
# Start with host access
docker-compose -f docker-compose.host.yml up -d

# Access backend container
docker-compose -f docker-compose.host.yml exec backend bash

# List host npm packages
curl http://localhost:8000/api/v1/managers/npm/packages
```

### Example 2: Execute PowerShell on Windows Host

```python
# Via API
POST http://localhost:8000/api/v1/host/execute
Content-Type: application/json

{
  "command": "Get-Package",
  "shell": "powershell"
}
```

### Example 3: Invoke Gemini CLI on Host

```python
# Via API
POST http://localhost:8000/api/v1/host/cli-tool
Content-Type: application/json

{
  "tool": "gemini-cli",
  "args": ["analyze", "--file", "code.py"]
}
```

### Example 4: WSL2 Dual Access

```bash
# Access Linux packages
curl http://localhost:8000/api/v1/managers/pip/packages

# Access Windows packages (via PowerShell)
POST http://localhost:8000/api/v1/host/execute
{
  "command": "winget list",
  "shell": "powershell"
}
```

## Platform Support

| Platform | Support Level | Notes |
|----------|--------------|-------|
| **Linux** | ✅ Full | Host networking available, best performance |
| **macOS** | ✅ Full | Bridge networking only, Docker Desktop required |
| **Windows** | ✅ Full | PowerShell/CMD support, Docker Desktop + WSL2 recommended |
| **WSL2** | ✅ Full | Access both Windows and Linux packages |

### Platform-Specific Features

**Linux:**
- Host network mode for best performance
- Direct volume mounts
- Native package manager access

**macOS:**
- Docker Desktop integration
- Homebrew support
- Bridge networking

**Windows:**
- PowerShell Core support
- CMD execution
- Winget integration
- WSL2 interoperability

**WSL2:**
- Access Windows drives (/mnt/c, /mnt/d)
- Run both Linux and Windows commands
- Best of both worlds

## Installation

### Quick Install

**Linux/macOS/WSL:**
```bash
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard
./scripts/install-docker-host.sh
```

**Windows (PowerShell):**
```powershell
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard
.\scripts\install-docker-host.ps1
```

### Manual Install

```bash
# 1. Clone repository
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard

# 2. Configure environment
cp .env.host .env
# Edit .env as needed

# 3. Build and start
docker-compose -f docker-compose.host.yml build
docker-compose -f docker-compose.host.yml up -d
```

## Testing

Run the test suite to verify installation:

```bash
./scripts/test-docker-host.sh
```

Expected output:
```
==========================================
✅ All Tests Passed!
==========================================
```

## Troubleshooting

### Common Issues

**Issue: Cannot access host packages**
```bash
# Solution: Check ENABLE_HOST_ACCESS
grep ENABLE_HOST_ACCESS .env
# Should be: ENABLE_HOST_ACCESS=true
```

**Issue: Docker socket permission denied**
```bash
# Solution: Add user to docker group (Linux)
sudo usermod -aG docker $USER
# Log out and log back in
```

**Issue: PowerShell not available**
```bash
# Solution: PowerShell Core is installed in Dockerfile.host
# If still issues, check container logs:
docker-compose -f docker-compose.host.yml logs backend
```

**Issue: Volume mount failures on Windows**
```powershell
# Solution: Enable drive sharing in Docker Desktop
# Settings → Resources → File Sharing → Add drives
```

## Limitations

1. **Host network mode** only works on Linux (macOS/Windows use bridge mode)
2. **Windows commands** require WSL2 or Docker Desktop with Windows containers
3. **SSH mode** requires SSH server configured on host
4. **Performance** may vary depending on execution mode
5. **Security** implications require careful configuration

## Future Enhancements

Potential improvements:
- [ ] Native Windows container support
- [ ] Kubernetes deployment option
- [ ] Remote host management
- [ ] Web-based host configuration UI
- [ ] CLI tool auto-discovery
- [ ] Package manager plugin system
- [ ] Enhanced security policies
- [ ] Multi-host orchestration

## Documentation

Complete documentation available:
- [Installation Guide](docs/INSTALLATION.md)
- [Usage Guide](docs/USAGE.md)
- [Docker Guide](docs/DOCKER.md)
- [Security Guidelines](docs/SECURITY.md)
- [API Documentation](docs/API.md)

## Support

- **Issues**: https://github.com/nsalvacao/Package_Audit_Dashboard/issues
- **Discussions**: https://github.com/nsalvacao/Package_Audit_Dashboard/discussions
- **Documentation**: `docs/` directory

## License

This feature is part of Package Audit Dashboard, licensed under MIT License.

---

**Version**: 1.0.0  
**Last Updated**: November 2024  
**Status**: Production Ready ✅
