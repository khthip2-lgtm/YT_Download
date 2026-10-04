"""Background worker that downloads the queued videos one by one."""
from __future__ import annotations

import os

from PySide6.QtCore import QThread, Signal

import yt_dlp

from ..config import AUDIO_CONTAINERS


class CancelledError(Exception):
    """Raised inside the yt-dlp progress hook when the user presses Stop."""


from core.downloader import build_format_selector as core_build_format

def build_format(height: int | None, container: str) -> tuple[str, dict]:
    return core_build_format(height, container)
    """Return (format_selector, extra yt-dlp options) for the chosen quality."""
    extra: dict = {}
    audio_ext = AUDIO_CONTAINERS.get(container)

    # Audio-only request (either "Audio only" resolution or an audio container)
    if height == 0 or audio_ext:
        extra["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_ext or "mp3",
                "preferredquality": "192",
            }
        ]
        return "bestaudio/best", extra

    ext = container.lower()  # mp4 / mkv / webm
    extra["merge_output_format"] = ext

    if height is None:
        selector = (
            f"bestvideo[ext={ext}]+bestaudio/bestvideo+bestaudio/best[ext={ext}]/best"
            if ext != "mkv"
            else "bestvideo+bestaudio/best"
        )
        return selector, extra

    if ext == "mkv":
        selector = (
            f"bestvideo[height<={height}]+bestaudio/"
            f"best[height<={height}]/best"
        )
    else:
        selector = (
            f"bestvideo[height<={height}][ext={ext}]+bestaudio[ext=m4a]/"
            f"bestvideo[height<={height}]+bestaudio/"
            f"best[height<={height}]/best"
        )
    return selector, extra


class DownloadWorker(QThread):
    """Downloads a list of (row, url) pairs sequentially."""

    progress = Signal(int, float, str)      # row, percent, detail text
    status = Signal(int, str)               # row, status text
    item_done = Signal(int, bool, str)      # row, success, message / filepath
    all_finished = Signal(int, int)         # completed, failed

    def __init__(
        self,
        jobs: list[tuple[int, str]],
        dest_dir: str,
        height: int | None,
        container: str,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._jobs = jobs
        self._dest_dir = dest_dir
        self._height = height
        self._container = container
        self._stop = False
        self._current_row = -1

    def stop(self) -> None:
        """Ask the worker to cancel as soon as possible."""
        self._stop = True
        self.requestInterruption()

    # -- yt-dlp hook ----------------------------------------------------
    def _hook(self, data: dict) -> None:
        if self._stop:
            raise CancelledError

        row = self._current_row
        state = data.get("status")

        if state == "downloading":
            total = data.get("total_bytes") or data.get("total_bytes_estimate") or 0
            done = data.get("downloaded_bytes") or 0
            percent = (done / total * 100.0) if total else 0.0
            speed = data.get("speed")
            eta = data.get("eta")
            detail = "{:.1f}%".format(percent)
            if speed:
                detail += "  •  {:.2f} MB/s".format(speed / 1024 / 1024)
            if eta:
                detail += "  •  ETA {}s".format(int(eta))
            self.progress.emit(row, percent, detail)
        elif state == "finished":
            self.progress.emit(row, 100.0, "កំពុងបញ្ចូលគ្នា (merging)...")
            self.status.emit(row, "Processing")

    # -- main loop ------------------------------------------------------
    def run(self) -> None:  # noqa: D102
        completed = 0
        failed = 0
        selector, extra = build_format(self._height, self._container)
        os.makedirs(self._dest_dir, exist_ok=True)

        base_opts = {
            "format": selector,
            "outtmpl": os.path.join(self._dest_dir, "%(title).200B [%(id)s].%(ext)s"),
            "progress_hooks": [self._hook],
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "ignoreerrors": False,
            "retries": 3,
            "fragment_retries": 3,
            "continuedl": True,
            "windowsfilenames": True,
        }
        base_opts.update(extra)

        for row, url in self._jobs:
            if self._stop:
                self.status.emit(row, "Cancelled")
                continue

            self._current_row = row
            self.status.emit(row, "Downloading")
            try:
                with yt_dlp.YoutubeDL(dict(base_opts)) as ydl:
                    info = ydl.extract_info(url, download=True)
                    path = ""
                    if isinstance(info, dict):
                        path = info.get("requested_downloads", [{}])[0].get(
                            "filepath", ""
                        ) or info.get("_filename", "")
                completed += 1
                self.status.emit(row, "Done")
                self.item_done.emit(row, True, path)
            except CancelledError:
                self.status.emit(row, "Cancelled")
                self.item_done.emit(row, False, "Cancelled by user")
                break
            except Exception as exc:  # noqa: BLE001 - reported per row
                failed += 1
                self.status.emit(row, "Error")
                self.item_done.emit(row, False, str(exc))

        self.all_finished.emit(completed, failed)
