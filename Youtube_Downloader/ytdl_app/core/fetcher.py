"""Background worker that resolves a YouTube URL into a list of videos.

Handles both a single video URL and a playlist / channel URL.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from PySide6.QtCore import QThread, Signal

import yt_dlp


@dataclass
class VideoItem:
    """One row of the download list."""

    title: str
    url: str
    video_id: str = ""
    duration: float | None = None
    status: str = "Ready"
    progress: float = 0.0
    filepath: str = ""
    extra: dict = field(default_factory=dict)


def _watch_url(entry: dict) -> str:
    url = entry.get("webpage_url") or entry.get("url") or ""
    vid = entry.get("id") or ""
    if url and url.startswith("http"):
        return url
    if vid:
        return "https://www.youtube.com/watch?v=" + vid
    return url


class FetchWorker(QThread):
    """Extracts video metadata without downloading anything."""

    item_found = Signal(object)          # VideoItem
    message = Signal(str)                # status-bar text
    failed = Signal(str)                 # error text
    finished_ok = Signal(int, bool)      # count, is_playlist

    def __init__(self, url: str, parent=None) -> None:
        super().__init__(parent)
        self._url = url.strip()

    def run(self) -> None:  # noqa: D102
        opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "ignoreerrors": True,
            "noplaylist": False,
            # Flat extraction keeps playlist fetching fast.
            "extract_flat": "in_playlist",
        }
        try:
            self.message.emit("កំពុងទាញព័ត៌មានពី YouTube...")
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(self._url, download=False)
        except Exception as exc:  # noqa: BLE001 - surfaced in the UI
            self.failed.emit(str(exc))
            return

        if info is None:
            self.failed.emit("រកមិនឃើញវីដេអូសម្រាប់តំណនេះទេ។")
            return

        entries = info.get("entries")
        count = 0

        if entries:  # playlist / channel
            for entry in entries:
                if self.isInterruptionRequested():
                    break
                if not entry:
                    continue
                item = VideoItem(
                    title=entry.get("title") or "(no title)",
                    url=_watch_url(entry),
                    video_id=entry.get("id") or "",
                    duration=entry.get("duration"),
                )
                self.item_found.emit(item)
                count += 1
            self.finished_ok.emit(count, True)
        else:  # single video
            item = VideoItem(
                title=info.get("title") or "(no title)",
                url=_watch_url(info),
                video_id=info.get("id") or "",
                duration=info.get("duration"),
            )
            self.item_found.emit(item)
            self.finished_ok.emit(1, False)
