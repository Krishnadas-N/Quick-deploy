"""Dependency caching system for QuickDeploy."""

import shutil
from pathlib import Path
from typing import Optional
from .utils import get_cache_dir


class CacheManager:
    """Manages pip wheel cache for faster dependency installation."""
    
    def __init__(self):
        self.cache_dir = get_cache_dir() / "wheels"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get_cache_path(self) -> Path:
        """Get the path to the wheel cache directory."""
        return self.cache_dir
    
    def clear_cache(self) -> None:
        """Clear the entire cache."""
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get_cache_size(self) -> int:
        """Get total size of cache in bytes."""
        total = 0
        if self.cache_dir.exists():
            for file in self.cache_dir.rglob("*"):
                if file.is_file():
                    total += file.stat().st_size
        return total
    
    def format_cache_size(self) -> str:
        """Format cache size as human-readable string."""
        size = self.get_cache_size()
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

