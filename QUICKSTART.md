# QuickDeploy Quick Start Guide

Get up and running with QuickDeploy in 5 minutes!

## Installation

```bash
# Clone and install
git clone https://github.com/yourusername/quickdeploy.git
cd quickdeploy
pip install -e .
```

## Example 1: Run a FastAPI Project

```bash
# Create a new FastAPI project
quickdeploy init fastapi my-api
cd my-api

# Run it!
quickdeploy run .
```

Open http://127.0.0.1:8000 in your browser!

## Example 2: Run a Flask Project

```bash
# Create a new Flask project
quickdeploy init flask my-app
cd my-app

# Run it!
quickdeploy run .
```

## Example 3: Run Your Existing Project

```bash
# Navigate to your project
cd /path/to/your/project

# Make sure you have requirements.txt or pyproject.toml
# Then run:
quickdeploy run .
```

## Example 4: Use the GUI

```bash
# Launch the GUI
quickdeploy-gui

# Then:
# 1. Click "Browse" to select your project
# 2. Click "Run" to start
# 3. Watch logs in real-time
# 4. Click "Stop" when done
```

## Configuration

Create `.quickdeploy.yaml` in your project:

```yaml
entrypoint: app.py
port: 8000
auto_reload: true
```

That's it! QuickDeploy handles the rest automatically.

## Troubleshooting

**Problem**: Virtual environment creation fails
**Solution**: Make sure you have Python 3.10+ installed and `venv` module available

**Problem**: Dependencies won't install
**Solution**: Check your `requirements.txt` or `pyproject.toml` syntax

**Problem**: Port already in use
**Solution**: Use `--port` flag: `quickdeploy run . --port 9000`

## Next Steps

- Read the full [README.md](README.md)
- Check out [examples](examples/) directory
- Join our community discussions

Happy coding! 🚀

