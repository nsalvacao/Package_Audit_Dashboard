# Operational Log

## 2025-11-03

### Context
- Initial Phase 1 review to align the secure MVP with the actual repository structure.

### Actions
- Updated `FASE1_BREAKDOWN.md` to remove redundant nested directories and reinforce merge practices for `.gitignore` / `README.md`.
- Added a critical testing checklist (CommandExecutor, OperationQueue, adapters, endpoints) and a five-block timeline.
- Documented guidance on LockManager compatibility with signals on Windows/macOS and the creation of helper scripts under `scripts/setup/`.
- Started Phase A by creating the base structure (`frontend/`, `backend/`, `cli/`, `docs/`) and the required `__init__.py` files.
- Consolidated `.gitignore` with standard Python/Node/IDE entries while keeping local notes.
- Implemented `scripts/setup/bootstrap_structure.py` to automate structure creation and `__init__.py` scaffolding.
- Developed `ValidationLayer` (SEC-001) with specialized exceptions plus validation for names, commands, and paths.
- Created unit tests `backend/tests/test_validation.py` with full coverage and fixtures that isolate the allowed directory.
- Configured a local `.venv` and installed `pytest` to run the suite in a controlled environment.
- Implemented `LockManager` (SEC-002) with stale-lock detection, automatic cleanup, and tolerance for platforms without signal support.
- Added tests `backend/tests/test_locking.py` covering acquisition, stale detection, waiting, and forced release.
- Built `OperationQueue` (SEC-003) supporting concurrent READ operations and serialized MUTATION operations via `LockManager`.
- Wrote async tests `backend/tests/test_queue.py` covering concurrency, blocking, error propagation, and singleton behaviour.
- Installed `pytest-asyncio` inside the `.venv` to support async suites.
- Developed `CommandExecutor` (CORE-001) with safe synchronous/asynchronous execution, logging, and configurable timeouts.
- Added tests `backend/tests/test_executor.py` covering success, failure, timeout, and type validation (including async variants).
- Implemented `JSONStorage` (CORE-002) with atomic writes, safe path resolution, and integration under `.package-audit/storage`.
- Created tests `backend/tests/test_json_storage.py` validating read, write, delete, traversal prevention, and file consistency.
- Implemented `BaseAdapter` (CORE-003) consolidating detection, command execution, and shared caching across managers.
- Added tests `backend/tests/test_base_adapter.py` to verify detection, version retrieval, sanitization, and caching.
- Implemented `SnapshotManager` (CORE-004) with automatic retention (10 items) and metadata storage.
- Added tests `backend/tests/test_snapshot_manager.py` for persistence, ordering, retention, and manager validation.
- Implemented `NpmAdapter` (Task 4.1) using `BaseAdapter` patterns for command execution and sanitization.
- Added tests `backend/tests/test_npm_adapter.py` covering listing, uninstall (with/without `--force`), manifest export, and invalid names.
- Implemented `PipAdapter` (Task 4.2) with `pip list --format=json`, automated uninstall, and manifest export.
- Added tests `backend/tests/test_pip_adapter.py` covering parsing, fallback behaviour, uninstall execution, and name validation.
- Implemented `WinGetAdapter` and `BrewAdapter` (Task 4.3) following the BaseAdapter + CommandExecutor approach.
- Added tests `backend/tests/test_winget_adapter.py` and `backend/tests/test_brew_adapter.py` covering parsing, command invocation (force), and validation.
- Built the `/api/discover` router with adapter-based detection.
- Added tests `backend/tests/test_discover_router.py` ensuring coverage of versions and simulated detections.
- Built the `/api/managers` router with enriched capabilities for each detected manager.
- Added tests `backend/tests/test_managers_router.py` covering behaviour with and without available managers.
- Prepared the environment for ChromaDB synchronization (basic install, `data/chromadb/` directory, and `scripts/chroma_sync.py`).
- Added `data/` to `.gitignore` and created a sync helper that warns about additional dependencies (`tokenizers`, `onnxruntime`, `duckdb`).
- Installed complementary dependencies (`tokenizers`, `onnxruntime`, `duckdb`, `opentelemetry-*`, `importlib-resources`, `typer`, `bcrypt`, `chroma-hnswlib`, `kubernetes`, `grpcio`) and performed an initial sync of `LOG.md` into `data/chromadb/`, confirming persistence.
- Built the `/api/managers/{id}/packages/{name}` router for uninstall operations with automatic snapshots.
- Added tests `backend/tests/test_packages_router.py` with queue/snapshot stubs and error verification.

### Tests
- `python3 scripts/setup/bootstrap_structure.py --dry-run`
- `python3 scripts/setup/bootstrap_structure.py`
- `.venv/bin/python -m pytest backend/tests/test_validation.py -v`
- `.venv/bin/python -m pytest backend/tests/test_locking.py -v`
- `.venv/bin/python -m pytest backend/tests/test_queue.py -v`
- `.venv/bin/python -m pytest backend/tests/test_executor.py -v`
- `.venv/bin/python -m pytest backend/tests/test_json_storage.py -v`
- `.venv/bin/python -m pytest backend/tests/test_base_adapter.py -v`
- `.venv/bin/python -m pytest backend/tests/test_snapshot_manager.py -v`
- `.venv/bin/python -m pytest backend/tests/test_npm_adapter.py -v`
- `.venv/bin/python -m pytest backend/tests/test_pip_adapter.py -v`
- `.venv/bin/python -m pytest backend/tests/test_winget_adapter.py backend/tests/test_brew_adapter.py -v`
- `.venv/bin/python -m pytest backend/tests/test_discover_router.py -v`
- `.venv/bin/python -m pytest backend/tests/test_managers_router.py -v`
- `.venv/bin/python -m pytest backend/tests/test_packages_router.py -v`

### Decisions
- Keep the existing `.gitignore` and `README.md`, merging changes via append-only updates.
- Ensure each critical module has acceptance criteria backed by explicit test coverage.
- Record relevant progress in this `LOG.md` and persist notable runs into ChromaDB during the next session.
- Validate LockManager signal handlers on Windows/macOS before closing SEC-002 and document the fallback strategy.
- Plan manual smoke tests for `OperationQueue` in a real environment after endpoint integration.
- Capture commands via `sys.executable` in CommandExecutor tests to guarantee cross-platform portability.
- Reinforce using `JSONStorage` for all persistent JSON operations.
- Ensure every concrete adapter inherits from `BaseAdapter` to guarantee consistent sanitization and atomic writes.
- SnapshotManager keeps a configurable retention limit; consider user-configurable settings later.
- For uninstall operations, create a snapshot via `SnapshotManager` before invoking adapters (to be implemented in routers).
- Evaluate reusing adapter-generated manifests in `/snapshot` and `/managers` endpoints.
- On multi-OS environments, dynamically select available adapters (WinGet vs. Brew) at runtime.
- As new endpoints are added, create shared FastAPI fixtures to reduce duplication across test suites.

### Next Steps
- Start implementing backend endpoints (Task 6.x) using adapters and `OperationQueue`.
- Define integration test suites for routers (`/discover`, `/managers`, `/packages`, `/snapshot`).
- Validate LockManager on Windows/macOS before closing SEC-002 and document the fallback.
- Populate ChromaDB with this log and related decisions once the memory pipeline is operational (tooling pending).
