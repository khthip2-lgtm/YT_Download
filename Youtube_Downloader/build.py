"""Build script for packaging YouTube Downloader with PyInstaller."""
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
VENV_PYTHON = ROOT_DIR / ".venv" / "Scripts" / "python.exe"
PYTHON_EXE = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable

ICON_PATH = ROOT_DIR / "ytdl_app" / "assets" / "icon.ico"
ASSETS_ARG = f"{ROOT_DIR / 'ytdl_app' / 'assets'};ytdl_app/assets"

cmd = [
    PYTHON_EXE,
    "-m",
    "PyInstaller",
    "--noconsole",
    "--onefile",
    "--name",
    "YouTube Downloader",
    "--icon",
    str(ICON_PATH),
    "--add-data",
    ASSETS_ARG,
    "--clean",
    "-y",
    str(ROOT_DIR / "main.py"),
]

print("Building YouTube Downloader...")
print("Running command:", " ".join(cmd))
res = subprocess.run(cmd, cwd=str(ROOT_DIR))
if res.returncode == 0:
    exe_path = ROOT_DIR / "dist" / "YouTube Downloader.exe"
    print("\n[SUCCESS] Build completed!")
    print(f"Standalone executable located at: {exe_path}")
else:
    print(f"\n[FAILED] Build failed with return code {res.returncode}")
    sys.exit(res.returncode)
