# Log Operacional

## 2025-11-03

### Contexto
- Revisão inicial da Fase 1 para alinhar o MVP seguro com a estrutura real do repositório.

### Ações
- Atualizada `FASE1_BREAKDOWN.md` para remover diretório aninhado redundante e reforçar práticas de merge em `.gitignore`/`README.md`.
- Adicionada checklist de testes críticos (CommandExecutor, OperationQueue, adapters, endpoints) e cronograma em cinco blocos.
- Documentado aviso sobre compatibilidade de `LockManager` com sinais em Windows/macOS e criação de scripts auxiliares em `scripts/setup/`.
- Iniciada Fase A com criação da estrutura base (`frontend/`, `backend/`, `cli/`, `docs/`) e ficheiros `__init__.py`.
- Consolidado `.gitignore` com entradas padrão para Python/Node/IDE mantendo notas locais.
- Implementado `scripts/setup/bootstrap_structure.py` para automatizar a criação da estrutura e ficheiros `__init__.py`.
- Desenvolvido `ValidationLayer` (SEC-001) com exceções especializadas e validação de nomes, comandos e paths.
- Criados testes unitários `backend/tests/test_validation.py` com cobertura total e fixtures isolando diretório permitido.
- Configurado ambiente virtual `.venv` local e instalado `pytest` para execução controlada da suite.
- Implementado `LockManager` (SEC-002) com detecção de locks obsoletos, cleanup automático e tolerância a plataformas que não suportem sinais.
- Adicionados testes `backend/tests/test_locking.py` cobrindo aquisição, stale detection, espera e force release.
- Desenvolvido `OperationQueue` (SEC-003) com suporte a operações READ concorrentes e MUTATION serializadas via `LockManager`.
- Criados testes assíncronos `backend/tests/test_queue.py` para concorrência, bloqueio, propagação de erros e singleton.
- Instalado `pytest-asyncio` no `.venv` para suporte às suites assíncronas.
- Desenvolvido `CommandExecutor` (CORE-001) com execução síncrona/assíncrona segura, logging e timeouts configuráveis.
- Acrescentados testes `backend/tests/test_executor.py` cobrindo sucesso, falha, timeout e validações de tipo, incluindo variantes assíncronas.
- Implementado `JSONStorage` (CORE-002) com escrita atómica, resolução segura de paths e integração no diretório `.package-audit/storage`.
- Criados testes `backend/tests/test_json_storage.py` validando leitura, escrita, remoção, prevenção de traversal e consistência dos ficheiros.
- Implementado `BaseAdapter` (CORE-003) consolidando detecção, execução de comandos e cache comum aos gestores.
- Criados testes `backend/tests/test_base_adapter.py` para verificação de deteção, obtenção de versão, sanitização e cache.
- Implementado `SnapshotManager` (CORE-004) com suporte a retenção automática (10 itens) e armazenamento de metadados.
- Criados testes `backend/tests/test_snapshot_manager.py` para persistência, ordenação, retenção e validação de gestores.
- Implementado `NpmAdapter` (Task 4.1) reutilizando `BaseAdapter` para comandos e sanitização.
- Criados testes `backend/tests/test_npm_adapter.py` cobrindo listagem, uninstall (com/sem `--force`), export de manifest e rejeição de nomes inválidos.
- Implementado `PipAdapter` (Task 4.2) com listagem via `pip list --format=json`, uninstall automatizado e export de manifest.
- Criados testes `backend/tests/test_pip_adapter.py` para parsing, fallback em caso de erro, execução de uninstall e validação de nomes.
- Implementados `WinGetAdapter` e `BrewAdapter` (Task 4.3) seguindo o padrão BaseAdapter + CommandExecutor.
- Criados testes `backend/tests/test_winget_adapter.py` e `backend/tests/test_brew_adapter.py` para parsing, comandos (force) e validação.
- Construído router `/api/discover` com deteção baseada nos adapters disponíveis.
- Criados testes `backend/tests/test_discover_router.py` garantindo cobertura de versões e deteções simuladas.
- Construído router `/api/managers` com enriquecimento de capacidades para cada gestor detetado.
- Criados testes `backend/tests/test_managers_router.py` garantindo comportamento com e sem gestores disponíveis.
- Preparado ambiente para sincronização com ChromaDB (instalação básica, diretório `data/chromadb/` e script `scripts/chroma_sync.py`).
- Adicionada proteção `data/` ao `.gitignore` e criado sincronizador que avisa sobre dependências adicionais (`tokenizers`, `onnxruntime`, `duckdb`).
- Instaladas dependências complementares (`tokenizers`, `onnxruntime`, `duckdb`, `opentelemetry-*`, `importlib-resources`, `typer`, `bcrypt`, `chroma-hnswlib`, `kubernetes`, `grpcio`) e efetuada sincronização inicial do `LOG.md` para `data/chromadb/` com confirmação de persistência.
- Construído router `/api/managers/{id}/packages/{name}` para operações de uninstall com snapshots automáticos.
- Criados testes `backend/tests/test_packages_router.py` com stubs de queue/snapshot e verificação de erros.

### Testes
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

### Decisões
- Manter `.gitignore` e `README.md` existentes, integrando alterações via anexos/append.
- Garantir que cada módulo crítico tenha critérios de aceitação com cobertura de testes explícita.
- Registar evoluções relevantes neste `LOG.md` e persistir execuções notáveis em ChromaDB na próxima sessão.
- Validar compatibilidade dos handlers de sinal do `LockManager` em Windows/macOS antes de encerrar definitivamente a task (pendente).
- Planear smoke manual para `OperationQueue` em ambiente real após integração com endpoints.
- Capturar comandos via `sys.executable` nos testes do `CommandExecutor` para garantir portabilidade entre plataformas.
- Reforçar uso do `JSONStorage` para todas as operações persistentes que envolvam ficheiros JSON.
- Todos os adapters concretos devem herdar de `BaseAdapter` para garantir sanitização e escrita atómica homogénea.
- SnapshotManager mantém limite de retenção configurável; considerar parametrização futura via config do utilizador.
- Para operações de uninstall, criar snapshot via `SnapshotManager` antes de invocar adapters (a implementar nos routers).
- Avaliar reutilização de manifestos gerados pelos adapters nos endpoints `/snapshot` e `/managers`.
- Para ambientes multi-OS, selecionar dinamicamente adapters disponíveis (WinGet vs Brew) em runtime.
- À medida que endpoints forem adicionados, criar fixtures FastAPI partilhadas para reduzir duplicação nas suites.

### Próximos Passos
- Iniciar implementação dos endpoints backend (Task 6.x) utilizando os adapters e `OperationQueue`.
- Especificar suite de testes de integração para os routers (`/discover`, `/managers`, `/packages`, `/snapshot`).
- Validar `LockManager` em Windows/macOS antes de fechar SEC-002 e documentar fallback.
- Alimentar `ChromaDB` com este log e decisões assim que o pipeline de memória estiver operacional (pendente de tooling).
