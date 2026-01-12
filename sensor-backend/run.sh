#!/bin/bash
# Run script for the semantic sensor backend
source venv/bin/activate
export HF_HUB_ENABLE_HF_TRANSFER=1
echo "Starting Semantic Sensor API server..."
python main.py