@echo off
echo ========================================================
echo Starting YouTube Downloader Web App (FastAPI + Web UI)
echo ========================================================

IF EXIST .venv\Scripts\python.exe (
    echo Using virtual environment (.venv)...
    .venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
) ELSE (
    echo Using system Python...
    python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
)

pause
