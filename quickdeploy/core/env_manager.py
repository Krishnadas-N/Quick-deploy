"""Virtual environment management for QuickDeploy."""

import subprocess
import sys
import venv
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .utils import find_python_executable, get_venv_python, ensure_dir
from .cache_manager import CacheManager


console = Console()


class EnvManager:
    """Manages virtual environments for QuickDeploy projects."""
    
    def __init__(self, project_path: Path):
        self.project_path = Path(project_path).resolve()
        self.venv_path = self.project_path / ".qd_env"
        self.cache_manager = CacheManager()
    
    def exists(self) -> bool:
        """Check if virtual environment exists."""
        python_exe = get_venv_python(self.venv_path)
        return python_exe.exists()
    
    def create(self, python_version: Optional[str] = None) -> bool:
        """Create a new virtual environment."""
        if self.exists():
            console.print(f"[green]✓[/green] Virtual environment already exists at {self.venv_path}")
            return True
        
        console.print(f"[cyan]Creating virtual environment at {self.venv_path}...[/cyan]")
        
        try:
            # Use venv module
            venv.create(self.venv_path, with_pip=True)
            console.print(f"[green]✓[/green] Virtual environment created successfully")
            return True
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to create virtual environment: {e}")
            return False
    
    def get_python(self) -> Path:
        """Get the Python executable in the virtual environment."""
        return get_venv_python(self.venv_path)
    
    def install_dependencies(self, requirements_file: Optional[Path] = None, 
                            pyproject_file: Optional[Path] = None,
                            use_cache: bool = True) -> bool:
        """Install dependencies from requirements.txt or pyproject.toml."""
        python_exe = self.get_python()
        
        # Find requirements file
        if requirements_file is None:
            requirements_file = self.project_path / "requirements.txt"
        
        if pyproject_file is None:
            pyproject_file = self.project_path / "pyproject.toml"
        
        install_cmd = [str(python_exe), "-m", "pip", "install", "--upgrade", "pip"]
        
        # Use cache if available
        if use_cache:
            cache_dir = self.cache_manager.get_cache_path()
            install_cmd.extend(["--cache-dir", str(cache_dir)])
        
        # Install pip first
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Upgrading pip...", total=None)
                subprocess.run(
                    install_cmd,
                    cwd=self.project_path,
                    check=True,
                    capture_output=True
                )
                progress.update(task, completed=True)
        except subprocess.CalledProcessError as e:
            console.print(f"[yellow]Warning: Failed to upgrade pip: {e}[/yellow]")
        
        # Install dependencies
        if requirements_file.exists():
            console.print(f"[cyan]Installing dependencies from {requirements_file.name}...[/cyan]")
            install_cmd = [str(python_exe), "-m", "pip", "install", "-r", str(requirements_file)]
            
            if use_cache:
                cache_dir = self.cache_manager.get_cache_path()
                install_cmd.extend(["--cache-dir", str(cache_dir)])
            
            try:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("Installing dependencies...", total=None)
                    result = subprocess.run(
                        install_cmd,
                        cwd=self.project_path,
                        check=True,
                        capture_output=False
                    )
                    progress.update(task, completed=True)
                
                console.print(f"[green]✓[/green] Dependencies installed successfully")
                return True
            except subprocess.CalledProcessError as e:
                console.print(f"[red]✗[/red] Failed to install dependencies: {e}[/red]")
                return False
        
        elif pyproject_file.exists():
            console.print(f"[cyan]Installing dependencies from {pyproject_file.name}...[/cyan]")
            install_cmd = [str(python_exe), "-m", "pip", "install", "-e", "."]
            
            if use_cache:
                cache_dir = self.cache_manager.get_cache_path()
                install_cmd.extend(["--cache-dir", str(cache_dir)])
            
            try:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("Installing dependencies...", total=None)
                    result = subprocess.run(
                        install_cmd,
                        cwd=self.project_path,
                        check=True,
                        capture_output=False
                    )
                    progress.update(task, completed=True)
                
                console.print(f"[green]✓[/green] Dependencies installed successfully")
                return True
            except subprocess.CalledProcessError as e:
                console.print(f"[red]✗[/red] Failed to install dependencies: {e}[/red]")
                return False
        else:
            console.print("[yellow]No requirements.txt or pyproject.toml found. Skipping dependency installation.[/yellow]")
            return True
    
    def install_package(self, package: str) -> bool:
        """Install a single package into the virtual environment."""
        python_exe = self.get_python()
        install_cmd = [str(python_exe), "-m", "pip", "install", package]
        
        cache_dir = self.cache_manager.get_cache_path()
        install_cmd.extend(["--cache-dir", str(cache_dir)])
        
        try:
            subprocess.run(install_cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def ensure_setup(self, python_version: Optional[str] = None, 
                    install_deps: bool = True) -> bool:
        """Ensure virtual environment is set up and dependencies are installed."""
        if not self.exists():
            if not self.create(python_version):
                return False
        
        if install_deps:
            return self.install_dependencies()
        
        return True

