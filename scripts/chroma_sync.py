"""Sincroniza o LOG.md com uma instância local do ChromaDB."""
from __future__ import annotations

import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
LOG_PATH = BASE_DIR / "LOG.md"
CHROMA_DIR = BASE_DIR / "data" / "chromadb"
COLLECTION_NAME = "project_logs"


def load_log_content() -> str:
    if not LOG_PATH.exists():
        raise FileNotFoundError(f"LOG.md não encontrado em {LOG_PATH}")
    return LOG_PATH.read_text(encoding="utf-8")


def compute_id(content: str) -> str:
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return f"log-{digest[:16]}"


def sync_log() -> None:
    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError(
            "chromadb não está instalado. Usa 'pip install chromadb' ou instala os "
            "extras necessários antes de correr o sincronizador."
        ) from exc
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "Falha ao importar chromadb (provavelmente faltam dependências como "
            "'tokenizers' ou 'onnxruntime'). Instala os extras necessários."
        ) from exc

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    content = load_log_content()
    doc_id = compute_id(content)

    try:
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        collection = client.get_or_create_collection(name=COLLECTION_NAME)
    except Exception as exc:  # pragma: no cover - depende de deps opcionais
        raise RuntimeError(
            "Falha ao inicializar o ChromaDB. Verifica se dependências como "
            "'tokenizers', 'onnxruntime' e 'duckdb' estão instaladas."
        ) from exc

    metadata = {
        "source": "LOG.md",
        "synced_at": datetime.now(timezone.utc).isoformat(),
        "characters": len(content),
        "lines": content.count("\n") + 1,
    }

    collection.upsert(ids=[doc_id], documents=[content], metadatas=[metadata])

    print(
        "Sincronização concluída:",
        f"coleção={COLLECTION_NAME}",
        f"doc_id={doc_id}",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Sincroniza LOG.md com ChromaDB")
    parser.add_argument(
        "--check", action="store_true", help="Apenas verifica se o LOG.md está acessível"
    )
    args = parser.parse_args()

    if args.check:
        content = load_log_content()
        print(f"LOG.md disponível ({len(content)} caracteres)")
        return

    sync_log()


if __name__ == "__main__":
    main()
