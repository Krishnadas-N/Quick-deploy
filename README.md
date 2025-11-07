# QuickDeploy 🚀

**Instant Python API and script runner** - Run any Python project with one command, no manual setup required.

QuickDeploy automatically:
- ✅ Creates and manages virtual environments
- ✅ Installs dependencies from `requirements.txt` or `pyproject.toml`
- ✅ Detects FastAPI/Flask apps automatically
- ✅ Provides hot reload for development
- ✅ Caches dependencies for faster restarts
- ✅ Offers both CLI and GUI interfaces

---

## 🎯 Features

- **Zero Configuration**: Works out of the box with sensible defaults
- **Auto Environment Management**: Creates `.qd_env` virtual environments automatically
- **Smart Detection**: Automatically detects FastAPI, Flask, or generic Python scripts
- **Hot Reload**: Watch for file changes and auto-restart your app
- **Dependency Caching**: Global wheel cache speeds up dependency installation
- **Dual Interface**: Use via CLI or friendly GUI
- **Template Scaffolding**: Quick start with `quickdeploy init fastapi` or `quickdeploy init flask`

---

## 📦 Installation

### From Source

```bash
git clone https://github.com/yourusername/quickdeploy.git
cd quickdeploy
pip install -e .
```

### From PyPI (when published)

```bash
pip install quickdeploy
```

---

## 🚀 Quick Start

### 1. Run an Existing Project

```bash
# Navigate to your project
cd my-python-project

# Run it!
quickdeploy run .
```

That's it! QuickDeploy will:
1. Create a virtual environment (`.qd_env`) if needed
2. Install dependencies from `requirements.txt` or `pyproject.toml`
3. Detect your entrypoint (FastAPI/Flask/generic)
4. Start your app with hot reload enabled

### 2. Create a New Project from Template

```bash
# Create a FastAPI project
quickdeploy init fastapi my-api
cd my-api
quickdeploy run .

# Create a Flask project
quickdeploy init flask my-app
cd my-app
quickdeploy run .
```

### 3. Use the GUI

```bash
quickdeploy-gui
```

Then:
- Click "Browse" to select your project
- Click "Run" to start
- View logs in real-time
- Click "Stop" when done

---

## 📖 Usage

### CLI Commands

```bash
# Run a project
quickdeploy run [path]              # Run current directory
quickdeploy run ./my-project        # Run specific project
quickdeploy run . --port 9000       # Override port
quickdeploy run . --no-reload       # Disable hot reload

# Initialize a project
quickdeploy init                    # Create .quickdeploy.yaml
quickdeploy init fastapi            # Create FastAPI template
quickdeploy init flask              # Create Flask template

# Manage cache
quickdeploy cache                   # Show cache info
quickdeploy cache --clear           # Clear cache

# Check status
quickdeploy status                  # Show running status
quickdeploy stop                    # Stop running process

# Version
quickdeploy version                 # Show version
```

### Configuration File

Create `.quickdeploy.yaml` in your project root:

```yaml
entrypoint: app.py              # Entry point file
port: 8000                      # Port number
python_version: "3.11"          # Optional Python version
auto_reload: true               # Enable hot reload
watch_patterns:                 # Files to watch
  - "*.py"
  - "*.yaml"
ignore_patterns:                # Files to ignore
  - "*.pyc"
  - "__pycache__"
env_vars:                       # Environment variables
  DEBUG: "true"
install_args: []                # Extra pip install args
```

---

## 🏗️ Project Structure

```
quickdeploy/
├── cli/              # CLI interface
├── core/             # Core functionality
│   ├── config.py     # Configuration management
│   ├── env_manager.py # Virtual environment management
│   ├── runner.py     # Process runner
│   ├── watcher.py    # File watching
│   └── cache_manager.py # Dependency caching
├── gui/              # GUI interface
├── templates/         # Project templates
└── tests/            # Tests
```

---

## 🧪 Development

### Setup Development Environment

```bash
git clone https://github.com/yourusername/quickdeploy.git
cd quickdeploy
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/ -v
```

### Lint Code

```bash
ruff check .
black quickdeploy/
```

---

## 📝 Examples

### FastAPI Example

```python
# app.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

```bash
quickdeploy run .
# → Application running at: http://127.0.0.1:8000
```

### Flask Example

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return {"Hello": "World"}
```

```bash
quickdeploy run .
# → Application running at: http://127.0.0.1:8000
```

### Generic Python Script

```python
# app.py
import time

print("Starting...")
for i in range(10):
    print(f"Count: {i}")
    time.sleep(1)
print("Done!")
```

```bash
quickdeploy run .
```

---

## 🛠️ Troubleshooting

### Virtual Environment Issues

If you encounter issues with virtual environments:

```bash
# Remove existing .qd_env and recreate
rm -rf .qd_env
quickdeploy run .
```

### Dependency Installation Issues

```bash
# Clear cache and reinstall
quickdeploy cache --clear
quickdeploy run .
```

### Port Already in Use

```bash
# Use a different port
quickdeploy run . --port 9000
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) for CLI
- Uses [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- File watching powered by [Watchdog](https://python-watchdog.readthedocs.io/)

---

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for Python developers**

