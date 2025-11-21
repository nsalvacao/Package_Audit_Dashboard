# Changelog

All notable changes to Package Audit Dashboard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Docker Host Access Mode**: Full host system access from Docker containers
  - Execute commands on host (bash, PowerShell, CMD)
  - Access host package managers (npm, pip, brew, winget)
  - Invoke CLI tools on host (gemini-cli, claude, codex, etc.)
  - Persistent data storage on host filesystem
- **Multi-Platform Support**: Windows, macOS, Linux, and WSL2
- **Host Command Executor**: Three execution modes (docker, ssh, direct)
- **Professional Documentation Structure**: Organized hierarchical documentation
- **Installation Scripts**: Automated setup for all platforms
  - `install-docker-host.sh` for Unix/Linux/macOS/WSL
  - `install-docker-host.ps1` for Windows PowerShell
  - `test-docker-host.sh` for validation
- **Comprehensive Guides**:
  - 16KB Installation Guide with platform-specific instructions
  - 18KB Usage Guide with examples and best practices
  - Docker Host Access Guide with architecture diagrams
  - Scripts README with detailed documentation

### Changed
- **Documentation Reorganization**: Professional structure
  - User guides in `docs/guides/`
  - Deployment docs in `docs/deployment/`
  - Reference docs in `docs/reference/`
  - Architecture docs in `docs/architecture/`
  - Development docs in `docs/development/`
- **README.md**: Updated with new Docker host access option
- **Security Improvements**:
  - Thread-safe singleton pattern
  - Command injection prevention with `shlex.quote()`
  - Security warnings for privileged mode
- **Docker Compose**: Enhanced with host access configuration

### Security
- Fixed command injection vulnerabilities in host executor
- Implemented thread-safe singleton pattern
- Added proper shell escaping for all command executions
- Non-root user in Docker containers
- Optional privileged mode with security warnings

## [0.2.0] - Phase 2 Release

### Added
- 📡 Real-time log streaming with Server-Sent Events (SSE)
- 🌳 Dependency tree visualization
- 🔐 Integrated vulnerability scanning (npm audit, pip-audit)
- 📦 Batch operations for multiple packages
- ⏮️ Automatic rollback functionality
- 📄 Lock file export (requirements.txt, package-lock.json)

### Improved
- Enhanced security layer
- Better error handling
- Improved UI/UX
- Performance optimizations

For detailed changes, see [docs/development/CHANGELOG_PHASE2.md](docs/development/CHANGELOG_PHASE2.md)

## [0.1.0] - Phase 1 (MVP)

### Added
- 🔍 Auto-discovery of package managers (npm, pip, winget, brew)
- 🗑️ Safe package uninstallation with automatic snapshots
- 🔒 Multi-layer security system
  - ValidationLayer for input validation
  - LockManager for operation coordination
  - OperationQueue for sequential processing
- 🎯 REST API with FastAPI
  - Automatic OpenAPI documentation
  - Interactive Swagger UI
- 💻 CLI tool with Typer
  - Discover package managers
  - List installed packages
  - Uninstall packages
  - Manage snapshots
- 🌐 Modern web dashboard
  - React 18 + TypeScript
  - TailwindCSS styling
  - Responsive design
- 📊 Snapshot management
  - Automatic pre-uninstall snapshots
  - Manual snapshot creation
  - Snapshot restoration
  - Configurable retention
- 🛡️ Security features
  - Command injection prevention
  - Race condition protection
  - Path traversal protection
  - Input validation

### Security
- Implemented comprehensive security layer
- Added command execution timeout
- Added operation locking mechanism
- Added validation for all inputs

For detailed breakdown, see [docs/development/FASE1_BREAKDOWN.md](docs/development/FASE1_BREAKDOWN.md)

## Project Milestones

### Future Plans (Roadmap)

**Phase 3: Advanced Features**
- [ ] Remote package manager support
- [ ] Multi-host orchestration
- [ ] Advanced analytics dashboard
- [ ] Package recommendation engine
- [ ] Automated dependency updates
- [ ] Integration with CI/CD pipelines

**Phase 4: Enterprise Features**
- [ ] Role-based access control (RBAC)
- [ ] Audit logging and compliance
- [ ] Multi-tenancy support
- [ ] High availability deployment
- [ ] Kubernetes operator
- [ ] Cloud-native architecture

**Continuous Improvements**
- [ ] Enhanced security scanning
- [ ] Performance optimizations
- [ ] Additional package managers
- [ ] Extended platform support
- [ ] Improved testing coverage
- [ ] Localization/i18n

## Version History

| Version | Release Date | Key Features |
|---------|--------------|--------------|
| **Unreleased** | TBD | Docker Host Access, Documentation Reorganization |
| **0.2.0** | 2024-Q3 | Real-time streaming, Dependency trees, Vulnerability scanning |
| **0.1.0** | 2024-Q2 | MVP: Basic auditing, Safe uninstall, Snapshots |

## Upgrade Guide

### From 0.2.0 to Unreleased

**New Features:**
1. Docker host access mode available
2. Professional documentation structure

**Action Required:**
- None for existing installations
- For Docker host access: Use new installation scripts
- Update documentation links to new structure

**Breaking Changes:**
- None

### From 0.1.0 to 0.2.0

**New Features:**
1. Real-time log streaming
2. Vulnerability scanning
3. Batch operations

**Action Required:**
- Update dependencies: `pip install -r requirements.txt`
- Restart services

**Breaking Changes:**
- None

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## Support

- **Documentation**: [docs/README.md](docs/README.md)
- **Issues**: https://github.com/nsalvacao/Package_Audit_Dashboard/issues
- **Discussions**: https://github.com/nsalvacao/Package_Audit_Dashboard/discussions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Maintained by**: Package Audit Dashboard Contributors  
**Project Start**: 2024-Q1  
**Current Version**: 0.2.0+  
**Status**: Active Development
