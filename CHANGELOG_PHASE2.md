# Changelog - Phase 2 Release

## Version 0.2.0 - Phase 2 Complete (2025-11-05)

### 🎉 Major Features Added

#### 1. Real-time Log Streaming (SSE)
- **New Router**: `/api/streaming`
- **Endpoint**: `GET /api/streaming/{manager_id}/packages/{package_name}/uninstall`
- Server-Sent Events (SSE) para monitoramento em tempo real de operações
- Streaming de logs durante uninstall de pacotes
- Headers otimizados para SSE (`Cache-Control`, `X-Accel-Buffering`)

#### 2. Dependency Tree Visualization
- **New Router**: `/api/advanced`
- **Endpoints**:
  - `GET /api/advanced/{manager_id}/dependency-tree` - Árvore completa
  - `GET /api/advanced/{manager_id}/dependency-tree/{package_name}` - Pacote específico
- **npm**: Usa `npm list --json` nativo
- **pip**: Suporte para `pipdeptree` (opcional, com fallback para `pip show`)

#### 3. Vulnerability Scanning
- **Endpoint**: `GET /api/advanced/{manager_id}/vulnerabilities`
- **npm**: Integração com `npm audit --json`
- **pip**: Integração com `pip-audit --format=json` (requer instalação)
- Retorna lista de vulnerabilidades com severidade, descrição e pacotes afetados

#### 4. Batch Operations
- **Endpoint**: `POST /api/advanced/{manager_id}/batch-uninstall`
- Desinstala múltiplos pacotes em uma única operação
- Snapshot automático antes da operação batch
- Retorna lista de sucessos e falhas
- Request model: `BatchUninstallRequest`
- Response model: `BatchUninstallResponse`

#### 5. Automatic Rollback
- **Endpoint**: `POST /api/advanced/{manager_id}/rollback/{snapshot_id}`
- Restaura sistema para estado de snapshot anterior
- Remove automaticamente pacotes que não existiam no snapshot
- Retorna lista de pacotes desinstalados e falhas

#### 6. Lock File Export
- **Endpoint**: `GET /api/advanced/{manager_id}/lockfile`
- **npm**: Exporta `npm list --json` (equivalente a package-lock)
- **pip**: Exporta `pip freeze` (requirements.txt)
- Download automático no frontend com formato correto

### 🔧 Backend Changes

#### New Files
- `backend/app/routers/streaming.py` - SSE router
- `backend/app/routers/advanced.py` - Advanced features router
- `backend/tests/test_advanced_router.py` - Testes para advanced router
- `backend/tests/test_streaming_router.py` - Testes para streaming router

#### Modified Files
- `backend/app/main.py` - Registra novos routers, atualiza versão para 0.2.0
- `backend/app/routers/__init__.py` - Exporta novos routers
- `backend/app/adapters/base.py` - Adiciona métodos para:
  - `get_dependency_tree()`
  - `scan_vulnerabilities()`
  - `export_lockfile()`
- `backend/app/adapters/npm.py` - Implementa novas funcionalidades para npm
- `backend/app/adapters/pip.py` - Implementa novas funcionalidades para pip

### 🎨 Frontend Changes

#### New Components
- `frontend/src/components/VulnerabilityScan.tsx` - Scanner de vulnerabilidades
- `frontend/src/components/LockfileExport.tsx` - Exportador de lockfiles

#### Modified Components
- `frontend/src/components/ManagerCard.tsx`:
  - Integra VulnerabilityScan
  - Integra LockfileExport
  - Adiciona link para Dependency Tree
  - UI expandível para "Advanced Features"

### 📚 Documentation

#### Updated Files
- `README.md`:
  - Adiciona seção "What's New in Phase 2"
  - Atualiza lista de features com Phase 2
  - Adiciona exemplos de API para features avançadas
  - Atualiza roadmap (Phase 2 ✅ COMPLETED)
  - Atualiza status do projeto
- `CHANGELOG_PHASE2.md` - Este arquivo

### 🧪 Testing

#### New Test Files
- `test_advanced_router.py`:
  - Testes para dependency tree
  - Testes para vulnerability scanning
  - Testes para lockfile export
  - Testes para batch operations
  - Testes para rollback
- `test_streaming_router.py`:
  - Testes para SSE endpoints
  - Validação de headers SSE

### 🔒 Security

Todas as novas funcionalidades mantêm as mesmas garantias de segurança do Phase 1:
- ✅ ValidationLayer para sanitização de inputs
- ✅ LockManager para prevenção de race conditions
- ✅ OperationQueue para serialização de operações
- ✅ Snapshots automáticos antes de operações destrutivas

### 📦 Dependencies

#### Optional Dependencies (para funcionalidades avançadas)
- **pip-audit**: Para vulnerability scanning no pip
  ```bash
  pip install pip-audit
  ```
- **pipdeptree**: Para dependency trees completos no pip
  ```bash
  pip install pipdeptree
  ```

#### Frontend Dependencies
Nenhuma dependência nova - usa as existentes:
- @tanstack/react-query
- axios
- react
- typescript

### 🚀 Migration Guide

#### Para Atualizar de Phase 1 para Phase 2:

1. **Pull das alterações**:
   ```bash
   git pull origin main
   ```

2. **Backend** (sem alterações necessárias):
   ```bash
   cd backend
   # As mesmas dependências do Phase 1
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

3. **Frontend** (sem alterações necessárias):
   ```bash
   cd frontend
   npm install  # ou yarn install
   npm run dev
   ```

4. **Opcional - Instalar ferramentas de análise**:
   ```bash
   # Para vulnerability scanning no pip
   pip install pip-audit

   # Para dependency trees completos no pip
   pip install pipdeptree
   ```

5. **Acessar nova documentação**:
   - API docs: http://localhost:8000/docs
   - Novos endpoints aparecem automaticamente na documentação interativa

### 🎯 API Endpoints Summary

#### Phase 2 Endpoints

```
# Streaming
GET  /api/streaming/{manager_id}/packages/{package_name}/uninstall

# Advanced Features
GET  /api/advanced/{manager_id}/dependency-tree
GET  /api/advanced/{manager_id}/dependency-tree/{package_name}
GET  /api/advanced/{manager_id}/vulnerabilities
GET  /api/advanced/{manager_id}/lockfile
POST /api/advanced/{manager_id}/batch-uninstall
POST /api/advanced/{manager_id}/rollback/{snapshot_id}
```

### 🐛 Known Limitations

1. **Rollback**: Apenas remove pacotes excedentes, não reinstala pacotes ausentes (install functionality não implementado)
2. **Vulnerability Scanning**:
   - pip: Requer `pip-audit` instalado
   - Alguns gestores podem não ter suporte nativo
3. **Dependency Trees**:
   - pip: Funcionalidade limitada sem `pipdeptree`
   - winget/brew: Não implementado (retorna mensagem de não suportado)

### 🔜 Next Steps (Phase 3)

- Multi-user support
- Cloud backup integration
- Advanced analytics
- Plugin system
- Usage recommendations
- Package installation functionality (para rollback completo)

---

**Full Release**: Phase 2 Complete
**Version**: 0.2.0
**Date**: 2025-11-05
