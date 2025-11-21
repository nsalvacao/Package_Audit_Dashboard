# Usage Guide

Complete guide for using Package Audit Dashboard to manage and audit your system's packages.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Web Dashboard Usage](#web-dashboard-usage)
3. [CLI Usage](#cli-usage)
4. [API Usage](#api-usage)
5. [Docker Host Access Features](#docker-host-access-features)
6. [Advanced Features](#advanced-features)
7. [Common Workflows](#common-workflows)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Getting Started

After installation, you can access the application through:

- **Web Dashboard**: http://localhost:5173 (Recommended for most users)
- **CLI**: `audit-cli` command or `python -m cli.audit_cli`
- **API**: http://localhost:8000 with interactive docs at http://localhost:8000/docs

### First Run Checklist

Before using the application:

1. ✅ Ensure backend is running: http://localhost:8000/health
2. ✅ Ensure frontend is accessible: http://localhost:5173
3. ✅ Check package managers are detected: Visit the Overview tab
4. ✅ Review security settings in `.env` file
5. ✅ (Docker only) Verify host access if using docker-compose.host.yml

---

## Web Dashboard Usage

The web dashboard provides a user-friendly interface for all operations.

### Overview Tab

**Purpose**: View detected package managers and system status

1. **Open the dashboard**: Navigate to http://localhost:5173
2. **Check detected managers**: The Overview tab shows all available package managers
3. **Select a manager**: Click on any package manager card (npm, pip, brew, winget)
4. **View statistics**: See total packages, outdated packages, and vulnerabilities

**Example detected managers:**
- 📦 **npm** - Node Package Manager (JavaScript/TypeScript)
- 🐍 **pip** - Python Package Manager
- 🍺 **brew** - Homebrew (macOS/Linux)
- 📦 **winget** - Windows Package Manager

### Packages Tab

**Purpose**: View and manage installed packages

#### Viewing Packages

1. Navigate to **Packages** tab
2. Select package manager from dropdown (if not already selected)
3. Browse the list of installed packages
4. Use search bar to filter by package name

**Information displayed:**
- Package name
- Current version
- Installation date (if available)
- Dependencies count
- Status (outdated, vulnerable, etc.)

#### Uninstalling a Package

**⚠️ Warning**: Uninstalling packages can break dependencies. Always create snapshots first.

1. Find the package you want to uninstall
2. Click the **Uninstall** button next to the package
3. Review the confirmation dialog
4. Confirm uninstallation
5. A snapshot is automatically created before removal
6. Monitor progress in the notifications
7. Review the result and snapshot ID

**Safety features:**
- Automatic snapshot creation before uninstall
- Validation of package names
- Lock mechanism prevents concurrent modifications
- Detailed logging of all operations

### Security Tab

**Purpose**: Scan for vulnerabilities in installed packages

#### Running a Security Scan

1. Navigate to **Security** tab
2. Select package manager
3. Click **Scan Vulnerabilities**
4. Wait for scan to complete (may take 30-60 seconds)
5. Review results by severity

**Vulnerability Severity Levels:**
- 🔴 **Critical**: Immediate action required
- 🟠 **High**: Action required soon
- 🟡 **Medium**: Plan remediation
- 🟢 **Low**: Monitor and review

#### Understanding Scan Results

Each vulnerability shows:
- **Package name**: Affected package
- **Severity**: Risk level
- **Description**: What the vulnerability is
- **Recommendation**: How to fix it
- **CVE ID**: Common Vulnerabilities and Exposures identifier (if available)

#### Fixing Vulnerabilities

**Recommended workflow:**
1. Review all critical and high severity issues
2. Check if updates are available
3. Update packages: `npm update` or `pip install --upgrade`
4. Re-run scan to verify fixes
5. For remaining issues, check for patches or workarounds

### Operations Tab

**Purpose**: Batch operations and advanced management

#### Batch Uninstall

Remove multiple packages at once:

1. Navigate to **Operations** tab
2. Select **Batch Uninstall**
3. Enter package names (one per line):
   ```
   lodash
   moment
   underscore
   ```
4. Click **Execute Batch Uninstall**
5. Review progress for each package
6. A snapshot is created before the operation
7. Check results showing success/failure for each package

#### Rollback

Restore system to a previous state:

1. Navigate to **Operations** tab
2. Select **Rollback**
3. Choose a snapshot from the list
4. Review snapshot details (date, packages affected)
5. Click **Restore Snapshot**
6. Confirm the action
7. Wait for restoration to complete

**Note**: Rollback reinstalls packages that were present at snapshot time.

#### Export Lockfile

Generate dependency lockfiles:

1. Navigate to **Operations** tab
2. Select **Export Lockfile**
3. Choose format:
   - **package-lock.json** (npm)
   - **requirements.txt** (pip)
4. Click **Export**
5. Download the generated file

**Use cases:**
- Share exact dependencies with team
- Reproduce environment on another machine
- Archive current state for compliance

### Dependency Tree

**Purpose**: Visualize package dependencies

1. Navigate to **Dependencies** tab
2. Select package manager
3. Optional: Enter specific package name to see its tree
4. Click **Generate Tree**
5. Explore the interactive tree visualization

**Tree features:**
- Expandable/collapsible nodes
- Color-coded by depth
- Shows version information
- Identifies circular dependencies
- Highlights outdated packages

### Settings

**Purpose**: Configure application behavior

Available settings:
- **Auto-snapshot**: Enable/disable automatic snapshots
- **Snapshot retention**: Number of snapshots to keep
- **Command timeout**: Maximum time for commands
- **Debug mode**: Enable verbose logging
- **API endpoint**: Backend URL (for frontend)

---

## CLI Usage

The command-line interface provides terminal-based access to all features.

### Installation

```bash
cd cli
pip install -e .
```

Or run directly:
```bash
python -m cli.audit_cli [command]
```

### Available Commands

#### Discover Package Managers

```bash
# List all detected package managers
audit-cli discover

# Example output:
# Detected Package Managers:
#   ✓ npm - v9.8.1
#   ✓ pip - v23.2.1
#   ✓ brew - v4.1.0
```

#### List Packages

```bash
# List all packages for a manager
audit-cli list npm

# With JSON output
audit-cli list npm --format json

# Save to file
audit-cli list npm --output packages.txt
```

#### Uninstall Package

```bash
# Uninstall a package
audit-cli uninstall npm lodash

# Force uninstall (skip confirmations)
audit-cli uninstall npm lodash --force

# Uninstall without snapshot
audit-cli uninstall npm lodash --no-snapshot
```

#### Security Scan

```bash
# Run vulnerability scan
audit-cli scan npm

# Output as JSON
audit-cli scan npm --format json

# Filter by severity
audit-cli scan npm --severity critical
audit-cli scan npm --severity high,critical
```

#### Dependency Tree

```bash
# Show dependency tree for all packages
audit-cli deps npm

# Show tree for specific package
audit-cli deps npm react

# Output as JSON
audit-cli deps npm --format json
```

#### Snapshots

```bash
# List snapshots
audit-cli snapshots list

# Create manual snapshot
audit-cli snapshots create --name "before-update"

# Restore snapshot
audit-cli snapshots restore <snapshot-id>

# Delete snapshot
audit-cli snapshots delete <snapshot-id>
```

#### Export

```bash
# Export lockfile
audit-cli export npm --output package-lock.json
audit-cli export pip --output requirements.txt
```

### CLI Options

Global options available for all commands:

```bash
--verbose, -v    # Enable verbose output
--quiet, -q      # Suppress non-error output
--no-color       # Disable colored output
--format         # Output format: text, json, yaml
--help, -h       # Show help message
```

### CLI Examples

```bash
# Find outdated packages
audit-cli list npm | grep "outdated"

# Count installed packages
audit-cli list npm | wc -l

# Security scan and save results
audit-cli scan pip --format json > security-report.json

# Batch uninstall (with confirmation)
cat packages-to-remove.txt | xargs -I {} audit-cli uninstall npm {}

# Create snapshot before major update
audit-cli snapshots create --name "pre-update-$(date +%Y%m%d)"
npm update
```

---

## API Usage

The REST API provides programmatic access to all features.

### API Documentation

Interactive documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Base URL

```
http://localhost:8000/api/v1
```

### Authentication

Currently, no authentication is required. For production use, implement authentication as described in [SECURITY.md](../reference/SECURITY.md).

### Common Endpoints

#### Health Check

```bash
GET /health

curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Discover Managers

```bash
GET /api/v1/discover

curl http://localhost:8000/api/v1/discover
```

Response:
```json
{
  "managers": [
    {
      "id": "npm",
      "name": "npm",
      "version": "9.8.1",
      "available": true,
      "executable": "/usr/local/bin/npm"
    }
  ]
}
```

#### List Packages

```bash
GET /api/v1/managers/{manager_id}/packages

curl http://localhost:8000/api/v1/managers/npm/packages
```

Response:
```json
{
  "manager": "npm",
  "packages": [
    {
      "name": "express",
      "version": "4.18.2",
      "description": "Fast, unopinionated, minimalist web framework"
    }
  ],
  "count": 1
}
```

#### Uninstall Package

```bash
POST /api/v1/managers/{manager_id}/uninstall
Content-Type: application/json

{
  "package": "lodash",
  "force": false
}

curl -X POST http://localhost:8000/api/v1/managers/npm/uninstall \
  -H "Content-Type: application/json" \
  -d '{"package":"lodash"}'
```

#### Security Scan

```bash
GET /api/v1/managers/{manager_id}/scan

curl http://localhost:8000/api/v1/managers/npm/scan
```

#### Batch Operations

```bash
POST /api/v1/managers/{manager_id}/batch/uninstall
Content-Type: application/json

{
  "packages": ["lodash", "moment", "underscore"]
}

curl -X POST http://localhost:8000/api/v1/managers/npm/batch/uninstall \
  -H "Content-Type: application/json" \
  -d '{"packages":["lodash","moment"]}'
```

### API Response Format

All API responses follow this structure:

**Success:**
```json
{
  "status": "success",
  "data": { /* response data */ },
  "message": "Operation completed successfully"
}
```

**Error:**
```json
{
  "status": "error",
  "error": {
    "code": "PACKAGE_NOT_FOUND",
    "message": "Package 'xyz' not found",
    "details": { /* additional context */ }
  }
}
```

### Rate Limiting

Default rate limits:
- 100 requests per minute per IP
- Batch operations count as 1 request
- Contact server admin to increase limits if needed

---

## Docker Host Access Features

When using Docker with host access (`docker-compose.host.yml`), additional features are available.

### Executing Host Commands

The application can execute commands directly on your host system:

```python
# Via API
POST /api/v1/host/execute
{
  "command": ["npm", "list", "-g"],
  "shell": "bash"
}
```

### Accessing Host Package Managers

Docker container can interact with package managers installed on host:

- **npm** on host (not just container)
- **pip** on host
- **brew** on macOS/Linux host
- **winget** on Windows host (via PowerShell)

### Invoking CLI Tools on Host

Call AI coding assistants and other CLI tools on your host:

```python
# Example: Invoke gemini-cli on host
POST /api/v1/host/cli-tool
{
  "tool": "gemini-cli",
  "args": ["--help"]
}
```

**Supported tools** (if installed on host):
- gemini-cli
- claude (Anthropic CLI)
- codex (OpenAI Codex)
- aider
- cursor
- Any custom CLI tool

### Windows PowerShell/CMD Execution

Execute Windows commands from container:

```python
# PowerShell
POST /api/v1/host/execute
{
  "command": "Get-Package",
  "shell": "powershell"
}

# CMD
POST /api/v1/host/execute
{
  "command": "dir C:\\Users",
  "shell": "cmd"
}
```

### WSL2 Interop

Access both Windows and Linux from same container:

```python
# Linux command
POST /api/v1/host/execute
{
  "command": ["apt", "list", "--installed"],
  "shell": "bash"
}

# Windows command via WSL interop
POST /api/v1/host/execute
{
  "command": "winget list",
  "shell": "powershell"
}
```

### Security Considerations

⚠️ **Host access is powerful but requires caution:**

1. **Validate all input**: Never execute user-provided commands without validation
2. **Use least privilege**: Run with minimal required permissions
3. **Audit logs**: Monitor all host command executions
4. **Limit scope**: Only mount necessary directories
5. **Review regularly**: Check logs and access patterns

---

## Advanced Features

### Real-Time Log Streaming

Monitor operations in real-time using Server-Sent Events (SSE):

```javascript
// JavaScript example
const eventSource = new EventSource('http://localhost:8000/api/v1/stream/logs');

eventSource.onmessage = (event) => {
  const log = JSON.parse(event.data);
  console.log(`[${log.level}] ${log.message}`);
};
```

### Custom Snapshots

Create named snapshots for important states:

```bash
# CLI
audit-cli snapshots create --name "production-stable-2024-01"

# API
POST /api/v1/snapshots
{
  "name": "production-stable-2024-01",
  "description": "Stable state before major update"
}
```

### Dependency Analysis

Analyze dependency trees to:
- Identify bloated dependencies
- Find duplicate dependencies
- Detect circular dependencies
- Calculate dependency depth

```bash
# CLI
audit-cli deps npm --analyze

# Shows:
# - Total dependencies: 523
# - Max depth: 8
# - Duplicates: 12
# - Circular: 0
```

### Package Health Score

Get an overall health score for your packages:

```bash
GET /api/v1/managers/{manager_id}/health

# Returns:
# {
#   "score": 85,
#   "factors": {
#     "outdated": 15,
#     "vulnerable": 5,
#     "deprecated": 2
#   }
# }
```

---

## Common Workflows

### Workflow 1: Clean Up Unused Packages

```bash
# 1. Create snapshot
audit-cli snapshots create --name "before-cleanup"

# 2. List installed packages
audit-cli list npm

# 3. Identify unused packages
# (manually review or use external tools)

# 4. Uninstall unused packages
audit-cli uninstall npm unused-package-1
audit-cli uninstall npm unused-package-2

# 5. Verify application still works
npm test

# 6. If issues, rollback
audit-cli snapshots restore <snapshot-id>
```

### Workflow 2: Security Audit

```bash
# 1. Run vulnerability scan
audit-cli scan npm --format json > scan-results.json

# 2. Review critical issues
audit-cli scan npm --severity critical

# 3. Update vulnerable packages
npm update

# 4. Re-scan to verify
audit-cli scan npm

# 5. Document remaining issues
audit-cli scan npm --format json > scan-final.json
```

### Workflow 3: Dependency Hygiene

```bash
# 1. Check for outdated packages
npm outdated

# 2. View dependency tree
audit-cli deps npm

# 3. Create snapshot before update
audit-cli snapshots create --name "pre-update"

# 4. Update packages
npm update

# 5. Run tests
npm test

# 6. Verify no vulnerabilities
audit-cli scan npm
```

### Workflow 4: Environment Replication

```bash
# On source machine:
# 1. Export lockfile
audit-cli export npm --output package-lock.json

# 2. Transfer file to target machine

# On target machine:
# 3. Install packages
npm ci --package-lock-only

# 4. Verify
audit-cli list npm
```

---

## Best Practices

### 1. Always Create Snapshots

Before any destructive operation:
```bash
audit-cli snapshots create --name "before-$(date +%Y%m%d-%H%M%S)"
```

### 2. Regular Security Scans

Schedule regular scans:
```bash
# Add to crontab (daily at 2 AM)
0 2 * * * cd /path/to/project && audit-cli scan npm --format json > /var/log/security-$(date +%Y%m%d).json
```

### 3. Monitor Dependency Bloat

Keep track of dependency count:
```bash
audit-cli list npm | wc -l
```

### 4. Document Major Changes

Use named snapshots for milestones:
```bash
audit-cli snapshots create --name "v2.0.0-release"
```

### 5. Review Logs Regularly

```bash
# Docker
docker-compose logs -f backend | grep ERROR

# Native
tail -f ~/.package-audit/logs/app.log
```

### 6. Use Lock Files

Always commit lock files to version control:
- `package-lock.json` (npm)
- `requirements.txt` (pip)
- `Gemfile.lock` (Ruby)

### 7. Test After Changes

```bash
# After package operations
npm test  # or appropriate test command
```

---

## Troubleshooting

### Package Manager Not Detected

**Problem**: Package manager shows as unavailable

**Solutions**:
1. Verify installation: `which npm` / `where npm`
2. Check PATH: `echo $PATH` / `$env:Path`
3. Restart application after installing package manager
4. See [SETUP_PATH.md](SETUP_PATH.md) for PATH configuration

### Operation Timeout

**Problem**: Commands timeout before completing

**Solutions**:
```ini
# Increase timeout in .env
COMMAND_TIMEOUT=120
```

### Permission Denied

**Problem**: Cannot execute commands

**Solutions**:
```bash
# Linux: Add user to necessary groups
sudo usermod -aG docker $USER

# Windows: Run as Administrator
# or check Docker Desktop settings
```

### Snapshot Restore Fails

**Problem**: Cannot restore snapshot

**Solutions**:
1. Check snapshot integrity: `audit-cli snapshots list`
2. Verify disk space: `df -h` / `Get-PSDrive`
3. Check logs for specific error
4. Try manual package reinstallation

### Host Access Not Working (Docker)

**Problem**: Container cannot access host

**Solutions**:
1. Verify ENABLE_HOST_ACCESS=true in .env
2. Check Docker socket is mounted
3. Restart Docker Desktop
4. Review docker-compose.host.yml configuration

---

## Next Steps

- Review [API Documentation](../reference/API.md) for detailed API reference
- Check [Security Guidelines](../reference/SECURITY.md) for hardening
- See [Docker Guide](../deployment/DOCKER.md) for advanced Docker usage
- Read [Limitations](../reference/LIMITATIONS.md) for known issues

---

## Support

- **Documentation**: Full docs in `docs/` directory
- **Issues**: https://github.com/nsalvacao/Package_Audit_Dashboard/issues
- **Discussions**: https://github.com/nsalvacao/Package_Audit_Dashboard/discussions

---

**Happy auditing!** 🎉
