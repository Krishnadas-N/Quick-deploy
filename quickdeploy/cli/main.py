"""Main CLI entry point for QuickDeploy."""

import sys
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..core.config import load_config, create_default_config
from ..core.runner import ProcessRunner
from ..core.cache_manager import CacheManager
from ..core.utils import find_entrypoint
from .. import __version__


app = typer.Typer(
    name="quickdeploy",
    help="QuickDeploy - Instant Python API and script runner",
    add_completion=False
)
console = Console()

# Global runner instance
_runner: Optional[ProcessRunner] = None


@app.command()
def version():
    """Show QuickDeploy version."""
    console.print(f"[bold cyan]QuickDeploy v{__version__}[/bold cyan]")


@app.command()
def run(
    path: str = typer.Argument(".", help="Path to project directory"),
    port: int = typer.Option(None, "--port", "-p", help="Override port number"),
    no_reload: bool = typer.Option(False, "--no-reload", help="Disable hot reload"),
    python_version: str = typer.Option(None, "--python", help="Python version to use")
):
    """Run a Python project instantly."""
    project_path = Path(path).resolve()
    
    if not project_path.exists():
        console.print(f"[red]Error: Path does not exist: {project_path}[/red]")
        raise typer.Exit(1)
    
    if not project_path.is_dir():
        console.print(f"[red]Error: Path is not a directory: {project_path}[/red]")
        raise typer.Exit(1)
    
    # Load or create config
    config = load_config(project_path)
    
    # Override config with CLI options
    if port:
        config.port = port
    if no_reload:
        config.auto_reload = False
    if python_version:
        config.python_version = python_version
    
    # Check for entrypoint
    entrypoint = find_entrypoint(project_path, config.entrypoint)
    if not entrypoint:
        console.print(f"[yellow]Warning: No entrypoint found. Creating default config...[/yellow]")
        create_default_config(project_path)
        console.print(f"[cyan]Please edit .quickdeploy.yaml and set the entrypoint.[/cyan]")
        raise typer.Exit(1)
    
    console.print(Panel.fit(
        f"[bold cyan]QuickDeploy[/bold cyan]\n"
        f"Project: [green]{project_path.name}[/green]\n"
        f"Entrypoint: [yellow]{entrypoint.name}[/yellow]\n"
        f"Port: [blue]{config.port}[/blue]\n"
        f"Hot Reload: [{'green' if config.auto_reload else 'red'}]{'Enabled' if config.auto_reload else 'Disabled'}[/]",
        title="Starting",
        border_style="cyan"
    ))
    
    # Create runner
    global _runner
    _runner = ProcessRunner(project_path, config)
    
    # Add console logging
    def log_callback(message: str):
        # Detect URLs and format them
        url_info = _runner._detect_and_format_url(message) if hasattr(_runner, '_detect_and_format_url') else None
        if url_info:
            console.print(url_info)
        else:
            console.print(message)
    
    _runner.add_log_callback(log_callback)
    
    # Run
    if not _runner.run():
        console.print("[red]Failed to start application[/red]")
        raise typer.Exit(1)
    
    # Wait for interrupt
    try:
        _runner.wait()
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopping...[/yellow]")
        _runner.stop()
        console.print("[green]Stopped[/green]")


@app.command()
def stop():
    """Stop a running QuickDeploy process."""
    global _runner
    if _runner and _runner.is_running:
        _runner.stop()
        console.print("[green]Process stopped[/green]")
    else:
        console.print("[yellow]No running process found[/yellow]")


@app.command()
def init(
    template: str = typer.Argument(None, help="Template name (fastapi, flask)"),
    path: str = typer.Argument(".", help="Path to initialize")
):
    """Initialize a new QuickDeploy project or create from template."""
    project_path = Path(path).resolve()
    
    if template:
        # Create from template
        from ..templates import create_template
        if create_template(template, project_path):
            console.print(f"[green]✓[/green] Created {template} template at {project_path}")
        else:
            console.print(f"[red]✗[/red] Unknown template: {template}")
            raise typer.Exit(1)
    else:
        # Just create config
        entrypoint = find_entrypoint(project_path)
        config = create_default_config(project_path, entrypoint.name if entrypoint else None)
        console.print(f"[green]✓[/green] Created .quickdeploy.yaml at {project_path}")
        console.print(f"[cyan]Edit .quickdeploy.yaml to customize settings[/cyan]")


@app.command()
def status():
    """Show status of QuickDeploy."""
    global _runner
    table = Table(title="QuickDeploy Status")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    if _runner and _runner.is_running:
        table.add_row("Status", "[green]Running[/green]")
        table.add_row("Project", str(_runner.project_path))
        table.add_row("Port", str(_runner.config.port))
    else:
        table.add_row("Status", "[yellow]Idle[/yellow]")
    
    cache_manager = CacheManager()
    table.add_row("Cache Size", cache_manager.format_cache_size())
    
    console.print(table)


@app.command()
def cache(
    clear: bool = typer.Option(False, "--clear", help="Clear the cache")
):
    """Manage QuickDeploy cache."""
    cache_manager = CacheManager()
    
    if clear:
        cache_manager.clear_cache()
        console.print("[green]✓[/green] Cache cleared")
    else:
        console.print(f"Cache size: [cyan]{cache_manager.format_cache_size()}[/cyan]")
        console.print(f"Cache location: [yellow]{cache_manager.get_cache_path()}[/yellow]")


def main():
    """Entry point for CLI."""
    app()


if __name__ == "__main__":
    main()

