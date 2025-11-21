# Changelog — Phase 2 Release

## Version 0.2.0 — Phase 2 Complete (2025-11-05)

### 🎉 Major Features

#### 1. Real-time Log Streaming (SSE)
- **Router:** `/api/streaming`
- **Endpoint:** `GET /api/streaming/{manager_id}/packages/{package_name}/uninstall`
- Server-Sent Events (SSE) stream live updates for uninstall operations
- Log streaming throughout the uninstall lifecycle
- Optimized SSE headers (`Cache-Control`, `X-Accel-Buffering`)

#### 2. Dependency Tree Visualization
- **Router:** `/api/advanced`
- **Endpoints:**
  - `GET /api/advanced/{manager_id}/dependency-tree` — Full tree
  - `GET /api/advanced/{manager_id}/dependency-tree/{package_name}` — Specific package
- **npm:** Uses native `npm list --json`
- **pip:** Supports `pipdeptree` (optional) with fallback to `pip show`

#### 3. Vulnerability Scanning
- **Endpoint:** `GET /api/advanced/{manager_id}/vulnerabilities`
- **npm:** Integrates `npm audit --json`
- **pip:** Integrates `pip-audit --format=json` (optional install)
- Returns vulnerabilities with severity, description, and affected packages

#### 4. Batch Operations
- **Endpoint:** `POST /api/advanced/{manager_id}/batch-uninstall`
- Uninstalls multiple packages in a single operation
- Automatic snapshot created before the batch runs
- Returns success/failure details per package
- Request model: `BatchUninstallRequest`
- Response model: `BatchUninstallResponse`

#### 5. Automatic Rollback
- **Endpoint:** `POST /api/advanced/{manager_id}/rollback/{snapshot_id}`
- Restores the system to a previous snapshot state
- Automatically removes packages not present in the snapshot
- Returns lists of uninstalled packages and failures

#### 6. Lock File Export
- **Endpoint:** `GET /api/advanced/{manager_id}/lockfile`
- **npm:** Exports `npm list --json` (lockfile equivalent)
- **pip:** Exports `pip freeze` (requirements.txt)
- Frontend downloads files with the correct format

### 🔧 Backend Changes

#### New Files
- `backend/app/routers/streaming.py` — SSE router
- `backend/app/routers/advanced.py` — Advanced feature router
- `backend/tests/test_advanced_router.py` — Advanced router tests
- `backend/tests/test_streaming_router.py` — Streaming router tests

#### Modified Files
- `backend/app/main.py` — Registers new routers, bumps version to 0.2.0
- `backend/app/routers/__init__.py` — Exposes new routers
- `backend/app/adapters/base.py` — Adds:
  - `get_dependency_tree()`
  - `scan_vulnerabilities()`
  - `export_lockfile()`
- `backend/app/adapters/npm.py` — Implements new npm features
- `backend/app/adapters/pip.py` — Implements new pip features

### 🎨 Frontend Changes

#### New Components
- `frontend/src/components/VulnerabilityScan.tsx` — Vulnerability scanner
- `frontend/src/components/LockfileExport.tsx` — Lockfile exporter

#### Updated Components
- `frontend/src/components/ManagerCard.tsx`:
  - Integrates VulnerabilityScan
  - Integrates LockfileExport
  - Adds link to Dependency Tree
  - Expandable UI for "Advanced Features"

### 📚 Documentation

#### Updated Files
- `README.md`:
  - Adds "What's New in Phase 2" section
  - Updates feature list with Phase 2 highlights
  - Adds API examples for advanced features
  - Updates roadmap (Phase 2 ✅ COMPLETE)
  - Refreshes project status
- `CHANGELOG_PHASE2.md` — This file

### 🧪 Testing

#### New Test Files
- `test_advanced_router.py`:
  - Dependency tree tests
  - Vulnerability scanning tests
  - Lockfile export tests
  - Batch operation tests
  - Rollback tests
- `test_streaming_router.py`:
  - SSE endpoint tests
  - SSE header validation

### 🔒 Security

All new features preserve the security guarantees established in Phase 1:
- ✅ ValidationLayer for input sanitization
- ✅ LockManager for race-condition prevention
- ✅ OperationQueue for serialized mutations
- ✅ Automatic snapshots before destructive actions

### 📦 Dependencies

#### Optional Dependencies (for advanced features)
- **pip-audit** — pip vulnerability scanning
  ```bash
  pip install pip-audit
  ```
- **pipdeptree** — pip dependency trees
  ```bash
  pip install pipdeptree
  ```

#### Frontend Dependencies
No new packages — relies on existing stack:
- @tanstack/react-query
- axios
- react
- typescript

### 🚀 Migration Guide

#### Upgrade from Phase 1 to Phase 2

1. **Pull the latest changes:**
   ```bash
   git pull origin main
   ```

2. **Backend** (no dependency changes):
   ```bash
   cd backend
   # Same dependencies as Phase 1
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

3. **Frontend** (no dependency changes):
   ```bash
   cd frontend
   npm install  # or yarn install
   npm run dev
   ```

4. **Optional — Install analysis tools:**
   ```bash
   # For pip vulnerability scanning
   pip install pip-audit

   # For full pip dependency trees
   pip install pipdeptree
   ```
