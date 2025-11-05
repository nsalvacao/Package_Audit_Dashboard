"""CLI application using Typer."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

# Add backend to path
backend_path = Path(__file__).resolve().parents[2] / "backend"
sys.path.insert(0, str(backend_path))

from app.adapters import get_registered_adapters
from app.adapters.base import BaseAdapter

app = typer.Typer(
    name="audit-cli",
    help="Package Audit Dashboard CLI - Manage package managers from the terminal",
    add_completion=False,
)
console = Console()


@app.command()
def discover() -> None:
    """
    Discover installed package managers on the system.
    """
    console.print("\n🔍 [bold cyan]Discovering package managers...[/bold cyan]\n")

    adapters = get_registered_adapters()
    detected: list[BaseAdapter] = []

    for adapter_cls in adapters:
        if adapter_cls.detect():
            detected.append(adapter_cls)

    if not detected:
        console.print(
            "[yellow]⚠ No package managers detected.[/yellow]",
            "\nSupported: npm, pip, winget, brew\n",
        )
        raise typer.Exit(code=1)

    # Create table
    table = Table(title="Detected Package Managers", show_header=True)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Version", style="green")
    table.add_column("Status", style="bold green")

    for adapter in detected:
        version = adapter.get_version() or "unknown"
        table.add_row(
            adapter.manager_id,
            adapter.display_name,
            version,
            "✓ Active",
        )

    console.print(table)
    console.print(
        f"\n[green]✓[/green] Found [bold]{len(detected)}[/bold] package manager(s)\n"
    )


@app.command()
def list_packages(
    manager: str = typer.Argument(..., help="Package manager ID (e.g., npm, pip)"),
) -> None:
    """
    List all packages installed by a specific package manager.
    """
    console.print(
        f"\n📦 [bold cyan]Listing packages for {manager}...[/bold cyan]\n"
    )

    # Find adapter
    adapters = get_registered_adapters()
    adapter_cls = None

    for cls in adapters:
        if cls.manager_id == manager:
            adapter_cls = cls
            break

    if not adapter_cls:
        console.print(f"[red]✗[/red] Package manager '{manager}' not found.\n")
        console.print("Available managers:")
        for cls in adapters:
            console.print(f"  - {cls.manager_id}")
        raise typer.Exit(code=1)

    if not adapter_cls.detect():
        console.print(
            f"[yellow]⚠[/yellow] Package manager '{manager}' is not installed.\n"
        )
        raise typer.Exit(code=1)

    # List packages
    try:
        adapter = adapter_cls()
        packages = adapter.list_packages()

        if not packages:
            console.print("[yellow]No packages found.[/yellow]\n")
            return

        # Create table
        table = Table(title=f"{adapter_cls.display_name} Packages", show_header=True)
        table.add_column("Package", style="cyan")
        table.add_column("Version", style="green")

        for pkg in packages:
            table.add_row(pkg.get("name", "unknown"), pkg.get("version", "unknown"))

        console.print(table)
        console.print(f"\n[green]✓[/green] Total: [bold]{len(packages)}[/bold] packages\n")

    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}\n")
        raise typer.Exit(code=1)


@app.command()
def uninstall(
    manager: str = typer.Argument(..., help="Package manager ID (e.g., npm, pip)"),
    package: str = typer.Argument(..., help="Package name to uninstall"),
    force: bool = typer.Option(False, "--force", "-f", help="Force uninstall"),
) -> None:
    """
    Uninstall a package using the specified package manager.

    WARNING: This is a destructive operation. A snapshot will be created automatically.
    """
    console.print(
        f"\n🗑️  [bold yellow]Uninstalling {package} from {manager}...[/bold yellow]\n"
    )

    # Find adapter
    adapters = get_registered_adapters()
    adapter_cls = None

    for cls in adapters:
        if cls.manager_id == manager:
            adapter_cls = cls
            break

    if not adapter_cls or not adapter_cls.detect():
        console.print(f"[red]✗[/red] Package manager '{manager}' not available.\n")
        raise typer.Exit(code=1)

    # Confirm
    if not typer.confirm(
        f"Are you sure you want to uninstall '{package}'?", default=False
    ):
        console.print("[yellow]Cancelled.[/yellow]\n")
        raise typer.Exit(code=0)

    # Uninstall
    try:
        adapter = adapter_cls()
        result = adapter.uninstall(package, force=force)

        console.print(f"[green]✓[/green] Package '{package}' uninstalled successfully!\n")
        console.print(f"Operation details: {result}\n")

    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}\n")
        raise typer.Exit(code=1)


@app.command()
def version() -> None:
    """
    Show CLI version information.
    """
    rprint("\n[bold cyan]Package Audit Dashboard CLI[/bold cyan]")
    rprint("[green]Version:[/green] 0.1.0 (MVP)")
    rprint("[green]Backend:[/green] FastAPI")
    rprint("[green]Phase:[/green] 1 (Core Functionality)\n")


@app.command()
def status() -> None:
    """
    Show system status and health check.
    """
    console.print("\n💻 [bold cyan]System Status[/bold cyan]\n")

    # Check backend directory
    backend_dir = Path(__file__).resolve().parents[2] / "backend"
    data_dir = Path.home() / ".package-audit"

    status_table = Table(show_header=True)
    status_table.add_column("Component", style="cyan")
    status_table.add_column("Status", style="green")
    status_table.add_column("Details", style="dim")

    # Backend
    status_table.add_row(
        "Backend",
        "✓ Found" if backend_dir.exists() else "✗ Missing",
        str(backend_dir),
    )

    # Data directory
    status_table.add_row(
        "Data Directory",
        "✓ Found" if data_dir.exists() else "✗ Missing",
        str(data_dir),
    )

    # Storage
    storage_dir = data_dir / "storage"
    status_table.add_row(
        "Storage",
        "✓ Ready" if storage_dir.exists() else "⚠ Not created",
        str(storage_dir),
    )

    # Snapshots
    snapshots_dir = data_dir / "snapshots"
    status_table.add_row(
        "Snapshots",
        "✓ Ready" if snapshots_dir.exists() else "⚠ Not created",
        str(snapshots_dir),
    )

    console.print(status_table)
    console.print()


if __name__ == "__main__":
    app()
