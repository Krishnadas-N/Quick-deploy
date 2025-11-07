"""Setup script for QuickDeploy."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read version
version_file = Path(__file__).parent / "quickdeploy" / "__init__.py"
version = "0.1.0"
if version_file.exists():
    for line in version_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break

setup(
    name="quickdeploy",
    version=version,
    description="Instant Python API and script runner with auto environment management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="QuickDeploy Team",
    author_email="",
    url="https://github.com/yourusername/quickdeploy",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "pyyaml>=6.0",
        "watchdog>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "ruff>=0.1.0",
            "black>=23.0.0",
        ],
        "gui": [],  # Tkinter is built-in
    },
    entry_points={
        "console_scripts": [
            "quickdeploy=quickdeploy.cli.main:main",
            "quickdeploy-gui=quickdeploy.gui.app:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="python deployment development api fastapi flask cli gui",
)

