# 🚀 Phase 1 — Implementation Breakdown

## Phase 1 Overview

**Objective:** Deliver a secure, fully functional MVP.
**Duration:** 1–2 weeks.
**Priority:** Security first.

**Deliverables:**
- ✅ Dashboard that lists packages
- ✅ Secure uninstall workflow with confirmation
- ✅ PATH validation with script generation
- ✅ Automatic snapshot before uninstall
- ✅ Protection against command injection and race conditions

---

## 📋 Task List Overview

### Setup & Infrastructure (Tasks 1–3)
- [ ] Task 1.1: Create the project structure
- [ ] Task 1.2: Set up the backend (FastAPI)
- [ ] Task 1.3: Set up the frontend (React + Vite)

### Security Layer — CRITICAL (Tasks 4–6)
- [ ] Task 2.1: Implement the ValidationLayer
- [ ] Task 2.2: Implement the LockManager
- [ ] Task 2.3: Implement the OperationQueue

### Core Backend (Tasks 7–10)
- [ ] Task 3.1: Implement the CommandExecutor
- [ ] Task 3.2: Implement JSON Storage
- [ ] Task 3.3: Implement the BaseAdapter interface
- [ ] Task 3.4: Implement the SnapshotManager (baseline)

### Adapters (Tasks 11–13)
- [ ] Task 4.1: Implement the NpmAdapter
- [ ] Task 4.2: Implement the PipAdapter
- [ ] Task 4.3: Implement the WinGetAdapter / BrewAdapter

### PATH Validation (Tasks 14–16)
- [ ] Task 5.1: Implement the PathValidator
- [ ] Task 5.2: Create script generators
- [ ] Task 5.3: Expose PATH validation endpoints

### API Endpoints (Tasks 17–21)
- [ ] Task 6.1: Endpoint `/discover`
- [ ] Task 6.2: Endpoint `/managers`
- [ ] Task 6.3: Endpoint `/packages` (uninstall)
- [ ] Task 6.4: Endpoint `/path`
- [ ] Task 6.5: Endpoint `/snapshot`

### Frontend Core (Tasks 22–27)
- [ ] Task 7.1: Set up layout and routing
- [ ] Task 7.2: Build the Dashboard
- [ ] Task 7.3: Build the ManagerCard
- [ ] Task 7.4: Build the PackageTable
- [ ] Task 7.5: Build the ConfirmationModal
- [ ] Task 7.6: Build the PathSetupGuide

### Testing (Tasks 28–30)
- [ ] Task 8.1: ValidationLayer tests
- [ ] Task 8.2: LockManager tests
- [ ] Task 8.3: Adapter tests

**Additional required coverage checklist:**
- [ ] CommandExecutor — simulate timeouts, return failures, async execution
- [ ] OperationQueue — concurrency scenarios (read vs. mutation), lock/unlock
- [ ] NPM/Pip adapters — command mocks, output parsing, error regressions
- [ ] Critical endpoints — smoke tests for `/packages` (uninstall) and `/snapshot`

### Documentation (Tasks 31–33)
- [ ] Task 9.1: SECURITY.md
- [ ] Task 9.2: LIMITATIONS.md
- [ ] Task 9.3: SETUP_PATH.md

## ⏱️ Phase 1 Sprint Schedule (5 business days)

- **Day 1 – Preparation & Infrastructure:** create base directories, configure initial tooling (venv, npm, lint/test placeholders), prepare helper scripts under `scripts/setup/`, confirm `.gitignore` and `README.md` retain history.
- **Day 2 – Security Layer:** implement `ValidationLayer`, start `LockManager`, define test stubs with agreed coverage, document multi-platform compatibility notes.
- **Day 3 – Core Backend:** finish `LockManager`, develop `OperationQueue` with async tests, build `CommandExecutor` with timeout harness, start storage/snapshot abstractions.
- **Day 4 – API & Frontend MVP:** expose main endpoints (`/discover`, `/managers`, `/packages`, `/path`, `/snapshot`), build the React layout with core components and mocked states.
- **Day 5 – Quality & Documentation:** reinforce tests (CommandExecutor, OperationQueue, adapters), produce `SECURITY.md`, `LIMITATIONS.md`, `SETUP_PATH.md`, run manual smoke tests, and prepare the Phase 2 backlog.

---

## 🏗️ Detailed Task Breakdown

---

## SETUP & INFRASTRUCTURE

### Task 1.1: Create the Project Structure

**ID:** SETUP-001
**Priority:** CRITICAL
**Duration:** 30 minutes
**Dependencies:** None

**Description:**
Create the complete directory and file layout for the project.

> **Best practice:** whenever possible, wrap repeatable commands in scripts (`scripts/setup/`) to ensure reproducibility and avoid accidental overwrites.

**Note:** Work directly in the repository root (`Package_Audit_Dashboard/`)—do not create an additional nested directory with the same name.

**Structure to create:**
```
frontend/
├── src/
│   ├── components/
│   ├── hooks/
│   ├── store/
│   ├── types/
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── tsconfig.json
├── vite.config.ts
└── index.html

backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routers/
│   │   └── __init__.py
│   ├── adapters/
│   │   └── __init__.py
│   ├── analysis/
│   │   └── __init__.py
│   ├── core/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   └── storage/
│       └── __init__.py
├── tests/
│   └── __init__.py
├── requirements.txt
└── pyproject.toml

cli/
└── audit_cli/
    └── __init__.py

docs/
└── README.md

.gitignore
README.md
LICENSE
```

**Commands:**
```bash
# Create base structure (skip directories that already exist)
mkdir -p frontend/src/{components,hooks,store,types}
mkdir -p backend/app/{routers,adapters,analysis,core,models,storage}
mkdir -p backend/tests cli/audit_cli docs
```

---

### Task 1.2: Backend Setup (FastAPI)

**ID:** SETUP-002
**Priority:** HIGH
**Duration:** 1 day
**Dependencies:** Task 1.1

**Description:**
Initialize the FastAPI project with the core scaffolding, virtual environment, and lint/test tooling.

**Checklist:**
- [ ] Create `.venv` and install `fastapi`, `uvicorn`, `pydantic`
- [ ] Configure `requirements.txt` and `pyproject.toml`
- [ ] Add base FastAPI app in `app/main.py`
- [ ] Configure `app/routers/__init__.py`
- [ ] Set up `pytest` with sample test file
- [ ] Configure linting (`flake8`, `black`, `isort`, `mypy` optional)

**Commands:**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn pydantic
pip install pytest black flake8 mypy isort
pip freeze > requirements.txt
```

---

### Task 1.3: Frontend Setup (React + Vite)

**ID:** SETUP-003
**Priority:** HIGH
**Duration:** 1 day
**Dependencies:** Task 1.1

**Description:**
Initialize the React application using Vite with TypeScript support and baseline tooling.

**Checklist:**
- [ ] Create the project with Vite + React + TypeScript
- [ ] Install dependencies: `react-router-dom`, `@tanstack/react-query`, `zustand`, `axios`
- [ ] Configure `tailwindcss` + `postcss`
- [ ] Set up `tsconfig.json`, `vite.config.ts`
- [ ] Add initial layout scaffolding

**Commands:**
```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install
npm install @tanstack/react-query zustand axios react-router-dom
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

---

## SECURITY LAYER

### Task 2.1: ValidationLayer

**ID:** SEC-001
**Priority:** CRITICAL
**Duration:** 1 day
**Dependencies:** Task 1.2

**Description:**
Implement robust validation utilities to sanitize all inputs, protecting against command injection and path traversal.

**Acceptance Criteria:**
- [ ] Validation for package names (`^[a-zA-Z0-9@/_.-]+$`, max 256 chars)
- [ ] Validation for command arguments (whitelist per manager)
- [ ] Validation for filesystem paths (must stay inside `~/.package-audit/`)
- [ ] Custom exception hierarchy (`InvalidPackageNameError`, etc.)
- [ ] 100% unit test coverage in `backend/tests/test_validation.py`

---

### Task 2.2: LockManager

**ID:** SEC-002
**Priority:** CRITICAL
**Duration:** 1 day
**Dependencies:** Task 2.1

**Description:**
Create a locking system to prevent concurrent destructive operations.

**Acceptance Criteria:**
- [ ] File-based lock stored under `~/.package-audit/.lock`
- [ ] Timeout for acquisition (default 30s)
- [ ] Stale lock detection and cleanup (5 minutes)
- [ ] Signal handling for Linux/macOS; documented fallback for Windows
- [ ] Unit tests in `backend/tests/test_locking.py`

---

### Task 2.3: OperationQueue

**ID:** SEC-003
**Priority:** HIGH
**Duration:** 1 day
**Dependencies:** Task 2.2

**Description:**
Serialize mutations while allowing concurrent read operations.

**Acceptance Criteria:**
- [ ] Operation types: READ vs. MUTATION
- [ ] MUTATION acquires LockManager lock; READ shares locks safely
- [ ] Async-compatible (`asyncio` queue)
- [ ] Unit tests in `backend/tests/test_queue.py`

---

## CORE BACKEND

### Task 3.1: CommandExecutor

**ID:** CORE-001
**Priority:** HIGH
**Duration:** 1 day
**Dependencies:** Task 2.3

**Description:**
Secure subprocess execution utility shared by all adapters.

**Acceptance Criteria:**
- [ ] `run_sync` and `run_async` methods
- [ ] Timeout control (default 30s)
- [ ] No shell execution; list-based arguments only
- [ ] Captures stdout/stderr separately
- [ ] Unit tests in `backend/tests/test_executor.py`

---

### Task 3.2: JSON Storage

**ID:** CORE-002
**Priority:** MEDIUM
**Duration:** 1 day
**Dependencies:** Task 3.1

**Description:**
Provide atomic read/write wrappers for JSON files stored under `~/.package-audit/`.

**Acceptance Criteria:**
- [ ] Atomic writes (temp file + replace)
- [ ] Path validation via ValidationLayer
- [ ] Delete operations with safety checks
- [ ] Unit tests in `backend/tests/test_json_storage.py`

---

### Task 3.3: BaseAdapter Interface

**ID:** CORE-003
**Priority:** HIGH
**Duration:** 1 day
**Dependencies:** Task 3.2

**Description:**
Define a shared interface for package manager adapters with built-in validation hooks.

**Acceptance Criteria:**
- [ ] Abstract methods for detect/list/audit/uninstall/export
- [ ] Shared helpers for command execution and caching
- [ ] Unit tests in `backend/tests/test_base_adapter.py`

---

### Task 3.4: SnapshotManager (Baseline)

**ID:** CORE-004
**Priority:** HIGH
**Duration:** 1 day
**Dependencies:** Task 3.2

**Description:**
Implement snapshot storage for package states with automatic retention.

**Acceptance Criteria:**
- [ ] Create snapshot with metadata (timestamp, manager, package list)
- [ ] Retain last 10 snapshots per manager
- [ ] Delete oldest snapshots automatically
- [ ] Unit tests in `backend/tests/test_snapshot_manager.py`

---

## ADAPTERS

### Task 4.1: NpmAdapter

**ID:** ADAPT-001
**Priority:** HIGH
**Duration:** 1 day
**Dependencies:** Task 3.3

**Description:**
Adapter that wraps npm commands with CommandExecutor.

**Acceptance Criteria:**
- [ ] Detection via `npm --version`
- [ ] List packages using `npm list --json --depth=0`
- [ ] Uninstall with snapshot integration
- [ ] Manifest export
- [ ] Unit tests in `backend/tests/test_npm_adapter.py`

---

### Task 4.2: PipAdapter

**ID:** ADAPT-002
**Priority:** HIGH
**Duration:** 1 day
**Dependencies:** Task 4.1

**Description:**
Adapter that wraps pip commands with CommandExecutor.

**Acceptance Criteria:**
- [ ] Detection via `pip --version`
- [ ] List packages using `pip list --format=json`
- [ ] Uninstall with snapshot integration
- [ ] Manifest export
- [ ] Unit tests in `backend/tests/test_pip_adapter.py`

---

### Task 4.3: WinGetAdapter / BrewAdapter

**ID:** ADAPT-003
**Priority:** MEDIUM
**Duration:** 1 day
**Dependencies:** Task 4.2

**Description:**
Adapters for Windows (WinGet) and macOS (Homebrew) with platform-specific detection.

**Acceptance Criteria:**
- [ ] Detection via `winget --version` / `brew --version`
- [ ] Package listing commands per platform
- [ ] Uninstall operations with validation
- [ ] Unit tests in `backend/tests/test_winget_adapter.py` / `backend/tests/test_brew_adapter.py`

---

## PATH VALIDATION

### Task 5.1: PathValidator

**ID:** PATH-001
**Priority:** HIGH
**Duration:** 1 day
**Dependencies:** Task 3.2

**Description:**
Validate the PATH environment to ensure each package manager is reachable.

**Acceptance Criteria:**
- [ ] Detect missing binaries
- [ ] Suggest common install locations per platform
- [ ] Provide remediation advice
- [ ] Unit tests in `backend/tests/test_path_validator.py`

---

### Task 5.2: Script Generators

**ID:** PATH-002
**Priority:** MEDIUM
**Duration:** 1 day
**Dependencies:** Task 5.1

**Description:**
Generate shell scripts to fix PATH issues.

**Acceptance Criteria:**
- [ ] Support Bash/Zsh, PowerShell, Fish
- [ ] Provide manual execution instructions
- [ ] Validate output with unit tests

---

### Task 5.3: PATH Endpoints

**ID:** PATH-003
**Priority:** MEDIUM
**Duration:** 1 day
**Dependencies:** Task 5.2

**Description:**
Expose PATH validation and script generation through the API.

**Acceptance Criteria:**
- [ ] `GET /api/path/validate`
- [ ] `GET /api/path/generate-fix-script`
- [ ] Integration tests covering success and error cases

---

## API ENDPOINTS

### Task 6.1: `/discover`

**ID:** API-001
**Priority:** HIGH
**Duration:** 1 day
**Dependencies:** Tasks 4.x

**Description:**
Discover installed package managers using registered adapters.

**Acceptance Criteria:**
- [ ] Returns list of detected managers with version and capabilities
- [ ] Handles missing adapters gracefully
- [ ] Tests in `backend/tests/test_discover_router.py`

---

### Task 6.2: `/managers`

**ID:** API-002
**Priority:** HIGH
**Duration:** 1 day
**Dependencies:** Task 6.1

**Description:**
Expose manager metadata and available operations.

**Acceptance Criteria:**
- [ ] REST responses include capabilities, lock status, snapshot availability
- [ ] Cache basic info for faster repeat calls
- [ ] Tests in `backend/tests/test_managers_router.py`

---

### Task 6.3: `/packages`

**ID:** API-003
**Priority:** HIGH
**Duration:** 1 day
**Dependencies:** Task 6.2

**Description:**
List packages and perform uninstall operations.

**Acceptance Criteria:**
- [ ] `GET /api/managers/{id}/packages`
- [ ] `DELETE /api/managers/{id}/packages/{name}` with snapshot + queue integration
- [ ] Tests in `backend/tests/test_packages_router.py`

---

### Task 6.4: `/path`

**ID:** API-004
**Priority:** MEDIUM
**Duration:** 1 day
**Dependencies:** Task 5.3

**Description:**
Expose PATH diagnostics and remediation scripts.

**Acceptance Criteria:**
- [ ] `GET /api/path/validate`
- [ ] `GET /api/path/generate-fix-script?shell=`
- [ ] Tests in `backend/tests/test_path_router.py`

---

### Task 6.5: `/snapshot`

**ID:** API-005
**Priority:** MEDIUM
**Duration:** 1 day
**Dependencies:** Task 3.4

**Description:**
Manage snapshots through REST endpoints.

**Acceptance Criteria:**
- [ ] `POST /api/snapshot/create`
- [ ] `GET /api/snapshot/list`
- [ ] `POST /api/snapshot/restore/{id}`
- [ ] Tests in `backend/tests/test_snapshot_router.py`

---

## FRONTEND CORE

### Task 7.1: Layout & Routing

**ID:** FE-001
**Priority:** HIGH
**Duration:** 1 day
**Dependencies:** Task 1.3

**Description:**
Set up base layout, navigation, and routing.

**Acceptance Criteria:**
- [ ] Main layout with sidebar/header
- [ ] Routes: Dashboard, Managers, Snapshots, Settings
- [ ] Loading/skeleton states

---

### Task 7.2: Dashboard Component

**ID:** FE-002
**Priority:** HIGH
**Duration:** 1 day
**Dependencies:** Task 7.1

**Description:**
Top-level summary view with per-manager cards and quick actions.

**Acceptance Criteria:**
- [ ] Displays manager status, package counts, health indicators
- [ ] Links to detailed manager view
- [ ] Tests (component + integration)

---

### Task 7.3: ManagerCard Component

**ID:** FE-003
**Priority:** HIGH
**Duration:** 1 day
**Dependencies:** Task 7.2

**Description:**
Detailed card for each manager with key metrics and actions.

**Acceptance Criteria:**
- [ ] Shows version, detected status, capabilities
- [ ] Buttons for list/audit/uninstall/help
- [ ] Handles loading/error/empty states

---

### Task 7.4: PackageTable Component

**ID:** FE-004
**Priority:** HIGH
**Duration:** 1 day
**Dependencies:** Task 7.3

**Description:**
Table view with package name, version, usage info, and actions.

**Acceptance Criteria:**
- [ ] Sorting, filtering, pagination
- [ ] Action column with uninstall + confirm modal
- [ ] Loading skeletons and error handling

---

### Task 7.5: ConfirmationModal Component

**ID:** FE-005
**Priority:** MEDIUM
**Duration:** 1 day
**Dependencies:** Task 7.4

**Description:**
Modal dialog for destructive actions (uninstall, snapshot delete).

**Acceptance Criteria:**
- [ ] Warning copy with usage info
- [ ] Force checkbox when required
- [ ] Accessible keyboard navigation

---

### Task 7.6: PathSetupGuide Component

**ID:** FE-006
**Priority:** MEDIUM
**Duration:** 1 day
**Dependencies:** Task 7.1

**Description:**
Display generated PATH scripts with copy/download options.

**Acceptance Criteria:**
- [ ] Shows scripts per shell (bash, zsh, PowerShell, fish)
- [ ] Copy-to-clipboard and download buttons
- [ ] Highlights manual steps and post-check instructions

---

## TESTING

### Task 8.1: ValidationLayer Tests

**ID:** TEST-001
**Priority:** CRITICAL
**Duration:** 1 day
**Dependencies:** Task 2.1

**Description:**
Unit tests covering all validation scenarios.

**Acceptance Criteria:**
- [ ] Valid/invalid package names
- [ ] Command whitelist enforcement
- [ ] Path traversal detection

---

### Task 8.2: LockManager Tests

**ID:** TEST-002
**Priority:** CRITICAL
**Duration:** 1 day
**Dependencies:** Task 2.2

**Description:**
Test lock acquisition, release, timeouts, and stale cleanup.

**Acceptance Criteria:**
- [ ] Acquire/release cycle
- [ ] Timeout scenarios
- [ ] Force release behaviour

---

### Task 8.3: Adapter Tests

**ID:** TEST-003
**Priority:** HIGH
**Duration:** 1 day
**Dependencies:** Tasks 4.x

**Description:**
Ensure each adapter handles command output, errors, and validation.

**Acceptance Criteria:**
- [ ] Command mocks for success/failure
- [ ] Parsing of command output
- [ ] Error handling with ValidationLayer integration

---

## DOCUMENTATION

### Task 9.1: SECURITY.md

**ID:** DOC-001
**Priority:** HIGH
**Duration:** 0.5 day
**Dependencies:** Phase 1 completion

**Description:**
Document the security architecture (ValidationLayer, LockManager, OperationQueue, CommandExecutor).

---

### Task 9.2: LIMITATIONS.md

**ID:** DOC-002
**Priority:** MEDIUM
**Duration:** 0.5 day
**Dependencies:** Phase 1 completion

**Description:**
Document known limitations and planned workarounds.

---

### Task 9.3: SETUP_PATH.md

**ID:** DOC-003
**Priority:** MEDIUM
**Duration:** 0.5 day
**Dependencies:** PATH subsystem

**Description:**
Document PATH diagnostics, scripts, and troubleshooting tips.

---

## ✔️ Acceptance Criteria for Phase 1 MVP

1. Dashboard lists installed packages and managers.
2. Uninstall flow captures snapshots, validates PATH, and prevents concurrent mutations.
3. Security layer covers validation, locking, and queued execution with full unit tests.
4. CLI supports discover/list/uninstall commands and mirrors API safeguards.
5. Documentation is complete (`README.md`, `SECURITY.md`, `LIMITATIONS.md`, `SETUP_PATH.md`).
6. Manual smoke tests executed with results recorded in `LOG.md`.
