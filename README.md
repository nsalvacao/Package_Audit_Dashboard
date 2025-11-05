# 📦 Package Audit Dashboard

[![Tests](https://github.com/nsalvacao/Package_Audit_Dashboard/actions/workflows/test.yml/badge.svg)](https://github.com/nsalvacao/Package_Audit_Dashboard/actions/workflows/test.yml)
[![Docker Build](https://github.com/nsalvacao/Package_Audit_Dashboard/actions/workflows/docker.yml/badge.svg)](https://github.com/nsalvacao/Package_Audit_Dashboard/actions/workflows/docker.yml)
[![codecov](https://codecov.io/gh/nsalvacao/Package_Audit_Dashboard/branch/main/graph/badge.svg)](https://codecov.io/gh/nsalvacao/Package_Audit_Dashboard)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![Node 18+](https://img.shields.io/badge/node-18+-brightgreen.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

MVP para auditar e gerir pacotes de diferentes gestores (npm, pip, winget/brew) com foco em segurança operacional.

---

## ✨ Features

### Phase 1 (MVP) - Completed
- 🔍 **Auto-discovery** de gestores de pacotes instalados (npm, pip, winget, brew)
- 🗑️ **Uninstall seguro** com snapshots automáticos antes da remoção
- 🔒 **Camada de segurança** robusta (ValidationLayer, LockManager, OperationQueue)
- 🎯 **API REST** completa com documentação automática (FastAPI)
- 💻 **CLI** para operações via terminal
- 🌐 **Dashboard web** com React + TypeScript + TailwindCSS
- 📊 **Gestão de snapshots** para backup e restauro
- 🛡️ **Prevenção de command injection** e race conditions

### Phase 2 (NEW!) - Just Released
- 📡 **Real-time log streaming** com Server-Sent Events (SSE)
- 🌳 **Dependency tree visualization** para análise de dependências
- 🔐 **Vulnerability scanning** integrado (npm audit, pip-audit)
- 📦 **Batch operations** para desinstalar múltiplos pacotes
- ⏮️ **Automatic rollback** para reverter alterações
- 📄 **Lock file export** (requirements.txt, package-lock.json)

---

## 🚀 Quick Start

### Opção 1: Setup Automatizado (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard

# Execute o script de setup
./scripts/quick_setup.sh

# Ou use a versão Python (cross-platform)
python3 scripts/quick_setup.py
```

### Opção 2: Setup Manual

#### 1. Backend Setup

```bash
cd backend

# Criar virtual environment
python3 -m venv .venv

# Ativar virtual environment
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar testes
pytest tests/ -v

# Iniciar servidor
uvicorn app.main:app --reload
```

O backend estará disponível em: http://localhost:8000

**Documentação interativa da API**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### 2. Frontend Setup

```bash
cd frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev
```

O frontend estará disponível em: http://localhost:5173

#### 3. CLI Setup (Opcional)

```bash
cd backend
source .venv/bin/activate

# Instalar CLI
pip install -e ../cli

# Ou usar diretamente
python -m cli.audit_cli --help
```

---

## 📁 Estrutura do Projeto

```
package-audit-dashboard/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── adapters/          # Package manager adapters (npm, pip, etc.)
│   │   ├── analysis/          # Snapshot management
│   │   ├── core/              # Security layer (validation, locking, queue)
│   │   ├── routers/           # API endpoints
│   │   ├── storage/           # JSON storage
│   │   └── main.py            # FastAPI application
│   ├── tests/                 # Comprehensive test suite
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # React + Vite Frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── hooks/             # Custom React hooks
│   │   └── App.tsx            # Main application
│   └── package.json           # Node dependencies
│
├── cli/                        # Typer CLI
│   ├── audit_cli/
│   │   ├── app.py             # CLI commands
│   │   └── __main__.py        # Entry point
│   └── setup.py               # CLI installation
│
├── docs/                       # Documentation
│   ├── SECURITY.md            # Security architecture
│   ├── LIMITATIONS.md         # Known limitations
│   ├── SETUP_PATH.md          # PATH configuration guide
│   └── API.md                 # API documentation
│
├── scripts/                    # Setup scripts
│   ├── quick_setup.sh         # Automated setup (Unix)
│   ├── quick_setup.py         # Automated setup (cross-platform)
│   └── chroma_sync.py         # ChromaDB synchronization
│
├── BLUEPRINT_FINAL.md          # Complete project blueprint
├── FASE1_BREAKDOWN.md          # Phase 1 task breakdown
└── LOG.md                      # Development log
```

---

## 🔧 Usage

### Web Dashboard

1. Inicie o backend: `cd backend && uvicorn app.main:app --reload`
2. Inicie o frontend: `cd frontend && npm run dev`
3. Aceda a http://localhost:5173
4. Dashboard mostrará automaticamente os gestores de pacotes detetados

### CLI

```bash
# Descobrir gestores instalados
python -m cli.audit_cli discover

# Listar pacotes
python -m cli.audit_cli list-packages npm
python -m cli.audit_cli list-packages pip

# Desinstalar pacote (com confirmação)
python -m cli.audit_cli uninstall npm lodash

# Desinstalar com força
python -m cli.audit_cli uninstall pip requests --force

# Ver status do sistema
python -m cli.audit_cli status

# Ajuda
python -m cli.audit_cli --help
```

### API REST

#### Basic Operations
```bash
# Descobrir gestores
curl -X POST http://localhost:8000/api/discover

# Obter detalhes dos gestores
curl http://localhost:8000/api/managers

# Desinstalar pacote
curl -X DELETE "http://localhost:8000/api/managers/npm/packages/lodash"
```

#### Phase 2 Advanced Features
```bash
# Scan vulnerabilities
curl http://localhost:8000/api/advanced/npm/vulnerabilities
curl http://localhost:8000/api/advanced/pip/vulnerabilities

# Get dependency tree
curl http://localhost:8000/api/advanced/npm/dependency-tree
curl http://localhost:8000/api/advanced/npm/dependency-tree/express

# Export lockfile
curl http://localhost:8000/api/advanced/npm/lockfile
curl http://localhost:8000/api/advanced/pip/lockfile

# Batch uninstall
curl -X POST http://localhost:8000/api/advanced/npm/batch-uninstall \
  -H "Content-Type: application/json" \
  -d '{"packages": ["lodash", "express"], "force": false}'

# Rollback to snapshot
curl -X POST http://localhost:8000/api/advanced/npm/rollback/snapshot-id-here

# Real-time streaming uninstall (SSE)
curl -N http://localhost:8000/api/streaming/npm/packages/lodash/uninstall
```

Ver documentação completa da API em: http://localhost:8000/docs

---

## 💡 Common Workflows

### Workflow 1: Complete Security Audit

Perform a comprehensive security audit of your project:

```bash
# 1. Start backend and frontend
cd backend && uvicorn app.main:app --reload &
cd frontend && npm run dev &

# 2. Discover package managers
curl -X POST http://localhost:8000/api/discover

# 3. Scan for vulnerabilities (npm)
curl http://localhost:8000/api/advanced/npm/vulnerabilities

# 4. Scan for vulnerabilities (pip)
curl http://localhost:8000/api/advanced/pip/vulnerabilities

# 5. Export lockfiles for backup
curl http://localhost:8000/api/advanced/npm/lockfile -o npm-list.json
curl http://localhost:8000/api/advanced/pip/lockfile -o requirements.txt

# 6. View dependency trees
curl http://localhost:8000/api/advanced/npm/dependency-tree
```

### Workflow 2: Safe Package Cleanup

Remove multiple packages safely with automatic rollback:

```bash
# 1. Create snapshot before cleanup
curl -X POST http://localhost:8000/api/discover

# 2. Review packages to remove
curl http://localhost:8000/api/managers/npm/packages

# 3. Batch uninstall with automatic snapshot
curl -X POST http://localhost:8000/api/advanced/npm/batch-uninstall \
  -H "Content-Type: application/json" \
  -d '{
    "packages": ["unused-package-1", "unused-package-2", "old-dep"],
    "force": false
  }'

# 4. If something goes wrong, rollback to previous state
# Get snapshot ID from response
curl -X POST http://localhost:8000/api/advanced/npm/rollback/SNAPSHOT_ID
```

### Workflow 3: Monitor Package Changes

Use the dashboard to monitor changes over time:

1. **Initial Snapshot**: Export lockfile as baseline
   ```bash
   curl http://localhost:8000/api/advanced/npm/lockfile -o baseline-npm.json
   curl http://localhost:8000/api/advanced/pip/lockfile -o baseline-pip.txt
   ```

2. **After Changes**: Compare current state
   ```bash
   curl http://localhost:8000/api/advanced/npm/lockfile -o current-npm.json
   diff baseline-npm.json current-npm.json
   ```

3. **Review Vulnerabilities**: Check for new security issues
   ```bash
   curl http://localhost:8000/api/advanced/npm/vulnerabilities | jq '.vulnerabilities[] | {package, severity}'
   ```

### Workflow 4: Development Environment Setup

Set up a clean development environment:

```bash
# 1. Clone and setup using Docker
git clone https://github.com/nsalvacao/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard
docker-compose up -d

# 2. Verify services are healthy
curl http://localhost:8000/health/detailed

# 3. Access the dashboard
open http://localhost:5173

# 4. Run security audit on your project
# The dashboard will show all detected package managers
# Click "Scan Vulnerabilities" on each manager card
```

### Workflow 5: CI/CD Integration

Integrate security scanning in your CI/CD pipeline:

```yaml
# .github/workflows/security-audit.yml
name: Security Audit

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    services:
      package-audit:
        image: ghcr.io/nsalvacao/package_audit_dashboard-backend:latest
        ports:
          - 8000:8000

    steps:
      - uses: actions/checkout@v3

      - name: Scan npm vulnerabilities
        run: |
          response=$(curl -s http://localhost:8000/api/advanced/npm/vulnerabilities)
          vulns=$(echo $response | jq '.vulnerabilities | length')

          if [ "$vulns" -gt 0 ]; then
            echo "::error::Found $vulns vulnerabilities"
            echo $response | jq '.vulnerabilities'
            exit 1
          fi

      - name: Scan pip vulnerabilities
        run: |
          response=$(curl -s http://localhost:8000/api/advanced/pip/vulnerabilities)
          vulns=$(echo $response | jq '.vulnerabilities | length')

          if [ "$vulns" -gt 0 ]; then
            echo "::error::Found $vulns vulnerabilities"
            exit 1
          fi
```

### Workflow 6: Real-time Package Operation Monitoring

Monitor package operations in real-time using SSE:

```javascript
// JavaScript example
const eventSource = new EventSource(
  'http://localhost:8000/api/streaming/npm/packages/lodash/uninstall'
);

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(`Status: ${data.status}`);
  console.log(`Output: ${data.output}`);

  if (data.status === 'completed') {
    console.log('✅ Uninstall successful');
    eventSource.close();
  } else if (data.status === 'failed') {
    console.error('❌ Uninstall failed:', data.error);
    eventSource.close();
  }
};
```

```bash
# Or using curl
curl -N http://localhost:8000/api/streaming/npm/packages/lodash/uninstall

# Output:
# data: {"status": "running", "output": "Removing lodash..."}
# data: {"status": "running", "output": "npm uninstall lodash"}
# data: {"status": "completed", "output": "removed 1 package"}
```

### Workflow 7: Dependency Tree Analysis

Analyze and visualize package dependencies:

```bash
# 1. Get complete dependency tree
curl http://localhost:8000/api/advanced/npm/dependency-tree | jq . > tree.json

# 2. Analyze specific package
curl http://localhost:8000/api/advanced/npm/dependency-tree/express | jq .

# 3. Find packages with most dependencies
curl http://localhost:8000/api/advanced/npm/dependency-tree | \
  jq '[.packages[] | {name, deps: (.dependencies | length)}] | sort_by(.deps) | reverse | .[0:10]'

# 4. Check for circular dependencies
curl http://localhost:8000/api/advanced/npm/dependency-tree | \
  jq '.packages[] | select(.dependencies | index(.name))'
```

---

## 🧪 Testing

```bash
cd backend
source .venv/bin/activate

# Executar todos os testes
pytest tests/ -v

# Executar com cobertura
pytest tests/ --cov=app --cov-report=html

# Executar testes específicos
pytest tests/test_validation.py -v
pytest tests/test_adapters.py -v
```

**Cobertura atual**: 80%+ (Core security components: 100%)

---

## 🔒 Security

Este projeto implementa múltiplas camadas de segurança:

- **ValidationLayer**: Validação de inputs e prevenção de command injection
- **LockManager**: Prevenção de race conditions
- **OperationQueue**: Serialização de operações perigosas
- **CommandExecutor**: Execução segura de comandos com timeouts
- **SnapshotManager**: Backup automático antes de operações destrutivas

Ver documentação completa em: [docs/SECURITY.md](docs/SECURITY.md)

---

## 📚 Documentation

- **[SECURITY.md](docs/SECURITY.md)** - Arquitetura de segurança e threat model
- **[LIMITATIONS.md](docs/LIMITATIONS.md)** - Limitações conhecidas e roadmap
- **[SETUP_PATH.md](docs/SETUP_PATH.md)** - Configuração de PATH para package managers
- **[API.md](docs/API.md)** - Documentação completa da API REST
- **[BLUEPRINT_FINAL.md](BLUEPRINT_FINAL.md)** - Blueprint completo do projeto
- **[FASE1_BREAKDOWN.md](FASE1_BREAKDOWN.md)** - Breakdown detalhado da Fase 1

---

## 🛠️ Requirements

### Backend
- Python 3.8+
- pip
- virtualenv

### Frontend
- Node.js 18+
- npm ou yarn

### Supported Package Managers
- **npm** (Node.js)
- **pip** (Python)
- **winget** (Windows)
- **brew** (macOS)

### ⚡ Optional Dependencies (Phase 2 Features)

For full Phase 2 functionality, install these optional tools:

```bash
# Python vulnerability scanning and dependency analysis
pip install pip-audit pipdeptree
```

**What you get:**
- ✅ **pip-audit**: Security vulnerability scanning for Python packages
- ✅ **pipdeptree**: Enhanced dependency tree visualization for pip

**Note:** npm features work out-of-the-box (built-in tools). See [OPTIONAL_DEPENDENCIES.md](docs/OPTIONAL_DEPENDENCIES.md) for details.

---

## 🗺️ Roadmap

### ✅ Phase 1 (MVP) - Completed
- [x] Security layer (ValidationLayer, LockManager, OperationQueue)
- [x] Package manager adapters (npm, pip, winget, brew)
- [x] Basic API endpoints (discover, managers, uninstall)
- [x] Snapshot management
- [x] CLI básico
- [x] Frontend básico

### ✅ Phase 2 - COMPLETED
- [x] Real-time log streaming (SSE)
- [x] Dependency tree visualization
- [x] Vulnerability scanning integration
- [x] Batch operations
- [x] Automatic rollback on failure
- [x] Lock file export

### 🔮 Phase 3 (Planned - Q3 2025)
- [ ] Multi-user support
- [ ] Cloud backup (optional)
- [ ] Advanced analytics
- [ ] Plugin system
- [ ] Usage recommendations

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

**Development Guidelines**:
- Escreva testes para novas funcionalidades
- Mantenha cobertura de testes acima de 80%
- Siga PEP 8 para código Python
- Use TypeScript para código frontend
- Documente alterações em `LOG.md`

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🐛 Troubleshooting

### Backend não inicia
```bash
# Verificar se virtual environment está ativo
which python  # deve mostrar .venv/bin/python

# Reinstalar dependências
pip install -r backend/requirements.txt
```

### Frontend não inicia
```bash
# Limpar cache e reinstalar
rm -rf frontend/node_modules frontend/package-lock.json
npm install
```

### Package managers não detetados
```bash
# Verificar PATH
echo $PATH

# Testar manualmente
which npm
which pip

# Ver guia de configuração
cat docs/SETUP_PATH.md
```

### Testes falham
```bash
# Alguns testes podem falhar se os package managers
# não estiverem instalados no sistema

# Executar apenas testes core
pytest tests/test_validation.py tests/test_locking.py -v
```

---

## 📧 Contact

- **Issues**: https://github.com/nsalvacao/Package_Audit_Dashboard/issues
- **Discussions**: https://github.com/nsalvacao/Package_Audit_Dashboard/discussions

---

## 🙏 Acknowledgments

- FastAPI por uma framework incrível
- React team pela biblioteca UI
- Typer por tornar CLIs simples
- Comunidade open-source

---

**Status**: ✅ Phase 1 & Phase 2 Complete | 🔮 Phase 3 In Planning

**Last Updated**: 2025-11-05

## 🆕 What's New in Phase 2

### Real-time Streaming
Monitor package operations in real-time with Server-Sent Events:
```javascript
const eventSource = new EventSource('/api/streaming/npm/packages/lodash/uninstall');
eventSource.onmessage = (event) => console.log(event.data);
```

### Vulnerability Scanning
Automatically scan for known vulnerabilities:
- **npm**: Uses built-in `npm audit`
- **pip**: Integrates with `pip-audit` (install with: `pip install pip-audit`)

### Dependency Trees
Visualize package dependencies:
- **npm**: Native `npm list --json` support
- **pip**: Enhanced with `pipdeptree` (install with: `pip install pipdeptree`)

### Batch Operations
Efficiently manage multiple packages at once with automatic snapshot creation before batch operations.

### Rollback Functionality
Restore system state to any previous snapshot, automatically removing packages that weren't present in the snapshot state.
