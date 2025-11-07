"""FastAPI template generator."""

from pathlib import Path


def create_fastapi_template(project_path: Path) -> bool:
    """Create a FastAPI template project."""
    project_path = Path(project_path)
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Create app.py
    app_content = '''"""FastAPI application template."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="QuickDeploy FastAPI App", version="1.0.0")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Hello from QuickDeploy FastAPI!"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/api/items")
async def get_items():
    """Example API endpoint."""
    return {"items": [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
'''
    
    (project_path / "app.py").write_text(app_content, encoding="utf-8")
    
    # Create requirements.txt
    requirements = """fastapi>=0.104.0
uvicorn[standard]>=0.24.0
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
    readme = """# FastAPI QuickDeploy Project

This is a FastAPI project set up with QuickDeploy.

## Running

```bash
quickdeploy run .
```

The API will be available at http://127.0.0.1:8000

## Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/items` - Example items endpoint
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation
"""
    (project_path / "README.md").write_text(readme, encoding="utf-8")
    
    return True

