# Backlog de Bugs e Melhorias

**Data da Instalação Teste**: 2025-11-27
**Ambiente Teste**: C:\Users\nunos\Package_Audit_Dashboard
**Versão**: v0.2.0 - Phase 2 Complete

---

## 🚨 Bloqueantes (P0)

- [x] **Rota GET inexistente**: `/api/managers/{manager_id}/packages` ✅ **RESOLVIDO 2025-11-27**
  - **Sintoma**: Tab "Packages" retorna 404, fica em "Loading packages..."
  - **Localização**: `backend/app/routers/managers.py`
  - **Impacto**: Funcionalidade crítica não funciona (listar pacotes instalados)
  - **Evidência**: Screenshot `packages-view-error.png`, logs `GET /api/managers/npm/packages 404`
  - **Resolução**: Endpoint GET completo implementado (linhas 40-74) com validação, error handling e formato correto
  - **Testes**: ✅ curl (10 npm packages), ✅ Playwright MCP (npm: 10, pip: 113)

---

## ⚠️ Alta Prioridade (P1)

- [x] **Enhanced Logging não visível** ✅ **RESOLVIDO 2025-11-27**
  - **Config**: `ENABLE_DETAILED_LOGGING=true` ativo em `.env`
  - **Sintoma**: Logs detalhados (request/response bodies) não aparecem no stdout
  - **Root causes identificadas**:
    1. `logging.py:_format_human()` não imprimia campos extra_data
    2. `main.py` não carregava .env (faltava `load_dotenv()`)
  - **Resolução**:
    1. Modificado `logging.py:98-115` para iterar e exibir extra_data fields
    2. Adicionado `from dotenv import load_dotenv` e `load_dotenv()` em `main.py:9,19`
  - **Testes**: ✅ Logs agora mostram request_id, method, path, query_params, headers, duration_ms, status_code

- [x] **Vulnerabilidade npm** ✅ **RESOLVIDO 2025-11-27**
  - **Sintoma**: `1 high severity vulnerability` após `npm install`
  - **Vulnerability**: glob 10.4.5 - Command Injection (CWE-78, CVSS 7.5)
  - **Dependency**: tailwindcss → sucrase → glob 10.4.5
  - **Risk**: LOW (indirect, dev-only, CLI not used)
  - **Resolução**: `npm audit fix` → glob 10.4.5 → 10.5.0
  - **Testes**: ✅ npm audit (0 vulnerabilities), ✅ build funcional (2.94s), ✅ UI operacional

---

## 📝 Melhorias (P2)

- [x] **Warnings npm deprecated** 📋 **DOCUMENTADO como NÃO-CRÍTICO 2025-11-27**
  - **Packages**: eslint@8.57.1 → rimraf@3.0.2 → glob@7.2.3 → inflight@1.0.6
  - **Análise**:
    - 4-5 níveis de profundidade (indirect dependency)
    - Usado apenas por eslint file caching (dev-only)
    - **npm audit: 0 vulnerabilities** ✅
    - Não afeta build ou runtime
  - **Upgrade path**: eslint 8→9 + @typescript-eslint 6→8 + flat config migration
  - **Decisão**: **NÃO upgrade**. Razões:
    1. Zero impacto funcional
    2. Zero risco segurança
    3. Esforço upgrade > benefício (flat config + breaking changes)
    4. Warnings informativos, não críticos
  - **Plugins compatíveis com eslint v9**: @typescript-eslint ✅, react-hooks ✅, react-refresh ✅

- [x] **Diretório de dados não criado** 📋 **DOCUMENTADO como COMPORTAMENTO ESPERADO 2025-11-27**
  - **Comportamento**: `C:\Users\nunos\.package-audit\` criado on-demand (primeira operação persistência)
  - **Implementação**:
    - `JSONStorage.__init__()` cria automaticamente via `mkdir(parents=True, exist_ok=True)`
    - Instantiated em: SnapshotManager e BaseAdapter (lazy initialization)
  - **Análise**:
    - ✅ Pattern válido (lazy initialization)
    - ✅ Error handling adequado (exist_ok=True)
    - ✅ Evita criar diretórios desnecessários
  - **Minor issue identificado**: .env define `DATA_DIR` mas código usa hardcoded `Path.home() / ".package-audit"` (`validation.py:22`)
  - **Decisão**: **ACEITAR comportamento atual**. Lazy initialization é apropriado.
  - **Ação futura opcional**: Considerar usar DATA_DIR do .env para customização

- [ ] **Vite 7.2.1 levemente desatualizado**
  - **Versão atual**: 7.2.1
  - **Versão latest**: 7.2.4 (released 2025-11-20, 7 dias atrás)
  - **Análise**: Patch version update, baixo risco
  - **Ação**: Upgrade opcional `npm install vite@latest`
  - **Prioridade**: Baixa - funciona perfeitamente

- [ ] **Conflito de prefixes** (Manutenibilidade)
  - **Localização**:
    - `managers.py:14` - `router = APIRouter(prefix="/api/managers", tags=["managers"])`
    - `packages.py:18` - `router = APIRouter(prefix="/api/managers", tags=["packages"])`
  - **Impacto**: Funciona (FastAPI merge routes) mas confuso para manutenção
  - **Análise**: Low priority - não afeta funcionalidade
  - **Ação futura**: Considerar renomear packages.py para `/api/packages` ou consolidar routers
  - **Prioridade**: Baixa - código funcional, apenas manutenibilidade

---

## ✅ Funcionando Corretamente

- ✓ Instalação limpa completa (backend + frontend)
- ✓ Descoberta de package managers (3/3: npm, pip, pnpm)
- ✓ **Endpoint GET packages funcional** ✅ (npm: 10, pip: 113 packages)
- ✓ **Enhanced logging operacional** ✅ (request_id, headers, duration_ms, etc.)
- ✓ **0 vulnerabilidades npm** ✅ (glob 10.5.0 secure)
- ✓ CORS configurado via variável de ambiente (não hardcoded)
- ✓ UI carrega e responde a interações
- ✓ Playwright MCP funcional para testes automatizados
- ✓ Servidores arrancam < 2 segundos
- ✓ .env carregado corretamente via python-dotenv

---

## 📊 Métricas da Instalação

| Métrica | Valor | Status |
|---------|-------|--------|
| Backend packages | ~150 | ✅ |
| Frontend packages | 352 | ✅ |
| Tempo install backend | ~2 min | ✅ |
| Tempo install frontend | 16 seg | ✅ |
| Managers detetados | 3/3 | ✅ |
| Rotas funcionais | 100% core | ✅ |
| npm vulnerabilities | 0 | ✅ |
| P0 bloqueantes resolvidos | 1/1 | ✅ |
| P1 alta prioridade resolvidos | 2/2 | ✅ |
| P2 melhorias documentadas | 4/4 | ✅ |

---

## 🎯 Notas de Progresso (2025-11-27)

**Sessão de correção P0+P1+P2 completa**:
- ✅ P0 (GET endpoint) - Implementado e testado
- ✅ P1 (Enhanced logging) - 2 fixes aplicadas (formatter + load_dotenv)
- ✅ P1 (npm vulnerability) - Resolvida (glob 10.5.0)
- ✅ P2 (npm deprecated) - Analisado e documentado (não-crítico, 0 security issues)
- ✅ P2 (data directory) - Analisado e documentado (lazy initialization válida)
- ⏳ P2 (Vite update) - Opcional, baixa prioridade
- ⏳ P2 (Prefix conflict) - Manutenibilidade, baixa prioridade

**Ferramentas utilizadas**:
- Sequential thinking MCP (8 thoughts, análise estruturada)
- Playwright MCP (testes UI automatizados)
- npm audit (análise vulnerabilidades)
- Git (deployment dev → test environment)

**Próximo ciclo**:
- Opcional: Upgrade Vite 7.2.1 → 7.2.4 (patch version, seguro)
- Ciclo 2: Adicionar adapters para gestores críticos (uv, choco, apt)

---

## 🔍 Investigação de Sistema (2025-11-27)

### Gestores de Pacotes Instalados

#### Windows
- ✅ **npm** - 10 global packages (claude-code, gemini-cli, playwright, flowise, pnpm, pyright, etc.)
- ✅ **pnpm** - Instalado via npm global
- ✅ **pip** - Python 3.12
- ✅ **pipx** - **39 CLIs isoladas** (aider, black, pytest, fastapi, langchain-cli, llama-index-cli, chromadb, vllm, safety, bandit, ruff, mypy, etc.)
- ✅ **uv** - Python package manager moderno (instalado via pipx)
- ✅ **winget** - ~20+ aplicações sistema (Docker, Git, Chrome, Node.js, Azure CLI)
- ✅ **choco** - Chocolatey ativo
- ❌ yarn, poetry, scoop (não instalados)

#### WSL (Ubuntu)
- ✅ **apt** - **871 packages** (sistema Ubuntu)
- ✅ **npm** - 10 global (claude-code, copilot, codex, eslint)
- ✅ **pip/pip3** - 65 packages (via pyenv Python 3.12)
- ✅ **pyenv** - Gestão versões Python
- ✅ **snap** - Canonical package manager
- ❌ pipx, uv, cargo, gem (não instalados)

**Total estimado: 1000+ pacotes/ferramentas instalados no sistema.**

### Análise vs Arquitetura Atual

#### ✅ Arquitetura está sólida e extensível
- **BaseAdapter** bem desenhado com interface clara (detect, get_version, list_packages, uninstall, export_manifest)
- **Registry centralizado** facilita adição de novos gestores
- **CommandExecutor** com validação, timeouts e segurança
- **JSONStorage** para persistência
- **SnapshotManager** para rollbacks seguros

#### ✅ Adapters já implementados
- npm, pnpm, pip, pipx, brew, winget (6 adapters)
- Código limpo, bem estruturado, fácil de estender

#### ⚠️ Gaps Identificados

**P0 - Bloqueantes**:
- Endpoint `GET /api/managers/{manager_id}/packages` faltante (já documentado acima)

**P1 - Gestores populares não suportados**:
- ❌ `uv` (Python, crescimento massivo em 2024)
- ❌ `choco` (Chocolatey, popular no Windows)
- ❌ `apt` (crítico para Ubuntu/Debian/WSL)
- ❌ `snap` (Canonical, usado em Ubuntu)
- ❌ `cargo` (Rust, crescente popularidade)
- ❌ `gem` (Ruby)
- ❌ `yarn` (Node.js alternativo, menos crítico)

**P2 - Funcionalidade futura**:
- [ ] **Detecção de CLIs instaladas diretamente** (fora de package managers)
  - Verificar PATH (Windows + WSL)
  - Scan de diretórios comuns: `Program Files`, `%LOCALAPPDATA%`, `~/.local/bin`, `/usr/local/bin`
  - Desafio: distinguir CLIs relevantes de binários de sistema

### 🎯 Decisão: Continuar ou Refactor?

**DECISÃO: Continuar com melhorias incrementais**

**Razões**:
1. Arquitetura suporta perfeitamente os requisitos fundamentais
2. Gaps são incrementais (adicionar adapters, completar endpoints)
3. Nenhum problema arquitetural fundamental identificado
4. BaseAdapter permite adicionar gestores em ~30 minutos cada
5. Registry centralizado mantém tudo organizado

**Não há necessidade de refactor completo.**

### 📋 Próximos Passos Recomendados

**Ciclo 1 - Resolver bloqueantes**:
1. Adicionar endpoint `GET /api/managers/{manager_id}/packages` (P0)
2. Investigar enhanced logging output (P1)
3. Executar `npm audit fix` (P1)
4. Testes UI completos com Playwright MCP

**Ciclo 2 - Adicionar gestores críticos**:
1. Criar `UvAdapter` (Python uv)
2. Criar `ChocoAdapter` (Chocolatey)
3. Criar `AptAdapter` (Ubuntu/Debian)
4. Atualizar registry com novos adapters
5. Testes integração

**Ciclo 3 - Gestores secundários**:
1. `SnapAdapter`, `CargoAdapter`, `GemAdapter`
2. Detecção de CLIs diretas (investigação + POC)

---

## 📚 Documentação Atualizada

- ✅ `CLAUDE.md` criado com contexto fundamental, arquitetura, gaps identificados
- ✅ `README.md` atualizado com "Problem Statement" clarificando as 3 perguntas fundamentais
