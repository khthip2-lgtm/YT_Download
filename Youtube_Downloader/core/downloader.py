"""Core YouTube Downloader logic using yt-dlp.
This module is independent of any UI framework (PySide6 / FastAPI / Web).
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Callable, Dict, Optional

import yt_dlp

YOUTUBE_URL_REGEX = re.compile(
    r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/(watch\?v=|embed/|v/|shorts/)?([a-zA-Z0-9_-]{11})"
)

AUDIO_CONTAINERS = {
    "MP3": "mp3",
    "M4A": "m4a",
    "MP3 (audio)": "mp3",
    "M4A (audio)": "m4a",
}

# Auto-detect local bin/ffmpeg.exe if available
BIN_DIR = Path(__file__).resolve().parent.parent / "bin"
FFMPEG_EXE = BIN_DIR / ("ffmpeg.exe" if os.name == "nt" else "ffmpeg")
if BIN_DIR.exists():
    bin_path_str = str(BIN_DIR)
    if bin_path_str not in os.environ.get("PATH", ""):
        os.environ["PATH"] = bin_path_str + os.pathsep + os.environ.get("PATH", "")


def is_valid_youtube_url(url: str) -> bool:
    """Validate if the string is a valid YouTube URL."""
    if not url or not isinstance(url, str):
        return False
    return bool(YOUTUBE_URL_REGEX.search(url.strip()))


def build_format_selector(height: Optional[int], container: str) -> tuple[str, dict]:
    """Return (format_selector, extra yt-dlp options) for the chosen quality and format.

    :param height: Target vertical resolution (e.g. 1080, 720, 480) or None for best, or 0 for audio only.
    :param container: Target container format e.g. "MP4", "MKV", "WEBM", "MP3", "M4A".
    """
    extra: dict = {}
    container_upper = container.upper()
    audio_ext = AUDIO_CONTAINERS.get(container_upper) or (container_upper if container_upper in ("MP3", "M4A") else None)

    # Audio only request
    if height == 0 or audio_ext:
        codec = audio_ext or "mp3"
        extra["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": codec,
                "preferredquality": "192",
            }
        ]
        return "bestaudio/best", extra

    ext = container.lower()  # mp4 / mkv / webm
    extra["merge_output_format"] = ext

    if height is None:
        if ext == "mkv":
            selector = "bestvideo+bestaudio/best"
        elif ext == "mp4":
            selector = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best"
        elif ext == "webm":
            selector = "bestvideo[ext=webm]+bestaudio[ext=webm]/bestvideo+bestaudio/best[ext=webm]/best"
        else:
            selector = "bestvideo+bestaudio/best"
        return selector, extra

    if ext == "mkv":
        selector = (
            f"bestvideo[height<={height}]+bestaudio/"
            f"best[height<={height}]/best"
        )
    elif ext == "mp4":
        selector = (
            f"bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/"
            f"bestvideo[height<={height}]+bestaudio/"
            f"best[height<={height}][ext=mp4]/"
            f"best[height<={height}]/best"
        )
    elif ext == "webm":
        selector = (
            f"bestvideo[height<={height}][ext=webm]+bestaudio[ext=webm]/"
            f"bestvideo[height<={height}]+bestaudio/"
            f"best[height<={height}][ext=webm]/"
            f"best[height<={height}]/best"
        )
    else:
        selector = (
            f"bestvideo[height<={height}]+bestaudio/"
            f"best[height<={height}]/best"
        )
    return selector, extra


def format_duration(seconds: Optional[float]) -> str:
    """Format duration in seconds to HH:MM:SS or MM:SS."""
    if seconds is None:
        return "N/A"
    sec_int = int(seconds)
    mins, sec = divmod(sec_int, 60)
    hrs, mins = divmod(mins, 60)
    if hrs > 0:
        return f"{hrs:d}:{mins:02d}:{sec:02d}"
    return f"{mins:d}:{sec:02d}"


class YTDownloaderCore:
    """Core video info extractor and downloader using yt-dlp."""

    @staticmethod
    def fetch_video_info(url: str) -> Dict[str, Any]:
        """Extract metadata from YouTube URL without downloading."""
        if not is_valid_youtube_url(url):
            raise ValueError("URL YouTube មិនត្រឹមត្រូវទេ! (Invalid YouTube URL)")

        ydl_opts: Dict[str, Any] = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "skip_download": True,
        }
        if BIN_DIR.exists():
            ydl_opts["ffmpeg_location"] = str(BIN_DIR)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url.strip(), download=False)
            if info is None:
                raise ValueError("មិនអាចទាញយកព័ត៌មានពី Video បានទេ")

            duration = info.get("duration")
            formats_raw = info.get("formats", [])

            # Extract unique video resolutions available
            resolutions = set()
            for fmt in formats_raw:
                h = fmt.get("height")
                if h and isinstance(h, int) and h > 0:
                    resolutions.add(h)

            sorted_resolutions = sorted(list(resolutions), reverse=True)

            return {
                "id": info.get("id"),
                "title": info.get("title", "Untitled Video"),
                "uploader": info.get("uploader", "Unknown"),
                "duration": duration,
                "duration_string": format_duration(duration),
                "thumbnail": info.get("thumbnail"),
                "description": (info.get("description") or "")[:200],
                "available_resolutions": sorted_resolutions,
                "view_count": info.get("view_count", 0),
            }

    @staticmethod
    def download(
        url: str,
        output_dir: str,
        height: Optional[int] = None,
        container: str = "MP4",
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
        cancel_check: Optional[Callable[[], bool]] = None,
    ) -> str:
        """Download video to target directory and return final filename/path."""
        if not is_valid_youtube_url(url):
            raise ValueError("URL YouTube មិនត្រឹមត្រូវទេ! (Invalid YouTube URL)")

        os.makedirs(output_dir, exist_ok=True)
        selector, extra_opts = build_format_selector(height, container)

        def _internal_hook(d: dict) -> None:
            if cancel_check and cancel_check():
                raise Exception("CANCELLED_BY_USER")

            if progress_callback:
                state = d.get("status", "")
                total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                downloaded = d.get("downloaded_bytes") or 0
                percent = (downloaded / total * 100.0) if total > 0 else 0.0
                speed = d.get("speed") or 0
                eta = d.get("eta") or 0

                progress_callback({
                    "status": state,
                    "percent": round(percent, 1),
                    "downloaded_bytes": downloaded,
                    "total_bytes": total,
                    "speed": speed,
                    "eta": eta,
                    "filename": d.get("filename", ""),
                })

        ydl_opts: Dict[str, Any] = {
            "format": selector,
            "outtmpl": os.path.join(output_dir, "%(title).150s [%(id)s].%(ext)s"),
            "progress_hooks": [_internal_hook],
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "retries": 3,
            "continuedl": True,
            "windowsfilenames": True,
        }
        if BIN_DIR.exists():
            ydl_opts["ffmpeg_location"] = str(BIN_DIR)

        ydl_opts.update(extra_opts)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url.strip(), download=True)
            if not info:
                raise RuntimeError("Download failed: could not fetch media info")

            filepath = ""
            if "requested_downloads" in info and info["requested_downloads"]:
                filepath = info["requested_downloads"][0].get("filepath", "")
            if not filepath or not os.path.exists(filepath):
                filepath = info.get("_filename", "")
            if not filepath or not os.path.exists(filepath):
                filepath = ydl.prepare_filename(info)

            # Safeguard: if extension changed during postprocessing (e.g. merged to mp4/mkv), find by ID
            if not os.path.exists(filepath):
                vid_id = info.get("id", "")
                if vid_id:
                    for f in os.listdir(output_dir):
                        if vid_id in f and not f.endswith(".temp") and not f.endswith(".part"):
                            candidate = os.path.join(output_dir, f)
                            if os.path.exists(candidate):
                                filepath = candidate
                                break

            return filepath
