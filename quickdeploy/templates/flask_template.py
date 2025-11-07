"""Flask template generator."""

from pathlib import Path


def create_flask_template(project_path: Path) -> bool:
    """Create a Flask template project."""
    project_path = Path(project_path)
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Create app.py
    app_content = '''"""Flask application template."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def root():
    """Root endpoint."""
    return jsonify({"message": "Hello from QuickDeploy Flask!"})


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


@app.route("/api/items")
def get_items():
    """Example API endpoint."""
    return jsonify({"items": [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
'''
    
    (project_path / "app.py").write_text(app_content, encoding="utf-8")
    
    # Create requirements.txt
    requirements = """flask>=3.0.0
"""
    (project_path / "requirements.txt").write_text(requirements, encoding="utf-8")
    
    # Create .quickdeploy.yaml
    config = """entrypoint: app.py
port: 8000
python_version: null
auto_reload: true
watch_patterns:
  - "*.py"
  - "*.yaml"
  - "*.yml"
ignore_patterns:
  - "*.pyc"
  - "__pycache__"
  - ".git"
  - ".qd_env"
env_vars: {}
install_args: []
"""
    (project_path / ".quickdeploy.yaml").write_text(config, encoding="utf-8")
    
    # Create README
    readme = """# Flask QuickDeploy Project

This is a Flask project set up with QuickDeploy.

## Running

```bash
quickdeploy run .
```

The API will be available at http://127.0.0.1:8000

## Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/items` - Example items endpoint
"""
    (project_path / "README.md").write_text(readme, encoding="utf-8")
    
    return True

