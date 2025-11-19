# 📦 Package Audit Dashboard

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/nsalvacao/Package_Audit_Dashboard?quickstart=1)
[![Tests](https://github.com/nsalvacao/Package_Audit_Dashboard/actions/workflows/test.yml/badge.svg)](https://github.com/nsalvacao/Package_Audit_Dashboard/actions/workflows/test.yml)
[![Docker Build](https://github.com/nsalvacao/Package_Audit_Dashboard/actions/workflows/docker.yml/badge.svg)](https://github.com/nsalvacao/Package_Audit_Dashboard/actions/workflows/docker.yml)
[![codecov](https://codecov.io/gh/nsalvacao/Package_Audit_Dashboard/branch/main/graph/badge.svg)](https://codecov.io/gh/nsalvacao/Package_Audit_Dashboard)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![Node 18+](https://img.shields.io/badge/node-18+-brightgreen.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Local dashboard (plus CLI companion) for auditing, managing, and maintaining package managers such as npm, pip, winget, and brew with a strong emphasis on operational security.

---

## ✨ Features

### Phase 1 (MVP) — Completed
- 🔍 **Auto-discovery** of installed package managers (npm, pip, winget, brew)
- 🗑️ **Safe uninstall** with automatic snapshots before removal
- 🔒 **Security layer** with ValidationLayer, LockManager, and OperationQueue
- 🎯 **REST API** with automatic documentation (FastAPI)
- 💻 **CLI** for terminal-driven workflows
- 🌐 **Web dashboard** built with React + TypeScript + TailwindCSS
- 📊 **Snapshot management** for backup and restore
- 🛡️ **Command injection and race-condition prevention** baked into the core

### Phase 2 (NEW!) — Recently Released
- 📡 **Real-time log streaming** powered by Server-Sent Events (SSE)
- 🌳 **Dependency tree visualization** for dependency analysis
- 🔐 **Integrated vulnerability scanning** (npm audit, pip-audit)
- 📦 **Batch operations** to uninstall multiple packages at once
- ⏮️ **Automatic rollback** to revert changes safely
- 📄 **Lock file export** (requirements.txt, package-lock.json)

---

## 🚀 Quick Start

### Option 1: GitHub Codespaces (☁️ Instant Cloud Development)

**Perfect for**: Quick start, no local setup, GitHub Student Pack users

Click the badge at the top or use this button:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/nsalvacao/Package_Audit_Dashboard?quickstart=1)

**What you get**:
- ✅ Fully configured dev environment in ~3 minutes
- ✅ All dependencies pre-installed (Python, Node, Docker)
- ✅ VS Code in browser with GitHub Copilot enabled
- ✅ Automatic port forwarding for frontend & backend
- ✅ 180 core-hours/month free with Student Developer Pack

**After Codespace starts**:
```bash
# Everything is set up automatically!
# Just run:
./start-all.sh

# Or start services individually:
# Backend:  cd backend && source .venv/bin/activate && uvicorn app.main:app --reload
# Frontend: cd frontend && npm run dev
```

**📖 Full guide**: See [docs/CODESPACES.md](docs/CODESPACES.md) for detailed Codespaces usage and [docs/COPILOT_GUIDE.md](docs/COPILOT_GUIDE.md) for GitHub Copilot integration.

---

### Option 2: Docker Setup (Isolated Environment)

**Perfect for**: Testing, development, isolated environments

**⚠️ Important Note**: Docker installation audits packages **inside the container** only. For auditing your host system's packages (npm, pip, brew, winget), use **Option 3 or 4** (native installation).

```bash
# Clone the repository
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard

# Start all services with Docker Compose
docker-compose up -d

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

**What you get with Docker**:
- ✅ Isolated environment
- ✅ No dependency installation on host
- ✅ Quick setup with one command
- ⚠️ Only audits container packages, not host system

**To stop services**:
```bash
docker-compose down
```

---

### Option 3: Automated Local Setup (Native - Recommended for System Auditing)

**Perfect for**: Auditing your actual system's installed packages (npm, pip, brew, winget)

```bash
# Clone the repository
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard

# Run the setup script
./scripts/quick_setup.sh

# Or use the cross-platform Python version
python3 scripts/quick_setup.py
```

---

### Option 4: Manual Setup (Native)

#### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Start the server
uvicorn app.main:app --reload
```

The backend will be available at: http://localhost:8000

**Interactive API documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at: http://localhost:5173

#### 3. CLI Setup (Optional)

```bash
cd backend
source .venv/bin/activate

# Install the CLI
pip install -e ../cli

# Or run it directly
python -m cli.audit_cli --help
```

---

## 📖 How to Use

After installation, access the dashboard at **http://localhost:5173** (frontend) with the backend running at **http://localhost:8000**.

### Basic Workflow

1. **Select a Package Manager**
   - The Overview tab auto-detects installed managers (npm, pip, brew, winget)
   - Click on any manager card to select it
   - Your selection persists across sessions

2. **View Installed Packages**
   - Navigate to the **Packages** tab
   - Search and filter packages by name
   - View package versions and details

3. **Uninstall Packages**
   - **Single uninstall**: Click "Uninstall" button next to any package
   - **Batch uninstall**: Go to Operations tab, enter package names (one per line)
   - All uninstalls automatically create snapshots for rollback

4. **Security Audits**
   - Go to the **Security** tab
   - Click "Scan Vulnerabilities" to audit installed packages
   - View results with severity levels (critical/high/medium/low)

5. **Advanced Features**
   - **Export lockfiles**: Download requirements.txt or package-lock.json
   - **Dependency trees**: Visualize package dependencies
   - **Rollback**: Restore previous states using snapshots

### Common Use Cases

```bash
# Use Case 1: Clean up unused packages
1. Select manager → Packages tab → Search package → Uninstall
2. System creates snapshot → Package removed → Snapshot ID returned

# Use Case 2: Security audit
1. Select manager → Security tab → Scan Vulnerabilities
2. Review critical/high severity issues → Plan remediation

# Use Case 3: Batch cleanup
1. Select manager → Operations tab → Enter package list
2. Click "Batch Uninstall" → Review results

# Use Case 4: Safe experimentation
1. Install test packages → Try functionality
2. Operations tab → Rollback → Select snapshot → Restore
```

### CLI Usage (Optional)

```bash
# Discover package managers
python -m cli.audit_cli discover

# List packages
python -m cli.audit_cli list npm

# Uninstall package
python -m cli.audit_cli uninstall npm lodash

# Security scan
python -m cli.audit_cli scan npm
```

---

## 📁 Project Structure

```
package-audit-dashboard/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── adapters/          # Package manager adapters (npm, pip, etc.)
│   │   ├── analysis/          # Snapshot management
│   │   ├── core/              # Security layer (validation, locking, queue)
│   │   ├── routers/           # API endpoints
│   │   ├── storage/           # JSON storage
│   │   └── main.py            # FastAPI application
│   ├── tests/                 # Comprehensive test suite
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # React + Vite frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── hooks/             # Custom React hooks
│   │   └── App.tsx            # Main application
│   └── package.json           # Node dependencies
│
├── cli/                        # Typer CLI
│   ├── audit_cli/
│   │   ├── app.py             # CLI commands
│   │   └── __main__.py        # Entry point
│   └── setup.py               # CLI installation
│
├── docs/                       # Documentation
│   ├── SECURITY.md            # Security architecture
│   ├── LIMITATIONS.md         # Known limitations
│   ├── SETUP_PATH.md          # PATH configuration guide
│   └── API.md                 # API documentation
│
├── scripts/                    # Setup scripts
│   ├── quick_setup.sh         # Automated setup (Unix)
│   ├── quick_setup.py         # Automated setup (cross-platform)
│   └── chroma_sync.py         # ChromaDB synchronization
│
├── BLUEPRINT_FINAL.md          # Complete project blueprint
├── FASE1_BREAKDOWN.md          # Phase 1 task breakdown
└── LOG.md                      # Development log
```
