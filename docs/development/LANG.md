# Language Guidelines

## Language Policy

This document defines the language policy for the Package Audit Dashboard project.

---

## Primary Language

**English** is the authoritative language for all project artifacts.

---

## Language Expectations

### Code

- **Variable names**: English only
- **Function names**: English only
- **Class names**: English only
- **Comments**: English preferred (Portuguese allowed only when it materially improves clarity)
- **Docstrings**: English only

### Documentation

| Document | Language | Notes |
|----------|----------|-------|
| README.md | English | Main project overview |
| API.md | English | REST API documentation |
| CONTRIBUTING.md | English | Contribution guidelines |
| SECURITY.md | English | Security architecture |
| CHANGELOG*.md | English | Release notes |
| OPTIONAL_DEPENDENCIES.md | English | Optional tool setup |
| ENV_SETUP.md | English | Environment configuration |
| DOCKER.md | English | Docker usage |
| Code comments | English (preferred) | Portuguese permitted for highly complex logic |
| Git commits | English | All commit messages |
| Issues/PRs | English (preferred) | Portuguese acceptable when necessary |

### User Interface

| Component | Language | Notes |
|-----------|----------|-------|
| API responses | English | Error messages and payloads |
| CLI output | English | Terminal interactions |
| Web dashboard | English | UI labels and notifications |
| Logs | English | Operational logging |

---

## Rationale

### Why English?

1. **International collaboration** — English keeps the project accessible to all contributors
2. **Technical consistency** — Most libraries, APIs, and reference material use English
3. **Easier integration** — External tooling expects English naming conventions
4. **Professional growth** — Contributors can practice technical English in a real project

### Why keep historical Portuguese references in git history?

1. **Audience continuity** — Earlier iterations targeted Portuguese-speaking users
2. **Context preservation** — Some architectural decisions were recorded in Portuguese
3. **Accessibility** — Existing contributors can refer to previous notes if needed
4. **Gradual migration** — The project transitioned to English without erasing prior work

---

## Migration Plan

### Current Status

- ✅ Codebase: 100% English
- ✅ API: 100% English
- ✅ README: Fully translated
- ✅ Documentation: 100% English
- ✅ Comments: Mostly English (Portuguese allowed only when clarifying complex logic)

### Future Goals

**v1.0.0 (Q4 2025):**
- Maintain English documentation as the default source of truth
- Provide Portuguese addenda when community demand justifies it
- Continue translating legacy Portuguese comments as they are touched

**v2.0.0 (2026):**
- Evaluate full i18n support for the web dashboard
- Offer localized documentation packs if maintainers are available
- Automate translation workflows where possible

---

## Best Practices

### For Contributors

#### English-speaking contributors

```python
# ✅ Good
def validate_package_name(name: str) -> bool:
    """Validate package name format."""
    return bool(re.match(r"^[a-zA-Z0-9@/_.-]+$", name))

# ❌ Avoid
def validar_nome_pacote(nome: str) -> bool:
    """Validate package name format."""
    return bool(re.match(r"^[a-zA-Z0-9@/_.-]+$", nome))
```

#### Portuguese-speaking contributors

```python
# ✅ Acceptable for complex logic
def process_dependency_tree(root_package: str) -> dict:
    """Process package dependency tree."""
    # First, verify that the package exists
    # Then, recursively collect all dependencies
    pass

# ✅ Better — keep comments in English when possible
def process_dependency_tree(root_package: str) -> dict:
    """Process package dependency tree."""
    # First, check if the package exists
    # Then, recursively fetch all dependencies
    pass
```

### For Documentation

When documenting features:

1. **Write in English first** — English is the canonical source
2. **Add Portuguese notes only when critical** — Keep the main flow in English
3. **Use clear, direct language** — Avoid idioms and region-specific jargon
4. **Include examples** — Code snippets remain language-agnostic

---

## Translation Guidelines

### Common Terms

| English | Portuguese | Usage |
|---------|------------|-------|
| package | pacote | Prefer the English term in code and docs |
| manager | gestor | Prefer the English term in code and docs |
| snapshot | snapshot | English term is standard |
| rollback | rollback | English term is standard |
| audit | auditoria | Use "audit" in technical contexts |
