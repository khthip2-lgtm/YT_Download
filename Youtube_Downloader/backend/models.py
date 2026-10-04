"""Pydantic data models for FastAPI requests and responses."""
from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class InfoRequest(BaseModel):
    url: str = Field(..., example="https://www.youtube.com/watch?v=dQw4w9WgXcQ")


class VideoInfoResponse(BaseModel):
    id: str
    title: str
    uploader: str
    duration: Optional[float] = None
    duration_string: str
    thumbnail: Optional[str] = None
    description: str
    available_resolutions: List[int]
    view_count: int


class DownloadRequest(BaseModel):
    url: str = Field(..., example="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    quality: Optional[int] = Field(default=None, description="Resolution height like 1080, 720 or null for best, 0 for audio only")
    format: str = Field(default="MP4", description="Format container e.g. MP4, MKV, WEBM, MP3, M4A")


class DownloadJobResponse(BaseModel):
    job_id: str
    status: str
    message: str


class JobProgressResponse(BaseModel):
    job_id: str
    status: str  # queued, downloading, completed, error, cancelled
    percent: float
    speed: float
    eta: int
    filename: Optional[str] = None
    error: Optional[str] = None
