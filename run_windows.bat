@echo off
echo ========================================
echo   NFL Plus Predictor - Launcher
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Download from https://python.org
    pause
    exit /b 1
)

:: Install dependencies
echo Installing dependencies...
python -m pip install "streamlit>=1.65.0" requests pandas numpy --quiet

echo.
echo Starting NFL Plus...
echo Open your browser at: http://localhost:8501
echo Press Ctrl+C to stop.
echo.
streamlit run app.py --server.port 8501 --server.headless false
pause
