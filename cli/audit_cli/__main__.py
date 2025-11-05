"""CLI principal do Package Audit Dashboard."""
import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).resolve().parents[2] / "backend"
sys.path.insert(0, str(backend_path))

from cli.audit_cli.app import app

if __name__ == "__main__":
    app()
