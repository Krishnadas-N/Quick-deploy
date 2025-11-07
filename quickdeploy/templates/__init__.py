"""Template scaffolding for QuickDeploy."""

from pathlib import Path
from typing import Dict
from .fastapi_template import create_fastapi_template
from .flask_template import create_flask_template


TEMPLATES: Dict[str, callable] = {
    "fastapi": create_fastapi_template,
    "flask": create_flask_template
}


def create_template(template_name: str, project_path: Path) -> bool:
    """Create a project from a template."""
    if template_name not in TEMPLATES:
        return False
    
    project_path = Path(project_path)
    project_path.mkdir(parents=True, exist_ok=True)
    
    return TEMPLATES[template_name](project_path)

