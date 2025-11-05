# Package Audit Dashboard CLI

Command-line interface for managing package managers.

## Installation

```bash
# From project root
cd backend
source .venv/bin/activate
pip install -e ../cli
```

## Usage

```bash
# Discover package managers
python -m cli.audit_cli discover

# List packages
python -m cli.audit_cli list-packages npm
python -m cli.audit_cli list-packages pip

# Uninstall a package
python -m cli.audit_cli uninstall npm lodash
python -m cli.audit_cli uninstall pip requests --force

# Check version
python -m cli.audit_cli version

# System status
python -m cli.audit_cli status

# Help
python -m cli.audit_cli --help
```

## Commands

### `discover`
Discovers installed package managers on the system.

### `list-packages <manager>`
Lists all packages installed by a specific manager.

### `uninstall <manager> <package>`
Uninstalls a package (with confirmation prompt).

Options:
- `--force, -f`: Force uninstall without dependency checks

### `version`
Shows CLI version information.

### `status`
Shows system status and health check.

## Examples

```bash
# Discover managers
$ python -m cli.audit_cli discover

🔍 Discovering package managers...

┌─────────────────────────────────┐
│ Detected Package Managers      │
├────────┬──────┬──────────┬──────┤
│ ID     │ Name │ Version  │ Status│
├────────┼──────┼──────────┼──────┤
│ npm    │ npm  │ 10.2.4   │ ✓    │
│ pip    │ pip  │ 23.3.1   │ ✓    │
└────────┴──────┴──────────┴──────┘

✓ Found 2 package manager(s)
```

## Phase 1 Limitations

- No batch operations
- No snapshot management via CLI (use backend API)
- No real-time progress indicators
- No colored output on some terminals

## Future Features (Phase 2)

- Interactive package selection
- Batch uninstall
- Snapshot restore
- Export manifests
- Vulnerability scanning
- Update all packages
