# Installation Guide

Complete installation guide for Package Audit Dashboard with support for native installation (Windows/WSL/Linux/macOS) and Docker with full host system access.

## Table of Contents

1. [Overview](#overview)
2. [Installation Methods](#installation-methods)
3. [Docker Installation with Host Access](#docker-installation-with-host-access)
4. [Native Installation](#native-installation)
5. [WSL2 Installation](#wsl2-installation)
6. [Post-Installation Configuration](#post-installation-configuration)
7. [Troubleshooting](#troubleshooting)

---

## Overview

Package Audit Dashboard can be installed in multiple ways depending on your needs:

| Installation Method | Use Case | Host Package Access | Complexity |
|-------------------|----------|---------------------|------------|
| **Docker (Standard)** | Testing, isolated development | ❌ Container only | ⭐ Easy |
| **Docker (Host Access)** | Full host system auditing from Docker | ✅ Full host access | ⭐⭐ Medium |
| **Native (Windows)** | Windows package management | ✅ Windows packages | ⭐⭐ Medium |
| **Native (Linux/macOS)** | Linux/macOS package management | ✅ System packages | ⭐⭐ Medium |
| **WSL2** | Windows + Linux dual environment | ✅ Both Windows & Linux | ⭐⭐⭐ Advanced |

**Recommendation:**
- For **auditing your actual system packages**: Use **Docker with Host Access** or **Native Installation**
- For **testing or development only**: Use **Docker (Standard)**
- For **Windows users wanting both Windows and Linux support**: Use **WSL2**

---

## Installation Methods

### Quick Start Decision Tree

```
Do you want to audit your actual system's packages?
├─ Yes → Docker with Host Access OR Native Installation
│  ├─ Prefer isolation? → Docker with Host Access
│  └─ Prefer simplicity? → Native Installation
└─ No (just testing) → Docker (Standard)

Are you on Windows?
├─ Yes
│  ├─ Want Linux tools too? → WSL2 Installation
│  └─ Windows only → Native Windows OR Docker Host Access
└─ No (Linux/macOS) → Native Installation OR Docker Host Access
```

---

## Docker Installation with Host Access

This method runs the application in Docker but gives it full access to your host system's packages and commands.

### Prerequisites

- **Docker Desktop** 20.10+ ([Download](https://www.docker.com/products/docker-desktop))
- **Docker Compose** 2.0+ (included with Docker Desktop)
- **Windows users**: WSL2 backend enabled in Docker Desktop (recommended)
- **Linux users**: Docker installed and daemon running
- **macOS users**: Docker Desktop for Mac

### Installation Steps

#### For Windows (PowerShell)

```powershell
# 1. Clone the repository
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard

# 2. Run the installation script
.\scripts\install-docker-host.ps1

# 3. Access the application
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
```

#### For Linux/macOS/WSL (Bash)

```bash
# 1. Clone the repository
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard

# 2. Run the installation script
chmod +x scripts/install-docker-host.sh
./scripts/install-docker-host.sh

# 3. Access the application
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
```

#### Manual Installation

If you prefer to set up manually:

```bash
# 1. Clone and navigate
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard

# 2. Create environment configuration
cp .env.host .env

# 3. Edit .env to customize settings (optional)
# nano .env  # or your preferred editor

# 4. Build and start services
docker-compose -f docker-compose.host.yml build
docker-compose -f docker-compose.host.yml up -d

# 5. Verify services are running
docker-compose -f docker-compose.host.yml ps
```

### What Gets Installed

- **Backend container** with host access capabilities
- **Frontend container** for the web dashboard
- **Persistent volumes** for data storage on host
- **Host volume mounts** for package manager access
- **Docker socket access** for host command execution

### Host Access Features

✅ **Volume Persistence**: All data stored directly on host filesystem
✅ **Host Command Execution**: Can execute commands on your actual system
✅ **Package Manager Access**: Access npm, pip, brew, winget on host
✅ **CLI Tool Integration**: Can invoke gemini-cli, claude, codex, etc.
✅ **Windows Support**: PowerShell and CMD execution from container
✅ **WSL2 Support**: Access both Windows and Linux filesystems

### Security Considerations

⚠️ **Important**: This installation method gives the container significant access to your host system.

**What the container can access:**
- Execute commands on your host system
- Read/write files in mounted directories
- Access your package managers
- Invoke CLI tools

**Security recommendations:**
1. Review the `.env` configuration before starting
2. Only enable privileged mode if absolutely necessary
3. Keep Docker Desktop updated
4. Review logs regularly: `docker-compose -f docker-compose.host.yml logs`
5. See [SECURITY.md](../reference/SECURITY.md) for detailed security guidelines

### Useful Commands

```bash
# View logs
docker-compose -f docker-compose.host.yml logs -f

# View logs for specific service
docker-compose -f docker-compose.host.yml logs -f backend

# Stop services (keep data)
docker-compose -f docker-compose.host.yml stop

# Start services
docker-compose -f docker-compose.host.yml start

# Restart services
docker-compose -f docker-compose.host.yml restart

# Stop and remove containers (keep data)
docker-compose -f docker-compose.host.yml down

# Stop and remove everything including data (⚠️ DESTRUCTIVE)
docker-compose -f docker-compose.host.yml down -v

# Check service status
docker-compose -f docker-compose.host.yml ps

# Execute command in backend container
docker-compose -f docker-compose.host.yml exec backend bash

# Rebuild after code changes
docker-compose -f docker-compose.host.yml build --no-cache
docker-compose -f docker-compose.host.yml up -d
```

---

## Native Installation

Install and run the application directly on your system without Docker.

### Prerequisites

**All platforms:**
- **Python** 3.10+ ([Download](https://www.python.org/downloads/))
- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Git** ([Download](https://git-scm.com/downloads))

**Windows-specific:**
- **Visual Studio Build Tools** (for some Python packages)
- **Package managers**: npm, pip, winget (as needed)

**Linux-specific:**
- **Build essentials**: `sudo apt-get install build-essential python3-dev`
- **Package managers**: npm, pip, apt/dnf/pacman (as available)

**macOS-specific:**
- **Xcode Command Line Tools**: `xcode-select --install`
- **Homebrew** (recommended): `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

### Installation Steps

#### 1. Clone Repository

```bash
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (CMD):
.venv\Scripts\activate.bat
# Linux/macOS/WSL:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install optional dependencies for security scanning
pip install pip-audit pipdeptree

# Run tests to verify installation
pytest tests/ -v

# Start backend server
uvicorn app.main:app --reload
```

The backend will be available at: **http://localhost:8000**

#### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Run tests (optional)
npm test

# Start development server
npm run dev
```

The frontend will be available at: **http://localhost:5173**

#### 4. CLI Setup (Optional)

```bash
cd cli

# Install CLI tool
pip install -e .

# Verify installation
audit-cli --help

# Or run directly
python -m cli.audit_cli --help
```

### Using Automated Setup Script

We provide cross-platform setup scripts:

**Unix-based (Linux/macOS/WSL):**
```bash
./scripts/quick_setup.sh
```

**Cross-platform (Python):**
```bash
python3 scripts/quick_setup.py
```

### Post-Installation

After installation:

1. Access frontend: http://localhost:5173
2. Access backend: http://localhost:8000
3. View API docs: http://localhost:8000/docs
4. Check health: http://localhost:8000/health

---

## WSL2 Installation

For Windows users who want to use both Windows and Linux package managers.

### Prerequisites

- **Windows 10** version 2004+ or **Windows 11**
- **WSL2** enabled with a Linux distribution (Ubuntu recommended)
- **Docker Desktop** with WSL2 integration enabled
- **Windows Terminal** (recommended)

### Setup WSL2

If WSL2 is not already installed:

```powershell
# Run in PowerShell as Administrator

# Enable WSL
wsl --install

# Install Ubuntu (or your preferred distro)
wsl --install -d Ubuntu

# Set WSL2 as default
wsl --set-default-version 2

# Verify installation
wsl --list --verbose
```

### Install in WSL2

1. **Open WSL2 terminal** (Ubuntu or your distro)

2. **Install prerequisites:**
   ```bash
   # Update package list
   sudo apt-get update
   
   # Install Python, Node.js, and build tools
   sudo apt-get install -y python3 python3-pip python3-venv nodejs npm build-essential
   
   # Install Docker (if not using Docker Desktop)
   # curl -fsSL https://get.docker.com -o get-docker.sh
   # sudo sh get-docker.sh
   ```

3. **Clone and install:**
   ```bash
   cd ~
   git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
   cd Package_Audit_Dashboard
   
   # Option 1: Docker with host access
   ./scripts/install-docker-host.sh
   
   # Option 2: Native installation
   ./scripts/quick_setup.sh
   ```

### WSL2 + Docker Desktop Integration

1. **Enable WSL2 integration in Docker Desktop:**
   - Open Docker Desktop
   - Go to Settings → Resources → WSL Integration
   - Enable integration with your WSL2 distro (e.g., Ubuntu)
   - Click "Apply & Restart"

2. **Access Windows filesystem from WSL2:**
   ```bash
   # Windows C: drive
   cd /mnt/c/Users/YourName
   
   # Windows D: drive
   cd /mnt/d
   ```

3. **Access WSL filesystem from Windows:**
   - Open File Explorer
   - Navigate to: `\\wsl$\Ubuntu\home\username\Package_Audit_Dashboard`

### Features in WSL2

✅ **Dual Package Manager Access**: Manage both Windows (winget) and Linux (apt, pip, npm) packages
✅ **Shared Filesystem**: Access files from both Windows and Linux
✅ **Docker Integration**: Use Docker Desktop from WSL2
✅ **Performance**: Near-native Linux performance

---

## Post-Installation Configuration

### Environment Variables

After installation, you may want to customize the `.env` file:

```bash
# Copy example configuration
cp .env.example .env

# Edit configuration
nano .env  # or use your preferred editor
```

**Key configurations:**

```ini
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# CORS (add your domains)
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Data directory
DATA_DIR=~/.package-audit/data

# Security
LOCK_TIMEOUT=30
COMMAND_TIMEOUT=60

# Logging
LOG_LEVEL=INFO
```

For Docker host access, see `.env.host` for additional options.

### Firewall Configuration

**Windows Firewall:**
```powershell
# Allow backend port
New-NetFirewallRule -DisplayName "Package Audit Backend" -Direction Inbound -Port 8000 -Protocol TCP -Action Allow

# Allow frontend port
New-NetFirewallRule -DisplayName "Package Audit Frontend" -Direction Inbound -Port 5173 -Protocol TCP -Action Allow
```

**Linux (UFW):**
```bash
# Allow backend port
sudo ufw allow 8000/tcp

# Allow frontend port
sudo ufw allow 5173/tcp
```

### PATH Configuration

Some package managers may not be in your PATH. See [SETUP_PATH.md](SETUP_PATH.md) for detailed instructions on adding package managers to your PATH.

---

## Troubleshooting

### Docker Issues

**Problem: Docker daemon not running**
```bash
# Solution: Start Docker Desktop or Docker service
# Windows/macOS: Start Docker Desktop
# Linux:
sudo systemctl start docker
```

**Problem: Port already in use**
```bash
# Solution: Change port in docker-compose.host.yml
ports:
  - "8001:8000"  # Use 8001 instead of 8000
```

**Problem: Permission denied accessing Docker socket**
```bash
# Linux solution: Add user to docker group
sudo usermod -aG docker $USER
# Log out and log back in
```

**Problem: Container can't access host**
```bash
# Verify host access is enabled in .env
ENABLE_HOST_ACCESS=true
HOST_EXECUTION_MODE=docker

# Check volume mounts in docker-compose.host.yml
docker-compose -f docker-compose.host.yml config
```

### Native Installation Issues

**Problem: Python version too old**
```bash
# Check version
python3 --version

# Install newer Python (Linux)
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.11

# Use specific version
python3.11 -m venv .venv
```

**Problem: Node.js version too old**
```bash
# Check version
node --version

# Install Node Version Manager (nvm)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Install and use Node 18
nvm install 18
nvm use 18
```

**Problem: npm install fails on Windows**
```powershell
# Install Visual Studio Build Tools
# Download from: https://visualstudio.microsoft.com/downloads/
# Select "Desktop development with C++"

# Or use windows-build-tools
npm install --global windows-build-tools
```

**Problem: Backend port already in use**
```bash
# Find process using port 8000
# Linux/macOS:
lsof -i :8000
# Windows:
netstat -ano | findstr :8000

# Kill the process or change port in .env
API_PORT=8001
```

### WSL2 Issues

**Problem: WSL2 not starting**
```powershell
# Restart WSL
wsl --shutdown
wsl

# Update WSL
wsl --update
```

**Problem: Docker not accessible in WSL2**
- Ensure Docker Desktop WSL2 integration is enabled
- Restart Docker Desktop
- Restart WSL2: `wsl --shutdown`

**Problem: Slow file access from Windows**
- Use WSL2 filesystem (`/home/username`) instead of Windows filesystem (`/mnt/c`)
- Clone repository in WSL2 filesystem for better performance

### Package Manager Detection

**Problem: Package manager not detected**

```bash
# Verify package manager is installed
which npm
which pip
which brew
which winget

# Add to PATH if not found (see SETUP_PATH.md)
```

### Testing Installation

After installation, verify everything works:

```bash
# Test backend
curl http://localhost:8000/health

# Expected output:
# {"status":"healthy","version":"1.0.0"}

# Test frontend
curl http://localhost:5173

# Test API
curl http://localhost:8000/api/v1/discover

# Test package listing (replace 'npm' with your package manager)
curl http://localhost:8000/api/v1/managers/npm/packages
```

---

## Next Steps

After installation:

1. Read the [Usage Guide](USAGE.md) to learn how to use the application
2. Review [Security Guidelines](SECURITY.md) for best practices
3. Check [API Documentation](API.md) for API details
4. See [DOCKER.md](../deployment/DOCKER.md) for advanced Docker configurations

---

## Support

- **Documentation**: [docs/](.)
- **Issues**: https://github.com/nsalvacao/Package_Audit_Dashboard/issues
- **Discussions**: https://github.com/nsalvacao/Package_Audit_Dashboard/discussions

---

## Quick Reference

### Installation Commands Summary

```bash
# Docker Host Access (Linux/macOS/WSL)
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard
./scripts/install-docker-host.sh

# Docker Host Access (Windows PowerShell)
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard
.\scripts\install-docker-host.ps1

# Native Installation (All platforms)
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard
./scripts/quick_setup.sh  # or: python3 scripts/quick_setup.py
```

### Access URLs

- **Frontend Dashboard**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

**Installation complete!** Proceed to [USAGE.md](USAGE.md) to start using Package Audit Dashboard.
