# Package Audit Dashboard

MVP para auditar e gerir pacotes de diferentes gestores (npm, pip, winget/brew) com foco em segurança operacional.

## Desenvolvimento Rápido

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Estrutura Atual
- `frontend/` – aplicação React 18 com Vite.
- `backend/` – API FastAPI (a preencher conforme Fase 1).
- `cli/` – ponto de entrada para comandos Typer.
- `docs/` – documentação e relatórios.
- `scripts/setup/` – utilitários para bootstrap do projeto.

## Próximos Passos
- Concluir tarefas da Fase 1 descritas em `FASE1_BREAKDOWN.md`.
- Manter `LOG.md` atualizado com decisões e progresso relevante.
