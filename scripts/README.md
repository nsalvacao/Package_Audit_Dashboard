# Scripts Directory

Automation and utility scripts for Package Audit Dashboard.

## Installation Scripts

### Docker Host Access Installation

Install Package Audit Dashboard with Docker host access mode, enabling the container to access and manage packages on your host system.

#### Unix/Linux/macOS/WSL

```bash
./install-docker-host.sh
```

**Features:**
- Auto-detects operating system
- Configures host access volumes
- Sets up environment variables
- Builds and starts Docker containers
- Provides status and usage information

#### Windows (PowerShell)

```powershell
.\install-docker-host.ps1
```

**Features:**
- Windows-specific path configuration
- PowerShell/CMD support setup
- Docker Desktop integration
- WSL2 compatibility check

### Native Installation

Install Package Audit Dashboard directly on your system without Docker.

#### Unix/Linux/macOS/WSL

```bash
./quick_setup.sh
```

**What it does:**
- Checks system requirements (Python 3.10+, Node 18+)
- Creates Python virtual environment
- Installs backend dependencies
- Installs frontend dependencies
- Runs initial tests
- Provides startup instructions

#### Cross-Platform (Python)

```bash
python3 quick_setup.py
```

**Features:**
- Works on any platform with Python 3
- Automated dependency installation
- Environment setup
- Cross-platform compatibility checks

## Testing Scripts

### Docker Host Configuration Test

```bash
./test-docker-host.sh
```

**Tests:**
1. Docker installation check
2. Docker Compose availability
3. Configuration file validation
4. Python syntax validation
5. Documentation completeness
6. Installation scripts presence

**Output:**
- ✅ Pass indicators for each test
- ❌ Fail indicators with error messages
- Summary of test results

## Utility Scripts

### ChromaDB Synchronization

```bash
python3 chroma_sync.py
```

**Purpose:**
- Synchronizes project data with ChromaDB
- Used for AI-powered features
- Optional utility (not required for core functionality)

## Script Usage Guidelines

### Before Running Scripts

1. **Check Prerequisites:**
   ```bash
   # For Docker scripts
   docker --version
   docker compose version
   
   # For native scripts
   python3 --version
   node --version
   npm --version
   ```

2. **Make Scripts Executable (Unix/Linux/macOS):**
   ```bash
   chmod +x *.sh
   ```

3. **Review Configuration:**
   - Check `.env.example` or `.env.host`
   - Customize environment variables as needed

### Script Execution Order

**For Docker Host Access:**
```
1. test-docker-host.sh    (optional: verify setup)
2. install-docker-host.sh  (or .ps1 on Windows)
3. Verify services are running
```

**For Native Installation:**
```
1. quick_setup.sh (or .py)
2. Start backend manually
3. Start frontend manually
```

## Troubleshooting

### Script Permission Denied (Unix/Linux/macOS)

```bash
# Make scripts executable
chmod +x scripts/*.sh
```

### PowerShell Execution Policy (Windows)

```powershell
# Allow script execution (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run with bypass
PowerShell -ExecutionPolicy Bypass -File .\install-docker-host.ps1
```

### Script Not Found

```bash
# Ensure you're in the project root
cd Package_Audit_Dashboard

# Run with explicit path
./scripts/install-docker-host.sh
```

### Docker Command Not Found

```bash
# Install Docker Desktop or Docker Engine
# Linux: https://docs.docker.com/engine/install/
# macOS/Windows: https://www.docker.com/products/docker-desktop
```

### Python/Node Not Found

```bash
# Install Python 3.10+
# https://www.python.org/downloads/

# Install Node.js 18+
# https://nodejs.org/

# Or use version managers
# Python: pyenv
# Node: nvm
```

## Script Details

### install-docker-host.sh

**Platform:** Unix/Linux/macOS/WSL  
**Purpose:** Docker host access installation  
**Dependencies:** docker, docker-compose  
**Execution Time:** 2-5 minutes  
**Output:** Detailed installation progress with colored output

**Key Features:**
- OS detection (Linux, macOS, WSL, Windows)
- Automatic Docker version detection
- Environment configuration
- Security prompt for privileged mode
- Service health checks
- Access URL display

### install-docker-host.ps1

**Platform:** Windows  
**Purpose:** Docker host access installation  
**Dependencies:** Docker Desktop, PowerShell 5.1+  
**Execution Time:** 2-5 minutes  
**Output:** Colored progress messages

**Key Features:**
- Windows version detection
- WSL2 compatibility check
- Path conversion (Windows → Docker format)
- Docker Desktop integration
- PowerShell Core support check

### test-docker-host.sh

**Platform:** Unix/Linux/macOS/WSL  
**Purpose:** Configuration validation  
**Dependencies:** docker, python3  
**Execution Time:** 10-30 seconds  
**Output:** Test results with pass/fail indicators

**Tests Performed:**
1. Docker installation
2. Docker Compose availability
3. YAML syntax validation
4. Python syntax check
5. File existence checks
6. Documentation verification

### quick_setup.sh

**Platform:** Unix/Linux/macOS/WSL  
**Purpose:** Native installation  
**Dependencies:** python3, node, npm  
**Execution Time:** 3-10 minutes  
**Output:** Installation progress

**Steps:**
1. Requirements check
2. Backend setup (venv, dependencies)
3. Frontend setup (npm install)
4. Initial tests
5. Startup instructions

### quick_setup.py

**Platform:** Cross-platform  
**Purpose:** Native installation  
**Dependencies:** Python 3.10+  
**Execution Time:** 3-10 minutes  
**Output:** Installation progress

**Advantages:**
- Works on any OS with Python
- No shell dependencies
- Unified cross-platform behavior

## Contributing

When adding new scripts:

1. **Follow naming conventions:**
   - Installation: `install-*.sh` or `install-*.ps1`
   - Testing: `test-*.sh` or `test-*.ps1`
   - Utilities: descriptive names

2. **Include documentation:**
   - Script purpose
   - Prerequisites
   - Usage examples
   - Expected output

3. **Add error handling:**
   - Check prerequisites
   - Validate inputs
   - Provide clear error messages
   - Suggest solutions

4. **Make scripts user-friendly:**
   - Colored output (when supported)
   - Progress indicators
   - Clear success/failure messages
   - Help text

5. **Test thoroughly:**
   - Test on target platforms
   - Verify error handling
   - Check edge cases

## Additional Resources

- **[Installation Guide](../docs/guides/INSTALLATION.md)** - Complete installation instructions
- **[Docker Guide](../docs/deployment/DOCKER.md)** - Docker-specific documentation
- **[Contributing](../CONTRIBUTING.md)** - Contribution guidelines

---

**Last Updated:** November 2024  
**Maintained By:** Package Audit Dashboard Contributors
