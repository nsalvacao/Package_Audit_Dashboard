# Language Guidelines / Guia de Idiomas

## Language Policy / Política de Idioma

This document describes the language policy for Package Audit Dashboard.

Este documento descreve a política de idioma para o Package Audit Dashboard.

---

## Primary Language / Idioma Principal

**English** is the primary language for this project.

**Inglês** é o idioma principal deste projeto.

---

## Language Distribution / Distribuição de Idiomas

### Code / Código

- **Variable names**: English only
- **Function names**: English only
- **Class names**: English only
- **Comments**: English preferred, Portuguese accepted
- **Docstrings**: English only

**Português:**
- **Nomes de variáveis**: Apenas inglês
- **Nomes de funções**: Apenas inglês
- **Nomes de classes**: Apenas inglês
- **Comentários**: Inglês preferencial, português aceite
- **Docstrings**: Apenas inglês

### Documentation / Documentação

| Document | Language | Notes |
|----------|----------|-------|
| README.md | Portuguese/English Mix | Main description in Portuguese, technical details in English |
| API.md | English | API documentation in English |
| CONTRIBUTING.md | English | Contributing guidelines in English |
| SECURITY.md | English | Security documentation in English |
| CHANGELOG*.md | English | Release notes in English |
| OPTIONAL_DEPENDENCIES.md | English | Setup instructions in English |
| ENV_SETUP.md | English | Configuration guide in English |
| DOCKER.md | English | Docker documentation in English |
| Code comments | English (preferred) | Can use Portuguese for complex logic |
| Git commits | English | Commit messages in English |
| Issues/PRs | English/Portuguese | Both accepted, English preferred |

### User Interface / Interface de Utilizador

| Component | Language | Notes |
|-----------|----------|-------|
| API responses | English | All error messages and responses in English |
| CLI output | English | Terminal output in English |
| Web dashboard | English | UI labels and messages in English |
| Logs | English | All log messages in English |

---

## Rationale / Justificação

### Why English? / Porquê Inglês?

1. **International collaboration**: English makes the project accessible to global contributors
2. **Technical standard**: Most programming documentation is in English
3. **Library integration**: External APIs and libraries use English
4. **Career development**: Contributors practice technical English

### Why Portuguese README? / Porquê README em Português?

1. **Target audience**: Initial users are Portuguese-speaking
2. **Local context**: Project started in Portuguese environment
3. **Accessibility**: Easier onboarding for local users
4. **Gradual transition**: Can migrate to full English later

---

## Migration Plan / Plano de Migração

### Current State / Estado Atual

- ✅ Code: 100% English
- ✅ API: 100% English
- ⚠️ README: Mixed (Portuguese intro, English technical)
- ✅ Documentation: 90% English
- ✅ Comments: Mostly English

### Future Goals / Objetivos Futuros

**v1.0.0 (Q4 2025)**:
- Maintain Portuguese README intro
- All new documentation in English
- Gradually translate existing Portuguese comments

**v2.0.0 (2026)**:
- Consider full English README with Portuguese translation
- Implement i18n for web dashboard (optional)
- Multi-language documentation support

---

## Best Practices / Melhores Práticas

### For Contributors / Para Contribuidores

#### English-speaking contributors:

```python
# ✅ Good
def validate_package_name(name: str) -> bool:
    """Validate package name format."""
    return bool(re.match(r'^[a-zA-Z0-9@/_.-]+$', name))

# ❌ Avoid
def validar_nome_pacote(nome: str) -> bool:
    """Validar formato do nome do pacote."""
    return bool(re.match(r'^[a-zA-Z0-9@/_.-]+$', nome))
```

#### Portuguese-speaking contributors:

```python
# ✅ Acceptable for complex logic
def process_dependency_tree(root_package: str) -> dict:
    """Process package dependency tree."""
    # Primeiro, verificamos se o pacote existe
    # Em seguida, obtemos todas as dependências recursivamente
    pass

# ✅ Better - use English comments
def process_dependency_tree(root_package: str) -> dict:
    """Process package dependency tree."""
    # First, check if package exists
    # Then, recursively fetch all dependencies
    pass
```

### For Documentation / Para Documentação

When documenting features:

1. **Write in English first**: Primary documentation should be English
2. **Add Portuguese notes** (optional): For complex concepts, add Portuguese explanations
3. **Use clear language**: Avoid idioms and colloquialisms
4. **Provide examples**: Code examples are language-agnostic

---

## Translation Guidelines / Guias de Tradução

### Common Terms / Termos Comuns

| English | Portuguese | Usage |
|---------|-----------|-------|
| package | pacote | Use "package" in code/docs |
| manager | gestor | Use "manager" in code/docs |
| snapshot | snapshot | Keep English term |
| rollback | rollback | Keep English term |
| vulnerability | vulnerabilidade | Use "vulnerability" in code |
| dependency | dependência | Use "dependency" in code |

### Do Not Translate / Não Traduzir

These terms should **always be in English**:

- Technical terms: API, CLI, REST, JSON, HTTP, SSE
- Tool names: Docker, npm, pip, FastAPI, React
- Code concepts: middleware, router, endpoint, request, response
- Command line: install, uninstall, list, audit

---

## Questions / Questões

### For English speakers:

**Q**: Should I write comments in English?
**A**: Yes, always write code comments in English.

**Q**: Can I create issues in English?
**A**: Yes, English issues are welcome and preferred.

**Q**: What about git commit messages?
**A**: Use English, following Conventional Commits format.

### For Portuguese speakers:

**Q**: Posso escrever comentários em português?
**A**: Pode, mas inglês é preferencial. Use português apenas para lógica complexa que seja mais fácil explicar.

**Q**: E as issues no GitHub?
**A**: Ambos os idiomas são aceites, mas inglês é preferencial para aumentar o alcance do projeto.

**Q**: Devo traduzir o README para inglês?
**A**: Por enquanto não. Mantenha a introdução em português. A partir da v1.0 consideraremos tradução completa.

---

## Contact / Contacto

For questions about language policy:
- Open an issue: https://github.com/nsalvacao/Package_Audit_Dashboard/issues
- Discussions: https://github.com/nsalvacao/Package_Audit_Dashboard/discussions

Para questões sobre a política de idioma:
- Abrir issue: https://github.com/nsalvacao/Package_Audit_Dashboard/issues
- Discussões: https://github.com/nsalvacao/Package_Audit_Dashboard/discussions

---

**Last Updated**: 2025-11-05
**Version**: 1.0
