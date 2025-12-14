.PHONY: install dev run test clean format lint type-check

# Install production dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
dev:
	pip install -r requirements.txt
	pip install pytest pytest-asyncio httpx black isort flake8 mypy

# Run the development server
run:
	python main.py

# Run tests
test:
	pytest

# Clean cache and temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

# Format code
format:
	black .
	isort .

# Lint code
lint:
	flake8 .

# Type check
type-check:
	mypy .

# Run all checks
check: format lint type-check test

# Setup virtual environment
venv:
	python -m venv venv
	@echo "Activate with: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)"

# Install in virtual environment
venv-install: venv
	./venv/bin/pip install -r requirements.txt

# Help
help:
	@echo "Available commands:"
	@echo "  install     - Install production dependencies"
	@echo "  dev         - Install development dependencies"
	@echo "  run         - Run the development server"
	@echo "  test        - Run tests"
	@echo "  clean       - Clean cache and temporary files"
	@echo "  format      - Format code with black and isort"
	@echo "  lint        - Lint code with flake8"
	@echo "  type-check  - Type check with mypy"
	@echo "  check       - Run all checks (format, lint, type-check, test)"
	@echo "  venv        - Create virtual environment"
	@echo "  venv-install- Create venv and install dependencies"
	@echo "  help        - Show this help message"