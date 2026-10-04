"""Job Manager for Web Downloads with Threading and Cleanup."""
from __future__ import annotations

import os
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, Optional

from core.downloader import YTDownloaderCore

# Temporary directory for web downloads
DOWNLOAD_DIR = Path(__file__).resolve().parent.parent / "temp_downloads"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Maximum file retention time (seconds): 1 hour
MAX_FILE_AGE = 3600

# Global job status store
# job_id -> { status, percent, speed, eta, filepath, filename, error, created_at }
jobs_db: Dict[str, Dict[str, Any]] = {}

executor = ThreadPoolExecutor(max_workers=3)


def cleanup_old_files() -> None:
    """Remove download files older than MAX_FILE_AGE."""
    now = time.time()
    for job_id, job in list(jobs_db.items()):
        created_at = job.get("created_at", now)
        filepath = job.get("filepath")

        if now - created_at > MAX_FILE_AGE:
            if filepath and os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception:
                    pass
            jobs_db.pop(job_id, None)


def _download_task(job_id: str, url: str, quality: Optional[int], container: str) -> None:
    """Background download task executed in thread pool."""
    jobs_db[job_id]["status"] = "downloading"

    def progress_callback(data: Dict[str, Any]) -> None:
        if job_id in jobs_db:
            state = data.get("status", "")
            if state == "finished":
                jobs_db[job_id]["status"] = "processing"
                jobs_db[job_id]["percent"] = 99.0
            else:
                jobs_db[job_id]["status"] = "downloading"
                jobs_db[job_id]["percent"] = data.get("percent", 0.0)
            jobs_db[job_id]["speed"] = data.get("speed", 0.0)
            jobs_db[job_id]["eta"] = data.get("eta", 0)

    try:
        filepath = YTDownloaderCore.download(
            url=url,
            output_dir=str(DOWNLOAD_DIR),
            height=quality,
            container=container,
            progress_callback=progress_callback,
        )
        if job_id in jobs_db:
            jobs_db[job_id]["status"] = "completed"
            jobs_db[job_id]["percent"] = 100.0
            jobs_db[job_id]["filepath"] = filepath
            jobs_db[job_id]["filename"] = os.path.basename(filepath)
    except Exception as exc:
        if job_id in jobs_db:
            jobs_db[job_id]["status"] = "error"
            jobs_db[job_id]["error"] = str(exc)


def create_download_job(url: str, quality: Optional[int], container: str) -> str:
    """Create a new download job and submit it to executor."""
    cleanup_old_files()

    job_id = str(uuid.uuid4())
    jobs_db[job_id] = {
        "job_id": job_id,
        "url": url,
        "status": "queued",
        "percent": 0.0,
        "speed": 0.0,
        "eta": 0,
        "filepath": None,
        "filename": None,
        "error": None,
        "created_at": time.time(),
    }

    executor.submit(_download_task, job_id, url, quality, container)
    return job_id


def get_job_status(job_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve status for a job_id."""
    return jobs_db.get(job_id)
