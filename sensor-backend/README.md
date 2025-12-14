# Semantic Sensor Backend

FastAPI backend for the Semantic Description Sensor application using sentence transformers.

## Setup

### Using pip (recommended)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

### Using Poetry (alternative)
```bash
# Install poetry if not already installed
pip install poetry

# Install dependencies
poetry install

# Run the server
poetry run python main.py
```

### Using conda (alternative)
```bash
# Create conda environment
conda create -n semantic-sensor python=3.10
conda activate semantic-sensor

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

## Development

### Install development dependencies
```bash
pip install -r requirements.txt
pip install pytest pytest-asyncio httpx black isort flake8 mypy
```

### Code formatting
```bash
black .
isort .
```

### Type checking
```bash
mypy .
```

### Running tests
```bash
pytest
```

## API Documentation

Once the server is running, visit:
- API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Environment Variables

Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

## Model Download

The sentence transformer model (`all-MiniLM-L6-v2`) will be automatically downloaded on first run. This may take a few minutes depending on your internet connection.