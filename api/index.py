import sys
import os
from pathlib import Path

# Add Youtube_Downloader to sys.path so modules import properly
BASE_DIR = Path(__file__).resolve().parent.parent / "Youtube_Downloader"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from Youtube_Downloader.backend.main import app as fastapi_app
except ImportError:
    import importlib

    fastapi_app = importlib.import_module("backend.main").app


async def app(scope, receive, send):
    """ASGI entrypoint with path resolution for Vercel serverless rewrites."""
    if scope["type"] == "http":
        headers = dict(scope.get("headers", []))

        # 1. Check if Vercel provided the original client URL
        forwarded_uri = headers.get(b"x-forwarded-uri", b"").decode("utf-8")
        matched_path = headers.get(b"x-matched-path", b"").decode("utf-8")

        current_path = scope.get("path", "")
        # If current path is generic or pointing to index.py, resolve from headers
        if current_path in ["/api", "/api/", "/api/index.py", ""] or not current_path.startswith("/api/"):
            if forwarded_uri:
                scope["path"] = forwarded_uri.split("?")[0]
            elif matched_path and matched_path not in ["/api", "/api/", "/api/index.py"]:
                scope["path"] = matched_path.split("?")[0]

    await fastapi_app(scope, receive, send)
