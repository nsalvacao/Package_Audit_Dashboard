# Enhanced Logging System

Sistema de logging avançado para debugging profundo e análise de problemas no Package Audit Dashboard.

## 📋 **Visão Geral**

O sistema oferece **dois modos de logging**:

1. **Basic Logging** (Default) - Lightweight, minimal overhead
2. **Detailed Logging** (Debug) - Comprehensive request/response capture

---

## 🔧 **Configuração**

### Variáveis de Ambiente

```bash
# .env ou .env.local

# Log Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Log para ficheiro (opcional)
LOG_FILE=~/.package-audit/logs/app.log

# JSON logs (recomendado para produção)
JSON_LOGS=false

# ⚠️ DETAILED LOGGING - Apenas para debugging!
ENABLE_DETAILED_LOGGING=true
```

### Activar Detailed Logging

```bash
# Método 1: Environment variable
export ENABLE_DETAILED_LOGGING=true

# Método 2: .env file
echo "ENABLE_DETAILED_LOGGING=true" >> backend/.env

# Método 3: Inline
ENABLE_DETAILED_LOGGING=true uvicorn app.main:app --reload
```

---

## 📊 **O Que é Capturado**

### Basic Logging (Default)

```
✓ HTTP method e path
✓ Status code
✓ Request duration (ms)
```

**Exemplo de output**:
```
2025-01-26 14:30:45 | INFO     | http                           | GET /api/managers 200
  method=GET path=/api/managers status_code=200 duration_ms=45.23
```

### Detailed Logging (Debug Mode)

```
✓ Request:
  - Method, path, query params
  - Headers (sanitizados)
  - Request body (JSON ou raw)

✓ Response:
  - Status code
  - Headers (sanitizados)
  - Response body (para erros 4xx/5xx)

✓ Errors:
  - Exception type e message
  - Full stack trace
  - Request que causou o erro

✓ Timing:
  - Request duration em ms
  - Timestamps completos
```

**Exemplo de output** (JSON format):
```json
{
  "timestamp": "2025-01-26T14:30:45.123Z",
  "level": "INFO",
  "message": "→ POST /api/managers/npm/packages/lodash",
  "request_id": "1706279445123456",
  "method": "POST",
  "path": "/api/managers/npm/packages/lodash",
  "query_params": {"force": "true"},
  "headers": {
    "content-type": "application/json",
    "authorization": "***REDACTED***"
  },
  "request_body": "{\"package_name\": \"lodash\"}",
  "duration_ms": 1250.45
}
```

---

## 🔒 **Segurança - Sanitização Automática**

O sistema **automaticamente sanitiza** dados sensíveis:

### Headers Sanitizados
```python
SENSITIVE_HEADERS = {
    "authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
    "x-auth-token",
}
```

### Campos Sanitizados em Bodies
```python
SENSITIVE_FIELDS = {
    "password",
    "token",
    "secret",
    "api_key",
    "apikey",
    "auth",
    "credential",
}
```

**Exemplo**:
```json
// Request body original
{"username": "admin", "password": "secret123"}

// Logged (sanitizado)
{"username": "admin", "password": "***REDACTED***"}
```

---

## 💻 **Uso no Código - OperationLogger**

### Context Manager para Operações

```python
from app.core.enhanced_logging import OperationLogger

@router.delete("/{manager_id}/packages/{package_name}")
async def uninstall_package(manager_id: str, package_name: str):
    # Automatic timing e error handling
    async with OperationLogger(
        "uninstall_package",
        manager_id=manager_id,
        package=package_name,
    ) as op:
        # Tua operação aqui
        adapter = get_adapter_by_id(manager_id)
        result = await adapter.uninstall(package_name)

        # Adicionar contexto extra (opcional)
        op.add_context(packages_removed=result.count)

        return {"success": True}
```

**Output produzido**:
```
▶ Starting: uninstall_package
  operation=uninstall_package manager_id=npm package=lodash

✓ Completed: uninstall_package
  operation=uninstall_package manager_id=npm package=lodash
  success=True duration_ms=1245.67 packages_removed=3
```

**Se erro**:
```
▶ Starting: uninstall_package
  operation=uninstall_package manager_id=npm package=lodash

✗ Failed: uninstall_package
  operation=uninstall_package manager_id=npm package=lodash
  success=False duration_ms=234.56
  error_type=PackageNotFoundError error_message="Package 'lodash' not found"
```

---

## 🔍 **Análise de Logs**

### Formato JSON (Recomendado para Parsing)

```bash
# Activar JSON logs
JSON_LOGS=true LOG_FILE=app.log uvicorn app.main:app

# Analisar com jq
cat app.log | jq 'select(.status_code >= 400)'
cat app.log | jq 'select(.duration_ms > 1000)'
cat app.log | jq 'select(.error_type != null)'
```

### Formato Human-Readable (Development)

```bash
# Activar cores e formato legível
JSON_LOGS=false uvicorn app.main:app

# Filtrar por nível
grep "ERROR" app.log
grep "duration_ms" app.log | sort -k8 -n
```

---

## 📈 **Performance Impact**

| Mode | Overhead | Log Size | Use Case |
|------|----------|----------|----------|
| **Basic** | ~1-2ms | Minimal | Produção, monitoring |
| **Detailed** | ~5-10ms | 10-50x maior | Debugging, troubleshooting |

⚠️ **IMPORTANTE**:
- **NUNCA usar Detailed Logging em produção** sem monitorização de disco
- Logs podem crescer **muito rapidamente** (100MB+/dia em aplicações busy)
- Configurar log rotation se usar ficheiro

---

## 🛠️ **Troubleshooting Workflow**

### 1. Reproduzir Erro com Detailed Logging

```bash
# Terminal 1: Backend com detailed logging
cd backend
source .venv/bin/activate
ENABLE_DETAILED_LOGGING=true \
LOG_LEVEL=DEBUG \
LOG_FILE=debug.log \
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 2. Reproduzir Erro no Browser

- Abrir aplicação
- Reproduzir ação que causa erro
- Copiar request ID do erro (se visível)

### 3. Analisar Logs

```bash
# Ver últimas 100 linhas
tail -100 backend/debug.log

# Procurar por request específico
grep "request_id=1706279445123456" backend/debug.log

# Procurar todos os erros
grep '"level":"ERROR"' backend/debug.log | jq .

# Procurar requests lentos (>1s)
grep "duration_ms" backend/debug.log | awk '$NF > 1000'
```

### 4. Partilhar com AI para Análise

```bash
# Extrair contexto relevante (últimos 50 erros + contexto)
grep -B 5 -A 10 "ERROR" backend/debug.log | tail -500 > error_context.txt

# Enviar para Claude Code ou outro AI
# O AI pode analisar:
# - Request que causou erro
# - Response body e status
# - Stack trace completo
# - Timing info
```

---

## 📝 **Exemplos de Casos de Uso**

### Caso 1: Investigar 500 Error

```bash
# 1. Activar detailed logging
ENABLE_DETAILED_LOGGING=true uvicorn app.main:app

# 2. Reproduzir erro no browser

# 3. Procurar erro nos logs
grep "status_code=500" backend/debug.log -A 20

# Output mostra:
# - Request completo que causou 500
# - Exception type e stack trace
# - Response body com detalhes
```

### Caso 2: Debuggar CORS Issues

```bash
# Detailed logging mostra headers completos
grep "origin" backend/debug.log
grep "access-control" backend/debug.log

# Vês exactamente:
# - Origin do request
# - CORS headers na response
# - Se foi bloqueado ou permitido
```

### Caso 3: Performance Analysis

```bash
# Encontrar requests lentos
grep "duration_ms" backend/debug.log | \
  jq 'select(.duration_ms > 1000) | {path, duration_ms}' | \
  sort -k2 -n

# Output:
# {"/api/managers/npm/packages": 1245.67}
# {"/api/advanced/scan": 5432.10}
```

---

## 🎯 **Best Practices**

### ✅ **DO**

- Usar **Basic Logging em produção**
- Usar **Detailed Logging apenas para debugging**
- **Sempre usar LOG_FILE** se ENABLE_DETAILED_LOGGING=true
- **Configurar log rotation** (logrotate, ou similar)
- **Monitorizar tamanho do disco** quando detailed logging activo
- **Desactivar depois de resolver problema**

### ❌ **DON'T**

- ❌ Deixar ENABLE_DETAILED_LOGGING=true em produção
- ❌ Logar para stdout sem limite em produção
- ❌ Assumir que sanitização remove TODOS os dados sensíveis (review manualmente)
- ❌ Committar ficheiros .env com logging activo

---

## 📚 **Referência API**

### DetailedLoggingMiddleware

```python
DetailedLoggingMiddleware(
    log_request_body: bool = True,      # Log request bodies
    log_response_body: bool = True,     # Log response bodies
    log_headers: bool = True,           # Log headers
    max_body_length: int = 10000,       # Max chars to log
    exclude_paths: List[str] = [...],   # Paths to skip
)
```

### OperationLogger

```python
async with OperationLogger(
    operation_name: str,           # Nome da operação
    logger_name: str = "operations",  # Logger a usar
    **context                      # Contexto adicional
) as op:
    # ... código ...
    op.add_context(key=value)     # Adicionar contexto
```

### Funções de Sanitização

```python
from app.core.enhanced_logging import sanitize_data, sanitize_headers

# Sanitizar dict/list
clean_data = sanitize_data({"password": "secret"})
# → {"password": "***REDACTED***"}

# Sanitizar headers
clean_headers = sanitize_headers({"authorization": "Bearer token"})
# → {"authorization": "***REDACTED***"}
```

---

## 🔗 **Integração com Outras Ferramentas**

### Sentry (Future)

```python
# Logs automáticamente enviados para Sentry se configurado
# Breadcrumbs incluem:
# - Request details
# - User context
# - Tags com manager_id, operation, etc.
```

### Elasticsearch/Logstash (Future)

```bash
# JSON logs são ELK-ready
# Filebeat pode ingerir directamente
```

### CloudWatch/Azure Monitor (Future)

```bash
# Structured logs compatíveis com cloud logging
```

---

## 📞 **Support**

- **Bugs**: Criar issue no GitHub com logs relevantes
- **Features**: Discussão no GitHub Discussions
- **Security**: Email privado (nunca logs públicos!)

---

**Última Actualização**: 2025-01-26
**Versão**: 0.3.0
