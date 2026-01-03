#!/bin/bash
# Setup script for sensor-backend

echo "========================================="
echo "Sensor Backend Setup"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Error: Python is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo "✓ Python found: $($PYTHON_CMD --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
$PYTHON_CMD -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to create virtual environment"
    exit 1
fi

echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to activate virtual environment"
    exit 1
fi

echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Check for poppler-utils
echo "Checking system dependencies..."
if command -v pdftoppm &> /dev/null; then
    echo "✓ poppler-utils is installed"
else
    echo "⚠️  Warning: poppler-utils is not installed"
    echo "   This is required for PDF processing in form-ocr module"
    echo ""
    echo "   Install with:"
    echo "   - Ubuntu/Debian: sudo apt-get install poppler-utils"
    echo "   - macOS: brew install poppler"
    echo "   - Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases"
fi

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "To activate the virtual environment:"
echo "  source venv/bin/activate"
echo ""
echo "To run the server:"
echo "  python main.py"
echo ""
echo "Or use the convenience script:"
echo "  ./run.sh"
echo ""
