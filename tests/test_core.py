"""Tests for core QuickDeploy modules."""

import pytest
from pathlib import Path
import tempfile
import shutil

from quickdeploy.core.config import QuickDeployConfig, load_config, create_default_config
from quickdeploy.core.cache_manager import CacheManager
from quickdeploy.core.utils import detect_framework, find_entrypoint


def test_config_defaults():
    """Test default configuration values."""
    config = QuickDeployConfig()
    assert config.entrypoint == "app.py"
    assert config.port == 8000
    assert config.auto_reload is True
    assert config.python_version is None


def test_config_from_dict():
    """Test creating config from dictionary."""
    data = {
        "entrypoint": "main.py",
        "port": 9000,
        "auto_reload": False
    }
    config = QuickDeployConfig.from_dict(data)
    assert config.entrypoint == "main.py"
    assert config.port == 9000
    assert config.auto_reload is False


def test_config_save_load(tmp_path):
    """Test saving and loading configuration."""
    config = QuickDeployConfig(entrypoint="server.py", port=8080)
    config_path = tmp_path / ".quickdeploy.yaml"
    config.save(config_path)
    
    assert config_path.exists()
    
    loaded = load_config(tmp_path)
    assert loaded.entrypoint == "server.py"
    assert loaded.port == 8080


def test_detect_framework_fastapi(tmp_path):
    """Test FastAPI detection."""
    app_file = tmp_path / "app.py"
    app_file.write_text("from fastapi import FastAPI\napp = FastAPI()")
    
    assert detect_framework(app_file) == "fastapi"


def test_detect_framework_flask(tmp_path):
    """Test Flask detection."""
    app_file = tmp_path / "app.py"
    app_file.write_text("from flask import Flask\napp = Flask(__name__)")
    
    assert detect_framework(app_file) == "flask"


def test_find_entrypoint(tmp_path):
    """Test finding entrypoint files."""
    # Create app.py
    app_file = tmp_path / "app.py"
    app_file.write_text("print('hello')")
    
    entrypoint = find_entrypoint(tmp_path)
    assert entrypoint == app_file


def test_cache_manager():
    """Test cache manager functionality."""
    cache_manager = CacheManager()
    assert cache_manager.get_cache_path().exists()
    
    size = cache_manager.get_cache_size()
    assert isinstance(size, int)
    assert size >= 0
    
    formatted = cache_manager.format_cache_size()
    assert isinstance(formatted, str)
    assert "B" in formatted or "KB" in formatted or "MB" in formatted


def test_create_default_config(tmp_path):
    """Test creating default configuration."""
    config = create_default_config(tmp_path, "main.py")
    assert config.entrypoint == "main.py"
    
    config_path = tmp_path / ".quickdeploy.yaml"
    assert config_path.exists()

