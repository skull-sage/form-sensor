@echo off
REM Setup script for sensor-backend (Windows)

echo =========================================
echo Sensor Backend Setup
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Python found: %PYTHON_VERSION%
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed
echo.

REM Check for poppler
echo Checking system dependencies...
where pdftoppm >nul 2>&1
if errorlevel 1 (
    echo Warning: poppler-utils is not installed
    echo This is required for PDF processing in form-ocr module
    echo.
    echo Download from: https://github.com/oschwartz10612/poppler-windows/releases
    echo Extract and add to PATH
) else (
    echo poppler-utils is installed
)

echo.
echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo To activate the virtual environment:
echo   venv\Scripts\activate
echo.
echo To run the server:
echo   python main.py
echo.
echo Or use the convenience script:
echo   run.bat
echo.
pause
