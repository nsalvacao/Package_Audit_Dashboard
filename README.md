# 📦 Package Audit Dashboard

[![Tests](https://github.com/nsalvacao/Package_Audit_Dashboard/actions/workflows/test.yml/badge.svg)](https://github.com/nsalvacao/Package_Audit_Dashboard/actions/workflows/test.yml)
[![Docker Build](https://github.com/nsalvacao/Package_Audit_Dashboard/actions/workflows/docker.yml/badge.svg)](https://github.com/nsalvacao/Package_Audit_Dashboard/actions/workflows/docker.yml)
[![codecov](https://codecov.io/gh/nsalvacao/Package_Audit_Dashboard/branch/main/graph/badge.svg)](https://codecov.io/gh/nsalvacao/Package_Audit_Dashboard)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
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

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard

# Run the setup script
./scripts/quick_setup.sh

# Or use the cross-platform Python version
python3 scripts/quick_setup.py
```

### Option 2: Manual Setup

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
