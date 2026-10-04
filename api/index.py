import sys
import os
from pathlib import Path

# Add Youtube_Downloader to sys.path so modules import properly
BASE_DIR = Path(__file__).resolve().parent.parent / "Youtube_Downloader"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.main import app
