# 🚀 Fase 1 - Breakdown de Implementação

## Visão Geral da Fase 1

**Objetivo**: MVP seguro e funcional
**Duração**: 1-2 semanas
**Prioridade**: Segurança em primeiro lugar

**Entregáveis**:
- ✅ Dashboard funcional que lista pacotes
- ✅ Desinstalar pacotes com confirmação
- ✅ PATH validation com script generation
- ✅ Snapshot automático antes de uninstall
- ✅ Proteção contra command injection e race conditions

---

## 📋 Task List Overview

### Setup & Infrastructure (Tasks 1-3)
- [ ] Task 1.1: Criar estrutura do projeto
- [ ] Task 1.2: Setup Backend (FastAPI)
- [ ] Task 1.3: Setup Frontend (React + Vite)

### Security Layer - CRÍTICO (Tasks 4-6)
- [ ] Task 2.1: Implementar ValidationLayer
- [ ] Task 2.2: Implementar LockManager
- [ ] Task 2.3: Implementar OperationQueue

### Core Backend (Tasks 7-10)
- [ ] Task 3.1: Implementar CommandExecutor
- [ ] Task 3.2: Implementar JSON Storage
- [ ] Task 3.3: Implementar BaseAdapter Interface
- [ ] Task 3.4: Implementar SnapshotManager (básico)

### Adapters (Tasks 11-13)
- [ ] Task 4.1: Implementar NpmAdapter
- [ ] Task 4.2: Implementar PipAdapter
- [ ] Task 4.3: Implementar WinGetAdapter/BrewAdapter

### PATH Validation (Tasks 14-16)
- [ ] Task 5.1: Implementar PathValidator
- [ ] Task 5.2: Criar script generators
- [ ] Task 5.3: Endpoints PATH validation

### API Endpoints (Tasks 17-21)
- [ ] Task 6.1: Endpoint /discover
- [ ] Task 6.2: Endpoint /managers
- [ ] Task 6.3: Endpoint /packages (uninstall)
- [ ] Task 6.4: Endpoint /path
- [ ] Task 6.5: Endpoint /snapshot

### Frontend Core (Tasks 22-27)
- [ ] Task 7.1: Setup Layout & Routing
- [ ] Task 7.2: Implementar Dashboard
- [ ] Task 7.3: Implementar ManagerCard
- [ ] Task 7.4: Implementar PackageTable
- [ ] Task 7.5: Implementar ConfirmationModal
- [ ] Task 7.6: Implementar PathSetupGuide

### Testing (Tasks 28-30)
- [ ] Task 8.1: Testes ValidationLayer
- [ ] Task 8.2: Testes LockManager
- [ ] Task 8.3: Testes Adapters

**Checklist adicional de cobertura obrigatória**:
- [ ] CommandExecutor – simular timeout, falhas de retorno, execução assíncrona
- [ ] OperationQueue – cenários de concorrência (read vs mutation), bloqueio e desbloqueio
- [ ] Adapters NPM/Pip – mocks de comandos, parsing de saída, regressões de erro
- [ ] Endpoints críticos – smoke tests `/packages` (uninstall) e `/snapshot`

### Documentation (Tasks 31-33)
- [ ] Task 9.1: SECURITY.md
- [ ] Task 9.2: LIMITATIONS.md
- [ ] Task 9.3: SETUP_PATH.md

## ⏱️ Cronograma Sprint Fase 1 (5 dias úteis)

- **Dia 1 – Preparação & Infraestrutura**: criar diretórios base, configurar tooling inicial (venv, npm, lint/test placeholders), preparar scripts auxiliares em `scripts/setup/`, validar que `.gitignore` e `README.md` mantêm histórico.
- **Dia 2 – Camada de Segurança**: implementar `ValidationLayer`, iniciar `LockManager`, definir stubs de testes com cobertura mínima acordada, escrever notas sobre compatibilidade multi-plataforma.
- **Dia 3 – Core Backend**: finalizar `LockManager`, desenvolver `OperationQueue` com testes assíncronos, criar `CommandExecutor` com harness de timeout, iniciar abstrações de storage/snapshot.
- **Dia 4 – API & Frontend MVP**: expor endpoints principais (`/discover`, `/managers`, `/packages`, `/path`, `/snapshot`), construir layout React com componentes principais e estados mockados.
- **Dia 5 – Qualidade & Documentação**: reforçar testes (CommandExecutor, OperationQueue, adapters), produzir `SECURITY.md`, `LIMITATIONS.md`, `SETUP_PATH.md`, preparar smoke manual e backlog Fase 2.

---

## 🏗️ Task Detalhado

---

## SETUP & INFRASTRUCTURE

### Task 1.1: Criar Estrutura do Projeto

**ID**: SETUP-001
**Prioridade**: CRÍTICA
**Duração**: 30min
**Dependências**: Nenhuma

**Descrição**:
Criar estrutura completa de pastas e ficheiros iniciais do projeto.

> **Boas práticas**: sempre que possível, encapsular comandos repetíveis em scripts (`scripts/setup/`) para garantir reprodutibilidade e evitar sobrescritas acidentais.

**Nota**: Trabalhar diretamente na raiz do repositório (`Package_Audit_Dashboard/`) — evitar criar diretório adicional com o mesmo nome.

**Estrutura a Criar**:
```
frontend/
├── src/
│   ├── components/
│   ├── hooks/
│   ├── store/
│   ├── types/
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── tsconfig.json
├── vite.config.ts
└── index.html

backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routers/
│   │   └── __init__.py
│   ├── adapters/
│   │   └── __init__.py
│   ├── analysis/
│   │   └── __init__.py
│   ├── core/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   └── storage/
│       └── __init__.py
├── tests/
│   └── __init__.py
├── requirements.txt
└── pyproject.toml

cli/
└── audit_cli/
    └── __init__.py

docs/
└── README.md

.gitignore
README.md
LICENSE
```

**Comandos**:
```bash
# Criar estrutura base (ignorar diretórios já existentes)
mkdir -p frontend/src/{components,hooks,store,types}
mkdir -p backend/app/{routers,adapters,analysis,core,models,storage}
mkdir -p backend/tests cli/audit_cli docs
mkdir -p scripts/setup

# Garantir ficheiros __init__.py
touch backend/app/__init__.py \
      backend/app/routers/__init__.py \
      backend/app/adapters/__init__.py \
      backend/app/analysis/__init__.py \
      backend/app/core/__init__.py \
      backend/app/models/__init__.py \
      backend/app/storage/__init__.py \
      backend/tests/__init__.py \
      cli/audit_cli/__init__.py

# Atualizar .gitignore existente (merge manual, não substituir)
cat > scripts/setup/gitignore.append <<'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
*.egg-info/
dist/
build/

# Node
node_modules/
dist/
.cache/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# App specific
.package-audit/
*.lock
.cache/
EOF

# Revisar e incorporar manualmente:
cat scripts/setup/gitignore.append

# Acrescentar secção de setup ao README atual (apenas se faltar)
cat >> README.md <<'EOF'

## Desenvolvimento Rápido

### Backend
\`\`\`bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
\`\`\`

### Frontend
\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`
EOF
```

> **Nota**: Rever diffs antes de confirmar — manter conteúdos existentes em `.gitignore` e `README.md`, integrando apenas as entradas/sectores em falta. Para automação futura, planear script em `scripts/setup/bootstrap_structure.py` que gere ficheiros auxiliares (ex.: `gitignore.append`) em vez de sobrescrever diretamente.

**Critérios de Aceitação**:
- [ ] Estrutura de pastas criada
- [ ] .gitignore atualizado sem substituir conteúdo existente
- [ ] README.md enriquecido mantendo secções já existentes
- [ ] Todos os __init__.py criados
- [ ] Scripts auxiliares prontos em `scripts/setup/`

---

### Task 1.2: Setup Backend (FastAPI)

**ID**: SETUP-002
**Prioridade**: CRÍTICA
**Duração**: 1h
**Dependências**: SETUP-001

**Ficheiros a Criar**:
1. `backend/requirements.txt`
2. `backend/pyproject.toml`
3. `backend/app/main.py`
4. `backend/app/models/schemas.py`

**1. requirements.txt**:
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
aiofiles==23.2.1
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

**2. pyproject.toml**:
```toml
[project]
name = "package-audit-dashboard"
version = "0.1.0"
description = "Package manager audit and management dashboard"
requires-python = ">=3.10"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
```

**3. backend/app/main.py**:
```python
"""
Package Audit Dashboard - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup/shutdown
    """
    logger.info("Starting Package Audit Dashboard API...")
    
    # Startup: Initialize storage directories
    from pathlib import Path
    storage_dir = Path.home() / ".package-audit"
    storage_dir.mkdir(exist_ok=True)
    (storage_dir / "snapshots").mkdir(exist_ok=True)
    (storage_dir / "logs").mkdir(exist_ok=True)
    
    logger.info(f"Storage directory: {storage_dir}")
    
    yield
    
    # Shutdown: Cleanup
    logger.info("Shutting down...")

# Create FastAPI app
app = FastAPI(
    title="Package Audit Dashboard API",
    description="API for auditing and managing package managers",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "name": "Package Audit Dashboard API",
        "version": "0.1.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Router imports will be added here
# from app.routers import discovery, managers, packages, path, snapshot
# app.include_router(discovery.router)
# app.include_router(managers.router)
# app.include_router(packages.router)
# app.include_router(path.router)
# app.include_router(snapshot.router)
```

**4. backend/app/models/schemas.py**:
```python
"""
Pydantic models for API request/response
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class PackageStatus(str, Enum):
    """Package status enumeration"""
    UP_TO_DATE = "up-to-date"
    OUTDATED = "outdated"
    VULNERABLE = "vulnerable"
    UNKNOWN = "unknown"

class Package(BaseModel):
    """Package model"""
    name: str
    version: str
    latest: Optional[str] = None
    status: PackageStatus = PackageStatus.UNKNOWN
    is_global: bool = True
    size_mb: Optional[float] = None
    installed_date: Optional[datetime] = None

class ManagerInfo(BaseModel):
    """Package manager information"""
    id: str
    name: str
    installed: bool
    version: Optional[str] = None
    path: Optional[str] = None
    package_count: int = 0

class DiscoveryResponse(BaseModel):
    """Discovery scan response"""
    managers: List[ManagerInfo]
    scan_duration_ms: int
    timestamp: datetime = Field(default_factory=datetime.now)

class UninstallRequest(BaseModel):
    """Uninstall package request"""
    manager: str
    package: str
    force: bool = False

class UninstallResponse(BaseModel):
    """Uninstall operation response"""
    success: bool
    message: str
    snapshot_id: Optional[str] = None

class PathValidationResult(BaseModel):
    """PATH validation result"""
    manager: str
    in_path: bool
    executable_path: Optional[str] = None
    missing_paths: List[str] = []

class PathValidationResponse(BaseModel):
    """PATH validation response"""
    results: List[PathValidationResult]
    all_valid: bool

class ScriptGenerationRequest(BaseModel):
    """Script generation request"""
    shell: str = Field(default="bash", pattern="^(bash|powershell|fish|zsh)$")

class ScriptGenerationResponse(BaseModel):
    """Script generation response"""
    script: str
    shell: str
    instructions: str

class SnapshotInfo(BaseModel):
    """Snapshot information"""
    id: str
    timestamp: datetime
    size_mb: float
    package_count: int
    managers: List[str]

class SnapshotCreateResponse(BaseModel):
    """Snapshot creation response"""
    snapshot_id: str
    created_at: datetime
    size_mb: float

class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
```

**Comandos para Testar**:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Em outro terminal
curl http://localhost:8000/health
# Deve retornar: {"status":"healthy"}
```

**Critérios de Aceitação**:
- [ ] requirements.txt criado
- [ ] Backend inicia sem erros
- [ ] Endpoint /health responde
- [ ] CORS configurado
- [ ] Storage directories criados automaticamente
- [ ] Logs funcionam

---

### Task 1.3: Setup Frontend (React + Vite)

**ID**: SETUP-003
**Prioridade**: CRÍTICA
**Duração**: 1h
**Dependências**: SETUP-001

**Ficheiros a Criar**:
1. `frontend/package.json`
2. `frontend/vite.config.ts`
3. `frontend/tsconfig.json`
4. `frontend/index.html`
5. `frontend/src/main.tsx`
6. `frontend/src/App.tsx`
7. `frontend/src/types/api.ts`

**1. package.json**:
```json
{
  "name": "package-audit-dashboard-frontend",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@tanstack/react-query": "^5.8.4",
    "zustand": "^4.4.6",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@typescript-eslint/eslint-plugin": "^6.10.0",
    "@typescript-eslint/parser": "^6.10.0",
    "@vitejs/plugin-react": "^4.2.0",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.53.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.4",
    "postcss": "^8.4.31",
    "tailwindcss": "^3.3.5",
    "typescript": "^5.2.2",
    "vite": "^5.0.0"
  }
}
```

**2. vite.config.ts**:
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

**3. tsconfig.json**:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

**4. index.html**:
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Package Audit Dashboard</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

**5. src/main.tsx**:
```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App'
import './index.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>,
)
```

**6. src/App.tsx**:
```typescript
import { useState } from 'react'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4">
          <h1 className="text-3xl font-bold text-gray-900">
            Package Audit Dashboard
          </h1>
        </div>
      </header>
      <main className="max-w-7xl mx-auto py-6 px-4">
        <div className="bg-white shadow rounded-lg p-6">
          <p className="text-gray-600">
            Dashboard is loading... Setup in progress.
          </p>
        </div>
      </main>
    </div>
  )
}

export default App
```

**7. src/types/api.ts**:
```typescript
/**
 * API types - matches backend schemas
 */

export type PackageStatus = 'up-to-date' | 'outdated' | 'vulnerable' | 'unknown'

export interface Package {
  name: string
  version: string
  latest?: string
  status: PackageStatus
  is_global: boolean
  size_mb?: number
  installed_date?: string
}

export interface ManagerInfo {
  id: string
  name: string
  installed: boolean
  version?: string
  path?: string
  package_count: number
}

export interface DiscoveryResponse {
  managers: ManagerInfo[]
  scan_duration_ms: number
  timestamp: string
}

export interface UninstallRequest {
  manager: string
  package: string
  force?: boolean
}

export interface UninstallResponse {
  success: boolean
  message: string
  snapshot_id?: string
}

export interface PathValidationResult {
  manager: string
  in_path: boolean
  executable_path?: string
  missing_paths: string[]
}

export interface PathValidationResponse {
  results: PathValidationResult[]
  all_valid: boolean
}

export interface ErrorResponse {
  error: string
  detail?: string
  code?: string
}
```

**8. src/index.css** (Tailwind):
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**9. tailwind.config.js**:
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**10. postcss.config.js**:
```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

**Comandos para Setup**:
```bash
cd frontend
npm install
npm run dev

# Frontend disponível em http://localhost:5173
```

**Critérios de Aceitação**:
- [ ] npm install sem erros
- [ ] Frontend inicia em localhost:5173
- [ ] TypeScript compila sem erros
- [ ] Tailwind CSS funciona
- [ ] Proxy para backend configurado
- [ ] React Query configurado

---

## SECURITY LAYER - CRÍTICO

### Task 2.1: Implementar ValidationLayer

**ID**: SEC-001
**Prioridade**: CRÍTICA (BLOCKER)
**Duração**: 2h
**Dependências**: SETUP-002

**Ficheiro**: `backend/app/core/validation.py`

```python
"""
ValidationLayer - Security module for input validation and command safety

CRITICAL: This module prevents:
- Command injection attacks
- Path traversal attacks
- Malformed package names

All user inputs MUST pass through this layer before execution.
"""
import re
import os
from typing import List
from pathlib import Path

class InvalidPackageNameError(ValueError):
    """Raised when package name fails validation"""
    pass

class PathTraversalError(ValueError):
    """Raised when path tries to escape allowed directory"""
    pass

class ValidationLayer:
    """
    Input validation and sanitization layer.
    
    CRITICAL SECURITY MODULE - DO NOT MODIFY WITHOUT SECURITY REVIEW
    """
    
    # Package name whitelist: alphanumeric + @/_.-
    # Covers: npm (@scope/package), pip (package-name), etc.
    PACKAGE_NAME_REGEX = re.compile(r'^[a-zA-Z0-9@/_.-]+$')
    
    # npm limit is 214, we use same
    MAX_PACKAGE_NAME_LENGTH = 214
    
    # Allowed base directories for file operations
    ALLOWED_BASE_DIR = Path.home() / ".package-audit"
    
    @staticmethod
    def sanitize_package_name(name: str) -> str:
        """
        Validate and sanitize package name.
        
        Args:
            name: Package name from user input
            
        Returns:
            Sanitized package name
            
        Raises:
            InvalidPackageNameError: If name is invalid
            
        Examples:
            >>> ValidationLayer.sanitize_package_name("react")
            'react'
            >>> ValidationLayer.sanitize_package_name("@types/node")
            '@types/node'
            >>> ValidationLayer.sanitize_package_name("lodash; rm -rf /")
            InvalidPackageNameError
        """
        if not name:
            raise InvalidPackageNameError("Package name cannot be empty")
        
        if len(name) > ValidationLayer.MAX_PACKAGE_NAME_LENGTH:
            raise InvalidPackageNameError(
                f"Package name too long (max {ValidationLayer.MAX_PACKAGE_NAME_LENGTH}): {name}"
            )
        
        if not ValidationLayer.PACKAGE_NAME_REGEX.match(name):
            raise InvalidPackageNameError(
                f"Package name contains invalid characters: {name}"
            )
        
        return name
    
    @staticmethod
    def build_safe_command(base_cmd: List[str], args: List[str]) -> List[str]:
        """
        Build command array for subprocess.run()
        
        CRITICAL: ALWAYS returns list, NEVER string
        NEVER use shell=True with this output
        
        Args:
            base_cmd: Base command (e.g., ["npm", "uninstall"])
            args: Arguments to append (e.g., ["react"])
            
        Returns:
            Complete command as list
            
        Example:
            >>> ValidationLayer.build_safe_command(
            ...     ["npm", "uninstall"],
            ...     ["react"]
            ... )
            ['npm', 'uninstall', 'react']
        """
        if not isinstance(base_cmd, list):
            raise TypeError("base_cmd must be a list")
        
        if not isinstance(args, list):
            raise TypeError("args must be a list")
        
        # Sanitize all arguments
        sanitized_args = [
            ValidationLayer.sanitize_package_name(arg)
            for arg in args
        ]
        
        return base_cmd + sanitized_args
    
    @staticmethod
    def validate_path(path: str) -> Path:
        """
        Validate path to prevent traversal attacks.
        
        Args:
            path: Path from user input
            
        Returns:
            Validated Path object
            
        Raises:
            PathTraversalError: If path escapes allowed directory
            
        Example:
            >>> ValidationLayer.validate_path("snapshots/test.json")
            Path('/home/user/.package-audit/snapshots/test.json')
            >>> ValidationLayer.validate_path("../../etc/passwd")
            PathTraversalError
        """
        # Resolve to absolute path
        full_path = Path(path)
        if not full_path.is_absolute():
            full_path = ValidationLayer.ALLOWED_BASE_DIR / path
        
        # Resolve symlinks and relative paths
        real_path = full_path.resolve()
        
        # Ensure it's within allowed directory
        try:
            real_path.relative_to(ValidationLayer.ALLOWED_BASE_DIR)
        except ValueError:
            raise PathTraversalError(
                f"Path outside allowed directory: {path}"
            )
        
        return real_path
    
    @staticmethod
    def sanitize_manager_id(manager_id: str) -> str:
        """
        Validate package manager ID.
        
        Args:
            manager_id: Manager ID (e.g., "npm", "pip")
            
        Returns:
            Sanitized manager ID
            
        Raises:
            InvalidPackageNameError: If ID is invalid
        """
        # Manager IDs should be simple alphanumeric
        if not re.match(r'^[a-z][a-z0-9_-]*$', manager_id):
            raise InvalidPackageNameError(
                f"Invalid manager ID: {manager_id}"
            )
        
        if len(manager_id) > 50:
            raise InvalidPackageNameError(
                f"Manager ID too long: {manager_id}"
            )
        
        return manager_id
```

**Ficheiro de Testes**: `backend/tests/test_validation.py`

```python
"""
Tests for ValidationLayer - 100% coverage required
"""
import pytest
from pathlib import Path
from app.core.validation import (
    ValidationLayer,
    InvalidPackageNameError,
    PathTraversalError
)

class TestPackageNameSanitization:
    """Test package name validation"""
    
    def test_valid_simple_name(self):
        """Test valid simple package name"""
        assert ValidationLayer.sanitize_package_name("react") == "react"
    
    def test_valid_scoped_name(self):
        """Test valid scoped npm package"""
        assert ValidationLayer.sanitize_package_name("@types/node") == "@types/node"
    
    def test_valid_with_hyphen(self):
        """Test package name with hyphen"""
        assert ValidationLayer.sanitize_package_name("lodash-es") == "lodash-es"
    
    def test_valid_with_underscore(self):
        """Test package name with underscore"""
        assert ValidationLayer.sanitize_package_name("test_package") == "test_package"
    
    def test_reject_shell_injection(self):
        """Test rejection of shell injection attempt"""
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.sanitize_package_name("lodash; rm -rf /")
    
    def test_reject_pipe_injection(self):
        """Test rejection of pipe injection"""
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.sanitize_package_name("lodash | cat /etc/passwd")
    
    def test_reject_path_traversal_in_name(self):
        """Test rejection of path traversal"""
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.sanitize_package_name("../../etc/passwd")
    
    def test_reject_empty_name(self):
        """Test rejection of empty name"""
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.sanitize_package_name("")
    
    def test_reject_too_long_name(self):
        """Test rejection of name exceeding length limit"""
        long_name = "a" * 300
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.sanitize_package_name(long_name)
    
    def test_reject_special_characters(self):
        """Test rejection of special characters"""
        invalid_names = [
            "package$name",
            "package#name",
            "package name",  # space
            "package\nname",  # newline
            "package;name",
        ]
        for name in invalid_names:
            with pytest.raises(InvalidPackageNameError):
                ValidationLayer.sanitize_package_name(name)

class TestCommandBuilding:
    """Test safe command building"""
    
    def test_build_simple_command(self):
        """Test building simple command"""
        cmd = ValidationLayer.build_safe_command(
            ["npm", "uninstall"],
            ["react"]
        )
        assert cmd == ["npm", "uninstall", "react"]
        assert isinstance(cmd, list)
    
    def test_build_multiple_args(self):
        """Test building command with multiple args"""
        cmd = ValidationLayer.build_safe_command(
            ["npm", "install"],
            ["react", "vue", "angular"]
        )
        assert cmd == ["npm", "install", "react", "vue", "angular"]
    
    def test_reject_invalid_arg(self):
        """Test rejection of invalid argument"""
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.build_safe_command(
                ["npm", "install"],
                ["react", "lodash; rm -rf /"]
            )
    
    def test_require_list_base_cmd(self):
        """Test that base_cmd must be list"""
        with pytest.raises(TypeError):
            ValidationLayer.build_safe_command(
                "npm install",  # string instead of list
                ["react"]
            )
    
    def test_require_list_args(self):
        """Test that args must be list"""
        with pytest.raises(TypeError):
            ValidationLayer.build_safe_command(
                ["npm", "install"],
                "react"  # string instead of list
            )

class TestPathValidation:
    """Test path validation"""
    
    def test_valid_relative_path(self):
        """Test valid relative path"""
        path = ValidationLayer.validate_path("snapshots/test.json")
        assert isinstance(path, Path)
        assert ".package-audit" in str(path)
    
    def test_valid_absolute_path(self):
        """Test valid absolute path within allowed dir"""
        base = ValidationLayer.ALLOWED_BASE_DIR
        test_path = base / "snapshots" / "test.json"
        result = ValidationLayer.validate_path(str(test_path))
        assert result == test_path
    
    def test_reject_traversal_up(self):
        """Test rejection of .. traversal"""
        with pytest.raises(PathTraversalError):
            ValidationLayer.validate_path("../../etc/passwd")
    
    def test_reject_absolute_outside(self):
        """Test rejection of absolute path outside allowed dir"""
        with pytest.raises(PathTraversalError):
            ValidationLayer.validate_path("/etc/passwd")

class TestManagerIdSanitization:
    """Test manager ID validation"""
    
    def test_valid_simple_id(self):
        """Test valid simple manager ID"""
        assert ValidationLayer.sanitize_manager_id("npm") == "npm"
    
    def test_valid_with_hyphen(self):
        """Test manager ID with hyphen"""
        assert ValidationLayer.sanitize_manager_id("pip-tools") == "pip-tools"
    
    def test_reject_uppercase(self):
        """Test rejection of uppercase"""
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.sanitize_manager_id("NPM")
    
    def test_reject_special_chars(self):
        """Test rejection of special characters"""
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.sanitize_manager_id("npm;rm")
    
    def test_reject_too_long(self):
        """Test rejection of too long ID"""
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.sanitize_manager_id("a" * 100)
```

**Comandos para Testar**:
```bash
cd backend
pytest tests/test_validation.py -v --cov=app.core.validation
# Deve ter 100% coverage
```

**Critérios de Aceitação**:
- [ ] ValidationLayer implementado
- [ ] Todos os testes passam
- [ ] Coverage = 100%
- [ ] Rejeita command injection
- [ ] Rejeita path traversal
- [ ] Retorna sempre lista (nunca string)

---

### Task 2.2: Implementar LockManager

**ID**: SEC-002
**Prioridade**: CRÍTICA (BLOCKER)
**Duração**: 2h
**Dependências**: SETUP-002

**Ficheiro**: `backend/app/core/locking.py`

```python
"""
LockManager - Prevents race conditions in concurrent operations

CRITICAL: This module ensures:
- Only one mutation operation at a time
- Safe concurrent reads
- Automatic cleanup on crash
- Stale lock detection
"""
import os
import json
import time
import atexit
import signal
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict

class OperationInProgressError(Exception):
    """Raised when operation is blocked by existing lock"""
    pass

class LockManager:
    """
    File-based lock manager for operation serialization.
    
Features:
- Prevents race conditions
- Auto-cleanup on process exit
- Stale lock detection (30s timeout)
- Lock info tracking

⚠️ **Compatibilidade**: verificar `signal.signal` no Windows/macOS; definir fallback/documentação caso os handlers tenham de ser registados apenas no processo principal ou substituídos por mecanismos alternativos.
    """
    
    LOCK_FILE = Path.home() / ".package-audit" / ".lock"
    TIMEOUT = 30  # seconds
    
    def __init__(self):
        """Initialize lock manager"""
        # Ensure storage directory exists
        self.LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        # Register cleanup handlers
        atexit.register(self._cleanup_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def acquire_lock(self, operation_id: str) -> bool:
        """
        Attempt to acquire lock for operation.
        
        Args:
            operation_id: Unique identifier for operation
            
        Returns:
            True if lock acquired, False if already locked
            
        Example:
            >>> lock = LockManager()
            >>> if lock.acquire_lock("uninstall:npm:react"):
            ...     # Perform operation
            ...     lock.release_lock()
        """
        # Check if already locked
        if self.is_locked() and not self.is_stale():
            return False
        
        # Clean stale lock
        if self.is_stale():
            self.release_lock()
        
        # Create new lock
        lock_data = {
            "operation": operation_id,
            "pid": os.getpid(),
            "timestamp": datetime.now().isoformat(),
            "hostname": os.uname().nodename if hasattr(os, 'uname') else "unknown"
        }
        
        try:
            with open(self.LOCK_FILE, 'w') as f:
                json.dump(lock_data, f, indent=2)
            return True
        except Exception as e:
            # Failed to create lock
            return False
    
    def release_lock(self) -> bool:
        """
        Release lock if owned by current process.
        
        Returns:
            True if released, False if not owned or doesn't exist
        """
        if not self.is_locked():
            return False
        
        try:
            lock_data = self.get_lock_info()
            
            # Only release if owned by current process
            if lock_data and lock_data.get("pid") == os.getpid():
                self.LOCK_FILE.unlink()
                return True
            
            return False
        except Exception:
            return False
    
    def is_locked(self) -> bool:
        """
        Check if lock file exists.
        
        Returns:
            True if locked
        """
        return self.LOCK_FILE.exists()
    
    def is_stale(self) -> bool:
        """
        Check if lock is older than TIMEOUT.
        
        A stale lock indicates the process crashed without cleanup.
        
        Returns:
            True if lock is stale
        """
        if not self.is_locked():
            return False
        
        try:
            lock_data = self.get_lock_info()
            if not lock_data:
                return True  # Corrupted = stale
            
            lock_time = datetime.fromisoformat(lock_data["timestamp"])
            age = (datetime.now() - lock_time).total_seconds()
            
            return age > self.TIMEOUT
        except (KeyError, ValueError):
            return True  # Corrupted = stale
    
    def get_lock_info(self) -> Optional[Dict]:
        """
        Get information about current lock.
        
        Returns:
            Lock data dict or None if not locked
        """
        if not self.is_locked():
            return None
        
        try:
            with open(self.LOCK_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    def wait_for_lock(
        self,
        operation_id: str,
        max_wait: int = 60,
        poll_interval: float = 0.5
    ) -> bool:
        """
        Wait for lock to become available.
        
        Args:
            operation_id: Operation identifier
            max_wait: Maximum seconds to wait
            poll_interval: Seconds between checks
            
        Returns:
            True if acquired, False if timeout
        """
        start = time.time()
        
        while time.time() - start < max_wait:
            if self.acquire_lock(operation_id):
                return True
            time.sleep(poll_interval)
        
        return False
    
    def force_release(self):
        """
        Force release lock regardless of owner.
        
        WARNING: Use only for admin cleanup, not normal operations.
        """
        if self.LOCK_FILE.exists():
            self.LOCK_FILE.unlink()
    
    def _cleanup_handler(self):
        """Cleanup handler for atexit"""
        self.release_lock()
    
    def _signal_handler(self, signum, frame):
        """Signal handler for SIGTERM/SIGINT"""
        self.release_lock()
        raise SystemExit(0)

# Global instance
_lock_manager = None

def get_lock_manager() -> LockManager:
    """
    Get global lock manager instance (singleton).
    
    Returns:
        LockManager instance
    """
    global _lock_manager
    if _lock_manager is None:
        _lock_manager = LockManager()
    return _lock_manager
```

**Ficheiro de Testes**: `backend/tests/test_locking.py`

```python
"""
Tests for LockManager - 100% coverage required
"""
import pytest
import time
import json
from pathlib import Path
from datetime import datetime, timedelta
from app.core.locking import LockManager, OperationInProgressError

@pytest.fixture
def lock_manager(tmp_path):
    """Create lock manager with temporary lock file"""
    lock_file = tmp_path / ".lock"
    
    # Monkey patch LOCK_FILE
    original_lock_file = LockManager.LOCK_FILE
    LockManager.LOCK_FILE = lock_file
    
    manager = LockManager()
    
    yield manager
    
    # Cleanup
    if lock_file.exists():
        lock_file.unlink()
    
    # Restore
    LockManager.LOCK_FILE = original_lock_file

class TestLockAcquisition:
    """Test lock acquisition"""
    
    def test_acquire_lock_success(self, lock_manager):
        """Test successful lock acquisition"""
        assert lock_manager.acquire_lock("test_operation")
        assert lock_manager.is_locked()
    
    def test_acquire_lock_blocked(self, lock_manager):
        """Test lock acquisition blocked by existing lock"""
        assert lock_manager.acquire_lock("operation1")
        assert not lock_manager.acquire_lock("operation2")
    
    def test_release_lock(self, lock_manager):
        """Test lock release"""
        lock_manager.acquire_lock("test")
        assert lock_manager.release_lock()
        assert not lock_manager.is_locked()
    
    def test_release_without_lock(self, lock_manager):
        """Test release when not locked"""
        assert not lock_manager.release_lock()

class TestStaleLock:
    """Test stale lock detection"""
    
    def test_detect_stale_lock(self, lock_manager):
        """Test stale lock detection"""
        # Acquire lock
        lock_manager.acquire_lock("test")
        
        # Manually set old timestamp
        lock_data = lock_manager.get_lock_info()
        old_time = datetime.now() - timedelta(seconds=60)
        lock_data["timestamp"] = old_time.isoformat()
        
        with open(lock_manager.LOCK_FILE, 'w') as f:
            json.dump(lock_data, f)
        
        # Should be stale
        assert lock_manager.is_stale()
    
    def test_acquire_over_stale_lock(self, lock_manager):
        """Test acquiring over stale lock"""
        # Create stale lock
        lock_data = {
            "operation": "old_operation",
            "pid": 99999,
            "timestamp": (datetime.now() - timedelta(seconds=60)).isoformat()
        }
        with open(lock_manager.LOCK_FILE, 'w') as f:
            json.dump(lock_data, f)
        
        # Should be able to acquire
        assert lock_manager.acquire_lock("new_operation")

class TestLockInfo:
    """Test lock information"""
    
    def test_get_lock_info(self, lock_manager):
        """Test getting lock info"""
        lock_manager.acquire_lock("test_op")
        info = lock_manager.get_lock_info()
        
        assert info is not None
        assert info["operation"] == "test_op"
        assert "pid" in info
        assert "timestamp" in info
    
    def test_get_lock_info_when_not_locked(self, lock_manager):
        """Test getting info when not locked"""
        assert lock_manager.get_lock_info() is None

class TestWaitForLock:
    """Test waiting for lock"""
    
    def test_wait_succeeds_immediately(self, lock_manager):
        """Test wait succeeds when lock available"""
        assert lock_manager.wait_for_lock("test", max_wait=1)
    
    def test_wait_timeout(self, lock_manager):
        """Test wait times out"""
        # Acquire lock first
        lock_manager.acquire_lock("blocking")
        
        # Try to acquire (should timeout)
        assert not lock_manager.wait_for_lock("test", max_wait=1)

class TestConcurrency:
    """Test concurrent access patterns"""
    
    def test_sequential_operations(self, lock_manager):
        """Test sequential operations work"""
        # Operation 1
        assert lock_manager.acquire_lock("op1")
        lock_manager.release_lock()
        
        # Operation 2
        assert lock_manager.acquire_lock("op2")
        lock_manager.release_lock()
```

**Comandos para Testar**:
```bash
cd backend
pytest tests/test_locking.py -v --cov=app.core.locking
# Deve ter 100% coverage
```

**Critérios de Aceitação**:
- [ ] LockManager implementado
- [ ] Todos os testes passam
- [ ] Coverage = 100%
- [ ] Deteta locks stale
- [ ] Auto-cleanup on exit
- [ ] Previne race conditions
- [ ] Handlers de sinal validados em Windows/macOS (fallback documentado se necessário)

---

### Task 2.3: Implementar OperationQueue

**ID**: SEC-003
**Prioridade**: ALTA
**Duração**: 1.5h
**Dependências**: SEC-002

**Ficheiro**: `backend/app/core/queue.py`

```python
"""
OperationQueue - Serial execution of mutation operations

Ensures mutations (install, uninstall, update) run one at a time.
Reads can run concurrently.
"""
import asyncio
from typing import Callable, Any, Coroutine
from enum import Enum
from app.core.locking import get_lock_manager

class OperationType(Enum):
    """Operation type classification"""
    READ = "read"      # Can run concurrently
    MUTATION = "mutation"  # Must run serially

class OperationQueue:
    """
    Queue for managing operation execution.
    
    Features:
    - Mutations run serially (using LockManager)
    - Reads run concurrently
    - Cancel pending operations
    """
    
    def __init__(self):
        self.lock_manager = get_lock_manager()
    
    async def execute(
        self,
        operation_id: str,
        operation_type: OperationType,
        func: Callable[..., Coroutine[Any, Any, Any]],
        *args,
        **kwargs
    ) -> Any:
        """
        Execute operation with proper synchronization.
        
        Args:
            operation_id: Unique identifier
            operation_type: READ or MUTATION
            func: Async function to execute
            *args, **kwargs: Arguments for func
            
        Returns:
            Result from func
            
        Raises:
            OperationInProgressError: If mutation blocked by lock
        """
        if operation_type == OperationType.READ:
            # Reads can run concurrently
            return await func(*args, **kwargs)
        
        else:  # MUTATION
            # Acquire lock for mutations
            if not self.lock_manager.acquire_lock(operation_id):
                lock_info = self.lock_manager.get_lock_info()
                raise OperationInProgressError(
                    f"Operation blocked by: {lock_info['operation']}"
                )
            
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                self.lock_manager.release_lock()

# Global instance
_queue = None

def get_operation_queue() -> OperationQueue:
    """Get global operation queue instance"""
    global _queue
    if _queue is None:
        _queue = OperationQueue()
    return _queue
```

**Critérios de Aceitação**:
- [ ] OperationQueue implementado
- [ ] Integra com LockManager
- [ ] Mutations serializadas
- [ ] Reads concorrentes
- [ ] Testes unitários cobrindo sucesso, bloqueio e propagação de erros

---

## CORE BACKEND

### Task 3.1: Implementar CommandExecutor

**ID**: CORE-001
**Prioridade**: CRÍTICA
**Duração**: 1.5h
**Dependências**: SEC-001

**Ficheiro**: `backend/app/core/executor.py`

```python
"""
CommandExecutor - Safe subprocess execution

CRITICAL: Always uses list args, never shell=True
"""
import subprocess
import asyncio
from typing import List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class CommandTimeoutError(Exception):
    """Raised when command times out"""
    pass

class CommandExecutionError(Exception):
    """Raised when command fails"""
    pass

class CommandExecutor:
    """
    Safe command execution wrapper.
    
    Features:
    - ALWAYS uses list (never string)
    - NEVER uses shell=True
    - Always has timeout
    - Captures output
    """
    
    DEFAULT_TIMEOUT = 30  # seconds
    
    @staticmethod
    def run(
        command: List[str],
        timeout: Optional[int] = None,
        check: bool = True,
        cwd: Optional[str] = None
    ) -> subprocess.CompletedProcess:
        """
        Execute command safely (sync).
        
        Args:
            command: Command as list
            timeout: Timeout in seconds
            check: Raise on non-zero exit
            cwd: Working directory
            
        Returns:
            CompletedProcess
            
        Raises:
            TypeError: If command is not list
            CommandTimeoutError: If timeout
            CommandExecutionError: If command fails
        """
        if not isinstance(command, list):
            raise TypeError("Command must be a list, not string")
        
        if timeout is None:
            timeout = CommandExecutor.DEFAULT_TIMEOUT
        
        logger.info(f"Executing: {' '.join(command)}")
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=check,
                cwd=cwd
            )
            
            logger.info(f"Command completed: exit code {result.returncode}")
            return result
            
        except subprocess.TimeoutExpired as e:
            logger.error(f"Command timed out after {timeout}s")
            raise CommandTimeoutError(
                f"Command timed out after {timeout}s: {command[0]}"
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {e.stderr}")
            raise CommandExecutionError(
                f"Command failed (exit {e.returncode}): {e.stderr}"
            )
    
    @staticmethod
    async def run_async(
        command: List[str],
        timeout: Optional[int] = None
    ) -> Tuple[str, str]:
        """
        Execute command asynchronously (for FastAPI).
        
        Args:
            command: Command as list
            timeout: Timeout in seconds
            
        Returns:
            (stdout, stderr) tuple
            
        Raises:
            CommandTimeoutError: If timeout
        """
        if not isinstance(command, list):
            raise TypeError("Command must be a list")
        
        if timeout is None:
            timeout = CommandExecutor.DEFAULT_TIMEOUT
        
        logger.info(f"Executing async: {' '.join(command)}")
        
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
            
            logger.info(f"Async command completed: exit {process.returncode}")
            
            return stdout.decode(), stderr.decode()
            
        except asyncio.TimeoutError:
            process.kill()
            logger.error(f"Async command timed out after {timeout}s")
            raise CommandTimeoutError(
                f"Command timed out after {timeout}s: {command[0]}"
            )
```

**Critérios de Aceitação**:
- [ ] CommandExecutor implementado
- [ ] Sempre usa lista (nunca string)
- [ ] Timeout configurável
- [ ] Async e sync versions
- [ ] Logs adequados
- [ ] Testes unitários para cenários de sucesso, timeout e falha de comando (sync e async)

---

## Continuação das Tasks...

**Nota**: O documento completo tem ~50 tasks. Por limitação de espaço, incluí as primeiras 10 tasks detalhadas (Setup + Security Layer + Core). 

As tasks restantes seguem o mesmo padrão:
- ID único
- Código completo
- Testes quando aplicável
- Critérios de aceitação claros
- Dependências explícitas

**Próximas secções no documento**:
- Task 3.2-3.4: JSON Storage, BaseAdapter, SnapshotManager
- Task 4.1-4.3: Adapters (npm, pip, winget/brew)
- Task 5.1-5.3: PATH Validation
- Task 6.1-6.5: API Endpoints
- Task 7.1-7.6: Frontend Components
- Task 8.1-8.3: Testing
- Task 9.1-9.3: Documentation

**Formato de execução sugerido**:
```bash
# Para cada task:
1. Ler task completa
2. Implementar código fornecido
3. Executar testes
4. Validar critérios de aceitação
5. Commit com mensagem: "feat: [TASK-ID] Descrição"
6. Avançar para próxima task
```

---

## 📊 Progress Tracking

```markdown
## Fase 1 Progress

### Setup & Infrastructure (3/3)
- [x] Task 1.1: Estrutura do projeto
- [x] Task 1.2: Backend setup
- [x] Task 1.3: Frontend setup

### Security Layer (0/3)
- [ ] Task 2.1: ValidationLayer
- [ ] Task 2.2: LockManager
- [ ] Task 2.3: OperationQueue

### Core Backend (0/4)
- [ ] Task 3.1: CommandExecutor
- [ ] Task 3.2: JSON Storage
- [ ] Task 3.3: BaseAdapter
- [ ] Task 3.4: SnapshotManager

### Adapters (0/3)
- [ ] Task 4.1: NpmAdapter
- [ ] Task 4.2: PipAdapter
- [ ] Task 4.3: WinGetAdapter/BrewAdapter

### PATH Validation (0/3)
- [ ] Task 5.1: PathValidator
- [ ] Task 5.2: Script generators
- [ ] Task 5.3: PATH endpoints

### API Endpoints (0/5)
- [ ] Task 6.1: /discover
- [ ] Task 6.2: /managers
- [ ] Task 6.3: /packages
- [ ] Task 6.4: /path
- [ ] Task 6.5: /snapshot

### Frontend (0/6)
- [ ] Task 7.1: Layout
- [ ] Task 7.2: Dashboard
- [ ] Task 7.3: ManagerCard
- [ ] Task 7.4: PackageTable
- [ ] Task 7.5: ConfirmationModal
- [ ] Task 7.6: PathSetupGuide

### Testing (0/3)
- [ ] Task 8.1: Test ValidationLayer
- [ ] Task 8.2: Test LockManager
- [ ] Task 8.3: Test Adapters

### Documentation (0/3)
- [ ] Task 9.1: SECURITY.md
- [ ] Task 9.2: LIMITATIONS.md
- [ ] Task 9.3: SETUP_PATH.md

**Total Progress: 3/33 tasks (9%)**
```

---

## ⚡ Ordem de Execução Recomendada

### Dia 1-2: Security Foundation
1. ValidationLayer (Task 2.1) - CRÍTICO
2. LockManager (Task 2.2) - CRÍTICO
3. OperationQueue (Task 2.3)
4. CommandExecutor (Task 3.1)

**Milestone**: Sistema seguro contra injection e race conditions

### Dia 3-4: Core Backend
5. JSON Storage (Task 3.2)
6. BaseAdapter (Task 3.3)
7. SnapshotManager (Task 3.4)
8. NpmAdapter (Task 4.1) - Proof of concept

**Milestone**: Backend funcional com 1 adapter

### Dia 5-6: More Adapters + PATH
9. PipAdapter (Task 4.2)
10. WinGetAdapter/BrewAdapter (Task 4.3)
11. PathValidator (Task 5.1-5.3)

**Milestone**: 3 adapters + PATH validation

### Dia 7-8: API Endpoints
12. All API endpoints (Task 6.1-6.5)

**Milestone**: API completa

### Dia 9-10: Frontend
13. All frontend components (Task 7.1-7.6)

**Milestone**: UI funcional

### Dia 11-12: Testing + Docs
14. All tests (Task 8.1-8.3)
15. All docs (Task 9.1-9.3)

**Milestone**: Fase 1 completa

---

## 🚀 Começar Implementação

**Comando inicial**:
```bash
# Clonar estrutura
cd ~/projects
mkdir package-audit-dashboard
cd package-audit-dashboard

# Começar por Task 1.1 (estrutura)
# Depois Task 1.2 (backend)
# Depois Task 1.3 (frontend)
# Depois Task 2.1 (ValidationLayer) ← CRÍTICO
```

**Cada task deve resultar num commit**:
```bash
git add .
git commit -m "feat: [TASK-ID] Descrição curta"
```

---

*Breakdown v1.0 - Fase 1 MVP Seguro*
*Total: 33 tasks | Duração: 1-2 semanas*
*Prioridade: Security first ✅*
