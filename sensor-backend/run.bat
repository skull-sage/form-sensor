@echo off
REM Run script for the semantic sensor backend (Windows)

echo Starting Semantic Sensor API server...
call venv\Scripts\activate.bat
python main.py
