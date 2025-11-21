# ⚠️ Known Limitations

## Overview

This document outlines the known limitations of the Package Audit Dashboard MVP (Phase 1). These are either by design (to keep scope manageable) or planned for future releases.

---

## 🔴 Critical Limitations

### 1. No Automatic Rollback on Failure

**Issue**: If package uninstall fails mid-operation, automatic rollback is not implemented.

**Impact**: System may be left in inconsistent state.

**Workaround**: Manual snapshot restoration via:
```bash
# Manual restore process (Phase 2)
# 1. Check snapshots
ls ~/.package-audit/snapshots/

# 2. Review snapshot metadata
cat ~/.package-audit/snapshots/snapshot-abc123.json

# 3. Manual package reinstall
npm install [package]@[version]
```

**Planned**: Phase 2 (Automatic rollback with `SnapshotManager.restore()`)

---

### 2. Single-User Only

**Issue**: No multi-user support or permission management.

**Impact**: All users on the system share the same `~/.package-audit/` directory.

**Workaround**: None (by design for MVP).

**Planned**: Phase 3 (Multi-user support with user isolation)

---

### 3. No Network Error Handling

**Issue**: Package manager operations that require network access can fail without retry logic.

**Impact**: Transient network failures cause operation failures.

**Workaround**: Manually retry operations.

**Planned**: Phase 2 (Exponential backoff retry logic)

---

## 🟡 Important Limitations

### 4. Limited Package Manager Support

**Current Support**:
- ✅ npm (Node.js)
- ✅ pip (Python)
- ✅ winget (Windows)
- ✅ brew (macOS)

**Not Yet Supported** (Planned for Phase 2+):
- yarn, pnpm, bun (Node.js)
- poetry, pipx, conda (Python)
- apt, snap, flatpak (Linux)
- cargo (Rust), go (Go), gem (Ruby)

**Workaround**: Manage unsupported package managers manually.

---

### 5. No Vulnerability Scanning

**Issue**: Dashboard does not scan for known vulnerabilities (CVEs).

**Impact**: Users must run vulnerability checks separately.

**Workaround**: Use package manager native tools:
```bash
npm audit
pip-audit
```

**Planned**: Phase 3 (Integration with vulnerability databases)

---

### 6. No Dependency Tree Analysis

**Issue**: Cannot visualize or analyze dependency trees.

**Impact**: Hidden transitive dependencies may cause issues.

**Workaround**: Use package manager native tools:
```bash
npm list
pip show [package]
```

**Planned**: Phase 2 (Dependency graph visualization)

---

### 7. Snapshot Retention Limit

**Issue**: Only last 10 snapshots are retained per manager.

**Impact**: Older snapshots are automatically deleted.

**Workaround**: Manually backup snapshots from `~/.package-audit/snapshots/`

**Planned**: Phase 2 (Configurable retention policy)

---

## 🟢 Minor Limitations

### 8. No Real-Time Log Streaming

**Issue**: UI does not show real-time command output.

**Impact**: Long operations appear to hang.

**Workaround**: Check backend logs in terminal.

**Planned**: Phase 2 (SSE-based log streaming)

---

### 9. No Batch Operations

**Issue**: Cannot uninstall multiple packages at once.

**Impact**: Must uninstall packages one by one.

**Workaround**: None.

**Planned**: Phase 2 (Bulk operations with progress tracking)

---

### 10. No Export to Package Manager Lock Files

**Issue**: Cannot export snapshots to `package-lock.json`, `requirements.txt`, etc.

**Impact**: Manual recreation of lock files needed.

**Workaround**: Use package manager native export:
```bash
npm list --json > npm-packages.json
pip freeze > requirements.txt
```

**Planned**: Phase 2 (Lock file generation)

---

### 11. No Cross-Platform PATH Validation

**Issue**: PATH validation is basic and doesn't handle complex shell configurations.

**Impact**: May not detect all PATH issues.

**Workaround**: Manually verify PATH in shell:
```bash
echo $PATH
which npm
```

**Planned**: Phase 2 (Enhanced PATH detection)

---

### 12. No GUI Confirmation for Destructive Operations

**Issue**: All confirmations are backend-side only (no UI modal confirmation yet).

**Impact**: Users might accidentally trigger operations.

**Workaround**: Review operations in backend logs before execution.

**Planned**: Phase 1.5 (Frontend confirmation modals)

---

## 🔧 Platform-Specific Limitations

### Windows

- **Issue**: LockManager signal handling limited (no SIGTERM on Windows)
- **Impact**: Lock cleanup on process termination may not work
- **Workaround**: Manual lock cleanup via `rm ~/.package-audit/.lock`
- **Planned**: Phase 2 (Windows-specific process termination handlers)

### macOS

- **Issue**: Brew operations may require Rosetta 2 on Apple Silicon
- **Impact**: Some packages may fail to install
- **Workaround**: Install Rosetta 2 manually
- **Planned**: None (upstream limitation)

### Linux

- **Issue**: System package managers (apt, dnf) not supported yet
- **Impact**: Only user-level package managers work
- **Workaround**: Use system package manager CLI directly
- **Planned**: Phase 2 (System package manager support)

---

## 🎯 Design Decisions (Intentional Limitations)

### 1. Local-Only (No Cloud Sync)

**Reason**: Security and simplicity. No data leaves user's machine.

**Benefit**: Zero privacy concerns, works offline.

**Trade-off**: Cannot sync across devices.

---

### 2. Read-Only Package Discovery

**Reason**: Minimize risk of accidental system changes.

**Benefit**: Safe exploration without side effects.

**Trade-off**: Must explicitly trigger mutations.

---

### 3. No Automatic Updates

**Reason**: User should control when packages update.

**Benefit**: Prevents unexpected breaking changes.

**Trade-off**: Manual update management required.

---

## 📊 Performance Limitations

### Command Timeouts

| Operation | Timeout | Reason |
|-----------|---------|--------|
| List packages | 30s | Most package managers respond quickly |
| Uninstall package | 60s | Includes snapshot creation |
| Get version | 10s | Simple command |

**Impact**: Very large package lists may timeout.

**Workaround**: Increase timeout in adapter configuration.

---

### Concurrent Operations

- **Max READ operations**: Unlimited (but limited by system resources)
- **Max MUTATION operations**: 1 at a time (by design)

**Impact**: Uninstall operations must wait for previous operations to complete.

**Workaround**: None (intentional for safety).

---

## 🔮 Future Roadmap

### Phase 2 (Planned - Q2 2025)
- Automatic rollback on failure
- Enhanced vulnerability scanning
- Dependency tree visualization
- Batch operations
- Real-time log streaming
- Lock file export

### Phase 3 (Planned - Q3 2025)
- Multi-user support
- Advanced analytics
- Plugin system for custom package managers
- Cloud backup (optional)
- Usage analytics and recommendations

---

## 📝 Reporting New Limitations

Found a limitation not listed here?

1. Check existing GitHub issues
2. Open a new issue with label `limitation`
3. Include: Description, impact, workaround (if any)

---

**Last Updated**: 2025-11-05
**Phase**: MVP (Phase 1)
