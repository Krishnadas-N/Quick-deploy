"""Configuration management for QuickDeploy."""

import yaml
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class QuickDeployConfig:
    """Configuration for a QuickDeploy project."""
    entrypoint: str = "app.py"
    port: int = 8000
    python_version: Optional[str] = None
    auto_reload: bool = True
    watch_patterns: list[str] = field(default_factory=lambda: ["*.py", "*.yaml", "*.yml", "*.json"])
    ignore_patterns: list[str] = field(default_factory=lambda: ["*.pyc", "__pycache__", ".git", ".qd_env"])
    env_vars: dict[str, str] = field(default_factory=dict)
    install_args: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QuickDeployConfig":
        """Create config from dictionary."""
        return cls(
            entrypoint=data.get("entrypoint", "app.py"),
            port=data.get("port", 8000),
            python_version=data.get("python_version"),
            auto_reload=data.get("auto_reload", True),
            watch_patterns=data.get("watch_patterns", ["*.py", "*.yaml", "*.yml", "*.json"]),
            ignore_patterns=data.get("ignore_patterns", ["*.pyc", "__pycache__", ".git", ".qd_env"]),
            env_vars=data.get("env_vars", {}),
            install_args=data.get("install_args", [])
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "entrypoint": self.entrypoint,
            "port": self.port,
            "python_version": self.python_version,
            "auto_reload": self.auto_reload,
            "watch_patterns": self.watch_patterns,
            "ignore_patterns": self.ignore_patterns,
            "env_vars": self.env_vars,
            "install_args": self.install_args
        }

    def save(self, path: Path) -> None:
        """Save config to YAML file."""
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, sort_keys=False)


def load_config(project_path: Path) -> QuickDeployConfig:
    """Load configuration from .quickdeploy.yaml or return defaults."""
    config_path = project_path / ".quickdeploy.yaml"

    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            return QuickDeployConfig.from_dict(data)
        except Exception as e:
            print(f"Warning: Failed to load config from {config_path}: {e}")
            print("Using default configuration.")

    return QuickDeployConfig()


def create_default_config(project_path: Path, entrypoint: Optional[str] = None) -> QuickDeployConfig:
    """Create and save a default configuration file."""
    config = QuickDeployConfig()
    if entrypoint:
        config.entrypoint = entrypoint

    config_path = project_path / ".quickdeploy.yaml"
    config.save(config_path)
    return config

