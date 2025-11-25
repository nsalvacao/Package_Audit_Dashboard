#!/usr/bin/env python3
"""Quick setup script for Package Audit Dashboard (cross-platform)."""
import os
import platform
import subprocess
import sys
from pathlib import Path

# Garantir UTF-8 em consoles Windows (evita UnicodeEncodeError com emojis)
os.environ.setdefault("PYTHONUTF8", "1")


class Colors:
    """ANSI color codes."""

    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color


def print_header(message: str) -> None:
    """Print a header message."""
    print(f"\n{Colors.BLUE}{message}{Colors.NC}")
    print("=" * len(message))


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"{Colors.GREEN}✓ {message}{Colors.NC}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.NC}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"{Colors.RED}❌ {message}{Colors.NC}")


def check_python_version() -> bool:
    """Check if Python version is 3.10+."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} found")
        return True
    print_error(f"Python {version.major}.{version.minor} found. Python 3.10+ required.")
    return False


def setup_backend() -> bool:
    """Setup backend environment and dependencies."""
    print_header("🔧 Setting up Backend")

    backend_dir = Path("backend")
    if not backend_dir.exists():
        print_error("Backend directory not found")
        return False

    os.chdir(backend_dir)

    # Create virtual environment
    venv_dir = Path(".venv")
    if not venv_dir.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print_success("Virtual environment created")
    else:
        print_warning("Virtual environment already exists")

    # Determine activation script
    if platform.system() == "Windows":
        python_exec = venv_dir / "Scripts" / "python.exe"
        pip_exec = venv_dir / "Scripts" / "pip.exe"
    else:
        python_exec = venv_dir / "bin" / "python"
        pip_exec = venv_dir / "bin" / "pip"

    # Upgrade pip (use python -m pip to avoid self-upgrade lock on Windows)
    print("Upgrading pip...")
    subprocess.run([str(python_exec), "-m", "pip", "install", "--upgrade", "pip"], check=True)

    # Install requirements
    print("Installing dependencies...")
    subprocess.run([str(python_exec), "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    print_success("Dependencies installed")

    # Run tests
    print("\n🧪 Running tests...")
    try:
        result = subprocess.run(
            [str(python_exec), "-m", "pytest", "tests/", "-v", "--tb=short"],
            capture_output=False,
        )
        if result.returncode == 0:
            print_success("All tests passed")
        else:
            print_warning(
                "Some tests failed (expected if system package managers not installed)"
            )
    except Exception as e:
        print_warning(f"Could not run tests: {e}")

    os.chdir("..")
    return True


def check_node() -> bool:
    """Check if Node.js is installed."""
    try:
        result = subprocess.run(
            ["node", "--version"], capture_output=True, text=True, check=True
        )
        version = result.stdout.strip()
        print_success(f"Node.js {version} found")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_warning("Node.js not found. Frontend setup skipped.")
        print("  Install Node.js 18+ from: https://nodejs.org/")
        return False


def setup_frontend() -> bool:
    """Setup frontend if Node.js is available."""
    print_header("🔧 Setting up Frontend")

    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print_warning("Frontend directory not found (will be created later)")
        return False

    if not check_node():
        return False

    os.chdir(frontend_dir)

    node_modules = Path("node_modules")
    if not node_modules.exists():
        print("Installing npm dependencies...")
        subprocess.run(["npm", "install"], check=True)
        print_success("Frontend dependencies installed")
    else:
        print_warning("Frontend dependencies already installed")

    os.chdir("..")
    return True


def create_directories() -> None:
    """Create necessary application directories."""
    print_header("📁 Creating necessary directories")

    home = Path.home()
    base_dir = home / ".package-audit"

    dirs = [
        base_dir / "storage",
        base_dir / "snapshots",
        base_dir / "manifests",
        base_dir / "logs",
    ]

    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)

    print_success(f"Directories created in {base_dir}")


def print_next_steps() -> None:
    """Print next steps for the user."""
    print("\n" + "=" * 50)
    print_success("Setup completed successfully!")
    print("\n📝 Next steps:\n")

    if platform.system() == "Windows":
        activate_cmd = ".\\.venv\\Scripts\\activate"
    else:
        activate_cmd = "source .venv/bin/activate"

    print("1. Start the backend server:")
    print("   cd backend")
    print(f"   {activate_cmd}")
    print("   uvicorn app.main:app --reload")
    print("\n2. Access the API documentation:")
    print("   http://localhost:8000/docs")
    print("\n3. If frontend is available, start it with:")
    print("   cd frontend")
    print("   npm run dev")
    print()


def ensure_node_in_path() -> None:
    """Guarantee Node.js binaries are reachable on Windows PATH."""
    if platform.system() != "Windows":
        return

    candidate_paths = [
        Path(r"C:\Program Files\nodejs"),
        Path.home() / "AppData" / "Local" / "Programs" / "nodejs",
    ]

    current_path = os.environ.get("PATH", "")
    to_prepend: list[str] = []
    for path in candidate_paths:
        if path.exists() and str(path) not in current_path:
            to_prepend.append(str(path))

    if to_prepend:
        os.environ["PATH"] = os.pathsep.join(to_prepend + [current_path])


def main() -> int:
    """Main setup function."""
    print_header("🚀 Package Audit Dashboard - Quick Setup")

    ensure_node_in_path()

    # Check Python version
    if not check_python_version():
        return 1

    # Setup backend
    if not setup_backend():
        return 1

    # Setup frontend (optional)
    setup_frontend()

    # Create directories
    create_directories()

    # Print next steps
    print_next_steps()

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Setup failed: {e}")
        sys.exit(1)
