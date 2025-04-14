.PHONY: dev install test lint format

# Create venv and install all packages
install:
	pip install -r requirements.txt

# Run FastAPI app with hot reload
dev:
	uvicorn app.main:app --reload

# Run test suite (adjust command to your test runner)
test:
	pytest tests

# Linting (using Ruff or Flake8)
lint:
	ruff check .

# Format code
format:
	ruff format .

