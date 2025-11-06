# 📋 Package Audit Dashboard – Final Blueprint v3.0

## 🎯 Project Overview

**Goal:** Deliver a local web dashboard (with CLI companion and automation-ready APIs) that audits, manages, and maintains package managers installed on the system with security-by-design guarantees.

**Context:** Personal productivity, open-source showcase, and technical portfolio piece.

**Confidence Level:** 0.90/1.0 after multi-dimensional validation.

---

## 🏗️ Technology Stack

### Frontend
- **React 18** + **TypeScript**
- **Vite** for bundling
- **TailwindCSS** + **shadcn/ui** for styling
- **TanStack Query** for async state
- **Zustand** for global state

### Backend
- **FastAPI** (async Python)
- **Uvicorn** (ASGI server)
- **Pydantic** (data validation)

### Storage
- **JSON files** under `~/.package-audit/`
- TTL-based cache
- Snapshots compressed with gzip

### CLI
- **Typer** (CLI framework)
- **Rich** (formatted output)

### Supported Package Managers
```
Node.js:     npm, pnpm, yarn, bun, nvm
Python:      pip, pipx, uv, conda, poetry
System:      winget, choco, scoop (Windows)
             brew (macOS)
             apt, snap, flatpak (Linux)
Dev Tools:   cargo, go, gem, composer
Others:      asdf, mise, volta
```

---

## 🧱 End-to-End Architecture

```
┌─────────────────────────────────────────────┐
│          React Dashboard (UI)               │
│  ├─ Global View (cards per manager)         │
│  ├─ Manager Detail (tables, actions)        │
│  ├─ Logs Viewer (SSE stream)                │
│  ├─ Usage Warning Panel (high risk alerts)  │
│  ├─ Help Browser (contextual docs)          │
│  └─ Settings (paths, schedules, options)    │
└──────────────────┬──────────────────────────┘
                   │ HTTP/REST + SSE
┌──────────────────▼──────────────────────────┐
│            FastAPI Backend                  │
│  ├─ /api/discover                           │
│  ├─ /api/managers/{id}/{action}             │
│  │   Actions: list, audit, update,          │
│  │            uninstall, help               │
│  ├─ /api/packages/{name}/usage              │
│  ├─ /api/manifest/export                    │
│  ├─ /api/path/validate                      │
│  ├─ /api/path/generate-fix-script           │
│  ├─ /api/snapshot/{action}                  │
│  └─ /api/logs/stream (SSE)                  │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│        Plugin System (Adapters)             │
│  ├─ BaseManagerAdapter (interface)          │
│  │   Methods:                               │
│  │   - detect() -> bool                     │
│  │   - get_version() -> str                 │
│  │   - list_packages() -> List[Package]     │
│  │   - audit() -> List[Vulnerability]       │
│  │   - update(package) -> Result            │
│  │   - uninstall(package) -> Result         │
│  │   - get_help() -> HelpInfo               │
│  │   - get_package_info() -> Metadata       │
│  │   - export_manifest() -> dict            │
│  └─ Adapters: npm, pip, cargo, etc.         │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│      Analysis & Context Layer               │
│  ├─ UsageAnalyzer (scan manifests)          │
│  ├─ DescriptionFetcher (metadata + cache)   │
│  ├─ TagGenerator (auto + user tags)         │
│  └─ SnapshotManager (backup + restore)      │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│         Execution Layer (CRITICAL)          │
│  ├─ ValidationLayer                         │
│  │   ├─ InputSanitizer (regex whitelist)    │
│  │   ├─ CommandValidator (prevent injection)│
│  │   └─ PathValidator (prevent traversal)   │
│  ├─ LockManager (race-condition prevention) │
│  ├─ OperationQueue (serial mutations)       │
│  ├─ CommandExecutor (safe subprocess calls) │
│  └─ ErrorHandler (graceful fallback)        │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│      Storage Layer                          │
│  ├─ config.json (settings + paths)          │
│  ├─ cache.json (descriptions, TTL 7d)       │
│  ├─ .lock (operation locking)               │
│  ├─ manifests/ (timestamped exports)        │
│  ├─ snapshots/ (packages + lockfiles)       │
│  └─ logs/ (audit trail)                     │
└─────────────────────────────────────────────┘
```

---

## 📁 Repository Layout (Reference)

```
package-audit-dashboard/
├── frontend/                          # React app
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.tsx          # Global view
│   │   │   ├── ManagerCard.tsx        # Per-manager card
│   │   │   ├── PackageTable.tsx       # Package table
│   │   │   ├── UsageWarningPanel.tsx  # Usage alerts
│   │   │   ├── HelpBrowser.tsx        # Contextual docs
│   │   │   ├── PathSetupGuide.tsx     # PATH script helper
│   │   │   ├── LogViewer.tsx          # Streaming logs
│   │   │   ├── SnapshotManager.tsx    # Snapshot control
│   │   │   └── ConfirmationModal.tsx  # Destructive actions
│   │   ├── hooks/
│   │   │   ├── useManagers.ts         # TanStack Query hooks
│   │   │   ├── usePackageUsage.ts     # Usage lookups
│   │   │   ├── useStreamLogs.ts       # SSE connection
│   │   │   └── useLockStatus.ts       # Lock state
│   │   ├── store/
│   │   │   └── appStore.ts            # Zustand store
│   │   ├── types/
│   │   │   └── api.ts                 # API interfaces
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                           # FastAPI service
│   ├── app/
│   │   ├── main.py                    # FastAPI app
│   │   ├── routers/
│   │   │   ├── discovery.py           # System scan
│   │   │   ├── managers.py            # Manager actions
│   │   │   ├── packages.py            # Package operations
│   │   │   ├── manifest.py            # Export/compare
│   │   │   ├── path.py                # PATH validation
│   │   │   ├── snapshot.py            # Snapshot lifecycle
│   │   │   └── logs.py                # Log streaming
│   │   ├── adapters/
│   │   │   ├── base.py                # BaseAdapter
│   │   │   ├── npm.py                 # npm adapter
│   │   │   ├── pip.py                 # pip adapter
│   │   │   ├── cargo.py               # cargo adapter
│   │   │   ├── winget.py              # WinGet adapter
│   │   │   ├── brew.py                # Homebrew adapter
│   │   │   └── __init__.py            # Auto-discovery
│   │   ├── analysis/
│   │   │   ├── usage_analyzer.py      # Project scans
│   │   │   ├── description_fetcher.py # Metadata fetch
│   │   │   ├── tag_generator.py       # Auto tagging
│   │   │   └── snapshot_manager.py    # Backup/restore
│   │   ├── core/
│   │   │   ├── validation.py          # ValidationLayer
│   │   │   ├── locking.py             # LockManager
│   │   │   ├── queue.py               # OperationQueue
│   │   │   ├── executor.py            # CommandExecutor
│   │   │   └── errors.py              # Custom exceptions
│   │   ├── models/
│   │   │   └── schemas.py             # Pydantic models
│   │   └── storage/
│   │       ├── json_store.py          # JSON persistence
│   │       └── cache.py               # Cache management
│   ├── tests/
│   │   ├── test_validation.py         # Security tests
│   │   ├── test_locking.py            # Concurrency tests
│   │   └── test_adapters.py           # Adapter tests
│   ├── requirements.txt
│   └── pyproject.toml
│
├── cli/                               # CLI companion
│   ├── audit_cli/
│   │   ├── __main__.py                # Entry point
│   │   ├── commands/
│   │   │   ├── scan.py                # Scan managers
│   │   │   ├── list.py                # List packages
│   │   │   ├── audit.py               # Security audit
│   │   │   ├── update.py              # Update packages
│   │   │   ├── uninstall.py           # Uninstall
│   │   │   ├── usage.py               # Usage checks
│   │   │   ├── help.py                # Show help
│   │   │   ├── export.py              # Export manifest
│   │   │   ├── compare.py             # Compare manifests
│   │   │   ├── snapshot.py            # Snapshot ops
│   │   │   └── fix_path.py            # PATH helper
│   │   ├── formatters/
│   │   │   ├── json.py                # JSON output
│   │   │   ├── table.py               # Rich tables
│   │   │   ├── csv.py                 # CSV output
│   │   │   └── yaml.py                # YAML output
│   │   └── client.py                  # HTTP client
│   ├── pyproject.toml
│   └── README.md
│
├── shared/                            # Shared schemas
│   ├── schemas/
│   │   ├── manifest_v1.json           # Schema v1
│   │   ├── manifest_v2.json           # Schema v2
│   │   └── migrations.py              # Schema migrations
│   └── __init__.py
│
├── docs/                              # Documentation
│   ├── ARCHITECTURE.md                # Technical decisions
│   ├── API.md                         # API reference
│   ├── SECURITY.md                    # Security policy
│   ├── LIMITATIONS.md                 # Known limitations
│   ├── SETUP_PATH.md                  # PATH guides
│   ├── TROUBLESHOOTING.md             # Common issues
│   ├── PLUGINS.md                     # Adapter creation
│   └── CLI.md                         # CLI reference
│
├── .github/
│   └── workflows/
│       ├── ci.yml                     # Lint + test
│       └── release.yml                # Build + publish
│
├── docker-compose.yml                 # Development stack
├── README.md
└── LICENSE
```

---

## 🎯 Detailed Roadmap

### **Phase 1: Secure MVP (Week 1–2)** — ⚡ Highest Priority

#### Objectives
- Working dashboard with core operations
- Security-first mindset (command injection, race conditions)
- PATH validation with generated scripts
- Automatic snapshots before destructive actions

#### Backend Core & Security (Critical)

**ValidationLayer (mandatory)**
- Input sanitization: `^[a-zA-Z0-9@/_.-]+$`
- Prevent command injection by using argument arrays only
- Path traversal validation
- Unit tests with full coverage

**LockManager (mandatory)**
- Lock file at `~/.package-audit/.lock`
- Timeout: 30 seconds
- Automatic cleanup after crashes
- Stale lock detection

**OperationQueue**
- Serialize mutations
- Allow concurrent read-only operations
- Cancel pending jobs when required

**BaseManagerAdapter interface**
```python
class BaseManagerAdapter(ABC):
    @abstractmethod
    def detect() -> bool:
        ...

    @abstractmethod
    def get_version() -> str:
        ...

    @abstractmethod
    def list_packages() -> List[Package]:
        ...

    @abstractmethod
    def uninstall(package: str, force: bool) -> Result:
        ...

    @abstractmethod
    def export_manifest() -> dict:
        ...
```

**Priority adapters**
- NpmAdapter (proof of concept)
- PipAdapter
- WinGetAdapter (Windows) / BrewAdapter (macOS)

**Phase 1 endpoints**
- `POST /api/discover` — scan the system
- `GET /api/managers` — list detected managers
- `GET /api/managers/{id}/list` — list packages
- `DELETE /api/managers/{id}/packages/{name}` — uninstall
- `GET /api/path/validate` — check PATH
- `GET /api/path/generate-fix-script` — produce shell script
- `POST /api/snapshot/create` — create snapshot
- `POST /api/snapshot/restore/{id}` — restore snapshot

**CommandExecutor**
```python
# ✅ Always do this
subprocess.run(["npm", "uninstall", validated_package],
               capture_output=True,
               timeout=30)

# ❌ Never do this
subprocess.run(f"npm uninstall {package}")
```

#### PATH Validation (Updated)

**PathValidator**
- Detect missing paths per manager
- Scan common locations (per platform)
- Generate fix scripts (bash/PowerShell/fish)
- Validate PATH after user action

**Endpoints**
- `GET /api/path/validate` → `{ "missing": [...], "suggestions": [...] }`
- `GET /api/path/generate-fix-script?shell=bash` → script body

**No automatic fixes**
- The user runs scripts manually
- Dashboard validates once applied

#### Snapshot System (Baseline)

**SnapshotManager v1**
- Stores package names and versions
- Auto-snapshot before uninstall/update
- Retains the last 10 snapshots
- Lockfiles deferred to Phase 2

**Endpoints**
- `POST /api/snapshot/create`
- `GET /api/snapshot/list`
- `POST /api/snapshot/restore/{id}`

#### Frontend Foundation

**Components**
- `Dashboard.tsx` — grid of cards
- `ManagerCard.tsx` — status and basic actions
- `PackageTable.tsx` — listing and uninstall
- `ConfirmationModal.tsx` — confirm destructive actions
- `PathSetupGuide.tsx` — display scripts
- `LoadingState.tsx` — during operations

**Hooks**
- `useManagers()` — TanStack Query integration
- `useLockStatus()` — lock monitoring
- `usePathValidation()` — PATH status

**UX features**
- Loading states while operations run
- Disable actions when resources are locked
- Retry-friendly error handling
- Toast notifications for success/failure

#### JSON Storage

**`~/.package-audit/` layout**
```
.package-audit/
├── config.json          # User settings
├── cache.json           # Temporary data
├── .lock                # Operation lock
├── snapshots/           # Backups
│   ├── snapshot_20251102_153045.json.gz
│   └── ...
└── logs/                # Audit trail
    └── operations.log
```

#### Phase 1 Deliverables
- ✅ Functional dashboard
- ✅ Package listing for detected managers
- ✅ Uninstall flow with confirmation
- ✅ PATH validation + script generation
- ✅ Automatic snapshot before uninstall
- ✅ Protection against command injection and race conditions

---

### **Phase 2: Context & Intelligence (Week 3–4)**

#### Usage Analysis (with high-visibility warnings)

**UsageAnalyzer**
- Scan configurable project directories
- Parse manifests: `package.json`, `requirements.txt`, `Cargo.toml`, etc.
- Build usage map `{package: [projects]}`
- Cache results with invalidation on change

**Integration workflow**
```python
def uninstall_package(manager, package, force=False):
    usage = usage_analyzer.get_usage(package)

    if usage and not force:
        raise PackageInUseError(
            package=package,
            projects=usage,
            can_force=True,
        )

    snapshot_manager.create_snapshot()
    result = adapter.uninstall(package)
    return result
```

**Endpoints**
- `GET /api/packages/{name}/usage` → `{ "used_in": [...], "safe_to_remove": bool }`
- `POST /api/config/project-directories` → configure search paths

**UI components**
- `UsageWarningPanel.tsx` — prominent warning banner
- Disclaimer: manifest-based detection only
- Force checkbox: "I understand the risks"

**Disclaimer template**
```
⚠️ This package appears in 3 projects

Warning: Detection is based on manifest files only. This does not
guarantee the package isn't used elsewhere (dynamic imports,
runtime dependencies, etc.). Test thoroughly after uninstalling.

☐ I understand the risks and want to proceed
```

#### Snapshot System (Full)

- Include lockfiles (`package-lock.json`, `requirements.txt`, etc.)
- Capture environment metadata (OS, manager versions)
- Add restore preview: diff before applying

#### Vulnerability Scanning

- `npm audit --json`
- `pip-audit --format=json`
- Normalize severity levels (info/warn/critical)
- Store results per package and version
- UI component: `VulnerabilityScan.tsx`

#### Dependency Tree Visualization

- `npm list --json`
- `pipdeptree --json`
- Fallback to `pip show` if pipdeptree missing
- Render tree with collapsible nodes
- Allow export as JSON

#### Batch Operations

- Batch uninstall with optional dry run
- Automatic snapshot before execution
- Return per-package status (success/failure, logs)

#### Automatic Rollback

- `SnapshotManager.restore()` handles file cleanup
- Remove packages not present in the snapshot
- Rollback command exposed via CLI and UI

#### Help System

```python
def get_help(self) -> HelpInfo:
    version = self.get_version()

    if version.startswith("10."):
        return NPM_V10_HELP
    if version.startswith("9."):
        return NPM_V9_HELP

    return HelpInfo(
        docs_url="https://docs.npmjs.com",
        commands=[...],
    )
```

- Endpoint: `GET /api/managers/{id}/help`
- UI: `HelpBrowser.tsx` with searchable command list
- Cache entries per `{manager}:{version}` (TTL 30 days)

#### Phase 2 Deliverables
- ✅ Usage analysis with warnings
- ✅ Full snapshots (lockfiles + metadata)
- ✅ Security audit integration
- ✅ Health scoring for managers
- ✅ Help system with version awareness
- ✅ Conflict detection across managers

---

### **Phase 3: Enrichment (Week 5)**

#### Description & Metadata Fetching

**DescriptionFetcher**
- Rate limits: 10 req/s (crates.io), 50 req/min (PyPI)
- Exponential backoff with retries
- Timeout: 5 seconds per request
- Graceful degradation on failure

```python
class DescriptionFetcher:
    def fetch_batch(self, packages: List[str]) -> Dict[str, Metadata]:
        results = {}
        for package in packages:
            if cached := cache.get(f"desc:{package}"):
                results[package] = cached
                continue

            try:
                metadata = self._fetch_with_retry(package)
                cache.set(f"desc:{package}", metadata, ttl=7 * 24 * 3600)
                results[package] = metadata
            except RateLimitError:
                results[package] = None
        return results
```

**Progress tracking**
```
Fetching descriptions... [████░░░░] 45/120 (37%)
Rate limited, waiting 2s...
Completed: 115/120 (5 failed)
```

**Endpoint**
- `GET /api/packages/enrich?with_descriptions=true`

**Cache**
- File: `descriptions_cache.json`
- TTL: 7 days
- Structure: `{package: {description, keywords, homepage, fetched_at}}`

#### Tag System (Dual source)

**Automatic tags**
- `outdated`, `vulnerable`, `in-use`, `orphan`
- `conflict` (detected across multiple managers)

**Generated tags from metadata**
- `javascript`, `python`, `rust` (language)
- `cli-tool`, `framework`, `library` (type)
- Derived from keywords, names, and descriptions

**User-defined tags**
- Custom labels: `critical`, `prod-only`, `can-remove`
- Persist per package

**TagGenerator**
```python
class TagGenerator:
    def classify(self, package: Package, metadata: Metadata) -> List[str]:
        tags: List[str] = []

        if "cli" in metadata.keywords:
            tags.append("cli-tool")
        if package.name.endswith("-cli"):
            tags.append("cli-tool")
        if "framework" in metadata.description.lower():
            tags.append("framework")
        return tags
```

**Schema integration**
```json
{
  "id": "pkg:npm:react",
  "name": "react",
  "manager": "npm",
  "version": "18.3.1",
  "tags": ["javascript", "framework", "in-use"],
  "metadata": {
    "homepage": "https://react.dev",
    "description": "React is a JavaScript library for building user interfaces.",
    "keywords": ["ui", "library", "javascript"],
    "fetched_at": "2025-11-05T12:30:00Z"
  }
}
```

#### Analytics Dashboard

- Health score per manager (availability + vulnerabilities + stale packages)
- Highlight top risky packages
- Trend lines for installs/uninstalls
- Exportable reports (CSV/JSON)

---

## 🔧 Automation & Tooling

### CLI Enhancements
- Interactive prompts for uninstall confirmation
- Batch selection with fuzzy search
- Manifest comparison (`compare-manifest` command)
- Snapshot restore from CLI
- JSON/YAML/CSV output switches

### API Client
- Shared `client.py` for CLI and automations
- Retries with exponential backoff
- Typed responses via Pydantic models

### Scripting Hooks
- `scripts/quick_setup.py` — bootstrap environments
- `scripts/chroma_sync.py` — sync operational memory (ChromaDB)
- CI helpers for smoke tests

---

## ✅ Non-Negotiable Quality Gates

1. **Security first** — ValidationLayer, LockManager, and OperationQueue must guard every destructive command.
2. **Test coverage** — Critical modules require explicit unit tests before merging.
3. **Manual review** — Dangerous operations (uninstall, rollback) always require explicit confirmation or a `--force` flag.
4. **Graceful degradation** — Optional dependencies (pip-audit, pipdeptree) must fail softly with actionable messaging.
5. **Observability** — Structured logging for every significant backend action and CLI command.

---

## 🧭 Next Steps Summary

1. Finalize Phase 1 security components and confirm cross-platform behaviour (Linux/macOS/Windows).
2. Deliver Phase 1 UI/UX polish and smoke-test the uninstall flow end to end.
3. Move into Phase 2 analytics (usage detection, vulnerability scanning, dependency trees).
4. Layer Phase 3 enrichment features (metadata, tags, analytics) once stability and coverage goals are met.
5. Document every architectural decision in `/docs/ARCHITECTURE.md` and keep the operational log (`LOG.md`) up to date.
