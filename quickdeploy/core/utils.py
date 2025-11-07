"""Utility functions for QuickDeploy."""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, Tuple


def find_python_executable(version: Optional[str] = None) -> str:
    """Find Python executable, optionally for a specific version."""
    if version:
        # Try specific version
        for cmd in [f"python{version}", f"python{version.replace('.', '')}"]:
            try:
                result = subprocess.run(
                    [cmd, "--version"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                if version in result.stdout or version in result.stderr:
                    return cmd
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
    
    # Fallback to current Python
    return sys.executable


def detect_framework(entrypoint: Path) -> Optional[str]:
    """Detect if entrypoint is FastAPI, Flask, or other."""
    try:
        content = entrypoint.read_text(encoding="utf-8")
        content_lower = content.lower()
        
        if "from fastapi import" in content or "import fastapi" in content:
            return "fastapi"
        elif "from flask import" in content or "import flask" in content:
            return "flask"
        elif "uvicorn" in content_lower or "app = FastAPI" in content:
            return "fastapi"
        elif "app = Flask" in content or "Flask(__name__)" in content:
            return "flask"
    except Exception:
        pass
    
    return None


def find_entrypoint(project_path: Path, config_entrypoint: Optional[str] = None) -> Optional[Path]:
    """Find the entrypoint file for the project."""
    if config_entrypoint:
        candidate = project_path / config_entrypoint
        if candidate.exists():
            return candidate
    
    # Common entrypoint names
    common_names = ["app.py", "main.py", "server.py", "run.py", "index.py"]
    for name in common_names:
        candidate = project_path / name
        if candidate.exists():
            return candidate
    
    # Look for FastAPI/Flask patterns in Python files
    for py_file in project_path.glob("*.py"):
        if detect_framework(py_file):
            return py_file
    
    return None


def get_venv_python(venv_path: Path) -> Path:
    """Get the Python executable path inside a virtual environment."""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists and return it."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_cache_dir() -> Path:
    """Get the global cache directory for QuickDeploy."""
    if sys.platform == "win32":
        cache_base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif sys.platform == "darwin":
        cache_base = Path.home() / "Library" / "Caches"
    else:
        cache_base = Path.home() / ".cache"
    
    return ensure_dir(cache_base / "quickdeploy")


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string."""
    if seconds < 1:
        return f"{int(seconds * 1000)}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}m {secs}s"

