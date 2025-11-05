#!/usr/bin/env python3
"""
Bootstrap utilitário para garantir que a estrutura base do Package Audit Dashboard
existe sem sobrescrever ficheiros existentes.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List


ROOT_DIR = Path(__file__).resolve().parents[2]

DIRECTORIES = [
    "frontend/src/components",
    "frontend/src/hooks",
    "frontend/src/store",
    "frontend/src/types",
    "backend/app/routers",
    "backend/app/adapters",
    "backend/app/analysis",
    "backend/app/core",
    "backend/app/models",
    "backend/app/storage",
    "backend/tests",
    "cli/audit_cli",
    "docs",
    "scripts/setup",
]

INIT_FILES = [
    "backend/app/__init__.py",
    "backend/app/routers/__init__.py",
    "backend/app/adapters/__init__.py",
    "backend/app/analysis/__init__.py",
    "backend/app/core/__init__.py",
    "backend/app/models/__init__.py",
    "backend/app/storage/__init__.py",
    "backend/tests/__init__.py",
    "cli/audit_cli/__init__.py",
]

GITIGNORE_APPEND_PATH = Path("scripts/setup/gitignore.append")
GITIGNORE_TEMPLATE = """# Python
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
"""


def ensure_directory(path: Path, dry_run: bool) -> bool:
    """Cria diretório se não existir. Retorna True se criado."""
    if path.exists():
        return False
    if dry_run:
        print(f"[dry-run] mkdir -p {path.relative_to(ROOT_DIR)}")
        return True
    path.mkdir(parents=True, exist_ok=True)
    print(f"[ok] created directory {path.relative_to(ROOT_DIR)}")
    return True


def ensure_file(path: Path, dry_run: bool) -> bool:
    """Cria ficheiro vazio se não existir. Retorna True se criado."""
    if path.exists():
        return False
    if dry_run:
        print(f"[dry-run] touch {path.relative_to(ROOT_DIR)}")
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    print(f"[ok] created file {path.relative_to(ROOT_DIR)}")
    return True


def ensure_gitignore_append(path: Path, dry_run: bool) -> bool:
    """Garante que o ficheiro gitignore.append existe com conteúdo base."""
    if path.exists():
        return False
    if dry_run:
        print(f"[dry-run] write template to {path}")
        return True
    path.write_text(GITIGNORE_TEMPLATE, encoding="utf-8")
    print(f"[ok] created template {path}")
    return True


def bootstrap(dry_run: bool) -> Dict[str, List[str]]:
    """Executa operações de bootstrap e devolve registo do que foi criado."""
    results: Dict[str, List[str]] = {
        "created_dirs": [],
        "existing_dirs": [],
        "created_files": [],
        "existing_files": [],
    }

    for rel_dir in DIRECTORIES:
        path = ROOT_DIR / rel_dir
        created = ensure_directory(path, dry_run)
        bucket = "created_dirs" if created else "existing_dirs"
        results[bucket].append(rel_dir)

    for rel_file in INIT_FILES:
        path = ROOT_DIR / rel_file
        created = ensure_file(path, dry_run)
        bucket = "created_files" if created else "existing_files"
        results[bucket].append(rel_file)

    ensure_gitignore_append(ROOT_DIR / GITIGNORE_APPEND_PATH, dry_run)

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Garante que a estrutura base do projeto existe."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra as ações sem alterar o sistema de ficheiros.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = bootstrap(dry_run=args.dry_run)

    print("\nResumo:")
    print(f"  Diretórios criados: {len(results['created_dirs'])}")
    print(f"  Diretórios já existentes: {len(results['existing_dirs'])}")
    print(f"  Ficheiros criados: {len(results['created_files'])}")
    print(f"  Ficheiros já existentes: {len(results['existing_files'])}")

    if results["created_dirs"] or results["created_files"]:
        print("\nVerifica diffs antes de fazer commit.")


if __name__ == "__main__":
    main()
