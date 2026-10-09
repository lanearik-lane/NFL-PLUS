#!/bin/bash
echo "========================================"
echo "  NFL Plus Predictor - Launcher"
echo "========================================"
echo

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found. Install from https://python.org"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
python3 -m pip install streamlit requests pandas numpy --quiet

echo
echo "Starting NFL Plus..."
echo "Open your browser at: http://localhost:8501"
echo "Press Ctrl+C to stop."
echo
streamlit run app.py --server.port 8501
