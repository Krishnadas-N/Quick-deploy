# Contributing to QuickDeploy

Thank you for your interest in contributing to QuickDeploy! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/quickdeploy.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Install in development mode: `pip install -e ".[dev]"`

## Development Setup

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Lint code
ruff check .
black quickdeploy/
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where possible
- Write docstrings for all public functions and classes
- Keep line length to 100 characters
- Use `ruff` for linting and `black` for formatting

## Testing

- Write tests for new features
- Ensure all tests pass: `pytest tests/ -v`
- Aim for good test coverage

## Submitting Changes

1. Make sure all tests pass
2. Update documentation if needed
3. Commit your changes with clear messages
4. Push to your fork
5. Open a Pull Request

## Pull Request Process

1. Update README.md if needed
2. Add tests for new functionality
3. Ensure CI passes
4. Request review from maintainers

Thank you for contributing! 🎉

