"""Application-wide configuration and small helpers."""
from __future__ import annotations

import os
from pathlib import Path

from PySide6.QtCore import QSettings, QStandardPaths

APP_NAME = "YouTube Downloader"
ORG_NAME = "PanhaTools"
APP_VERSION = "1.0.0"

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
APP_ICON_PATH = ASSETS_DIR / "icon.ico"
APP_ICON_PNG = ASSETS_DIR / "icon.png"


# Label -> max height (None = best available)
RESOLUTIONS: list[tuple[str, int | None]] = [
    ("Best", None),
    ("4k (2160p)", 2160),
    ("2k (1440p)", 1440),
    ("1080p", 1080),
    ("720p", 720),
    ("480p", 480),
    ("360p", 360),
    ("Audio only", 0),
]

CONTAINERS = ["MP4", "MKV", "WEBM", "MP3 (audio)", "M4A (audio)"]

AUDIO_CONTAINERS = {"MP3 (audio)": "mp3", "M4A (audio)": "m4a"}


def default_download_dir() -> str:
    """Return the user's Downloads folder (falls back to the home folder)."""
    path = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
    if not path:
        path = str(Path.home())
    return os.path.normpath(path)


def settings() -> QSettings:
    return QSettings(ORG_NAME, APP_NAME)


def human_size(num_bytes: float | None) -> str:
    if not num_bytes:
        return "-"
    step = 1024.0
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if num_bytes < step:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= step
    return f"{num_bytes:.1f} PB"


def human_time(seconds: float | None) -> str:
    if seconds is None:
        return "-"
    seconds = int(seconds)
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:d}:{minutes:02d}:{sec:02d}"
    return f"{minutes:d}:{sec:02d}"
