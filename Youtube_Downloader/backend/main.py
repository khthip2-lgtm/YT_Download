"""FastAPI Server for YouTube Downloader Web Application."""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Add project root directory to sys.path so modules import correctly
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from core.downloader import YTDownloaderCore, is_valid_youtube_url
from backend.models import (
    DownloadJobResponse,
    DownloadRequest,
    InfoRequest,
    JobProgressResponse,
    VideoInfoResponse,
)
from backend.downloader import (
    create_download_job,
    get_job_status,
    cleanup_old_files,
)

app = FastAPI(
    title="YouTube Downloader API",
    description="FastAPI Backend for YouTube Video/Audio Downloader Web App (Mobile & Desktop)",
    version="1.0.0",
)

# Enable CORS for mobile devices & cross-origin apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WEB_DIR = BASE_DIR / "web"


# 1. Web UI Homepage & API Status Check
@app.get("/")
def serve_home():
    """Serve the Web UI frontend at the root URL."""
    index_file = WEB_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {
        "status": "online",
        "service": "YouTube Downloader API",
        "version": "1.0.0",
    }


@app.get("/api")
@app.get("/api/status")
@app.get("/status")
def status_check():
    """Check API server status."""
    return {
        "status": "online",
        "service": "YouTube Downloader API",
        "version": "1.0.0",
    }


# 2. Extract Video Information
@app.post("/api/info", response_model=VideoInfoResponse)
@app.post("/info", response_model=VideoInfoResponse)
def get_video_info(req: InfoRequest):
    """Fetch video metadata and available qualities from YouTube URL."""
    if not is_valid_youtube_url(req.url):
        raise HTTPException(
            status_code=400,
            detail="URL YouTube មិនត្រឹមត្រូវទេ! (Invalid YouTube URL)",
        )

    try:
        info = YTDownloaderCore.fetch_video_info(req.url)
        return VideoInfoResponse(**info)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# 3. Start Download Job
@app.post("/api/download", response_model=DownloadJobResponse)
@app.post("/download", response_model=DownloadJobResponse)
def start_download(req: DownloadRequest, background_tasks: BackgroundTasks):
    """Start background download job for a YouTube URL."""
    if not is_valid_youtube_url(req.url):
        raise HTTPException(
            status_code=400,
            detail="URL YouTube មិនត្រឹមត្រូវទេ! (Invalid YouTube URL)",
        )

    # Schedule background cleanup of old files
    background_tasks.add_task(cleanup_old_files)

    try:
        job_id = create_download_job(
            url=req.url,
            quality=req.quality,
            container=req.format,
        )
        return DownloadJobResponse(
            job_id=job_id,
            status="queued",
            message="ទាញយកបានចាប់ផ្តើមក្នុង Queue",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# 4. Check Job Download Progress
@app.get("/api/progress/{job_id}", response_model=JobProgressResponse)
@app.get("/progress/{job_id}", response_model=JobProgressResponse)
def get_progress(job_id: str):
    """Get real-time download progress for a specific job."""
    job = get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="រកមិនឃើញ Job ID នេះទេ")

    return JobProgressResponse(
        job_id=job["job_id"],
        status=job["status"],
        percent=job["percent"],
        speed=job["speed"],
        eta=job["eta"],
        filename=job.get("filename"),
        error=job.get("error"),
    )


# 5. Serve & Download Completed File
@app.get("/api/file/{job_id}")
@app.get("/file/{job_id}")
def download_file(job_id: str):
    """Serve the downloaded file for browser/mobile download."""
    job = get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="រកមិនឃើញ Job ID នេះទេ")

    if job["status"] != "completed" or not job.get("filepath"):
        raise HTTPException(
            status_code=400,
            detail=f"File មិនទាន់ Download រួចរាល់ទេ (Status: {job['status']})",
        )

    filepath = job["filepath"]
    if not os.path.exists(filepath):
        # Fallback check in temp_downloads
        filename = job.get("filename")
        if filename:
            fallback = os.path.join(str(BASE_DIR / "temp_downloads"), filename)
            if os.path.exists(fallback):
                filepath = fallback

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File ត្រូវបានលុប ឬ រកមិនឃើញ")

    filename = job.get("filename") or os.path.basename(filepath)
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="application/octet-stream",
    )


# Mount Web Frontend Static Files (only for local / non-Vercel environments)
if not os.environ.get("VERCEL") and WEB_DIR.exists():
    app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="web")
