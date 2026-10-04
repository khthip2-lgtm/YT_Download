import sys
import os
import urllib.parse
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
    """ASGI entrypoint with robust path resolution for Vercel serverless rewrites."""
    if scope["type"] == "http":
        # 1. Check if Vercel passed _path in the query string
        qs = scope.get("query_string", b"").decode("utf-8")
        params = urllib.parse.parse_qs(qs)

        path_param = params.get("_path", [None])[0]
        if path_param:
            clean_path = path_param.lstrip("/")
            scope["path"] = f"/api/{clean_path}"
            scope["raw_path"] = scope["path"].encode("utf-8")

            # Remove _path from query string so endpoints don't see extra params
            filtered_params = {k: v for k, v in params.items() if k != "_path"}
            scope["query_string"] = urllib.parse.urlencode(filtered_params, doseq=True).encode("utf-8")
        else:
            # Fallback: check headers
            headers = dict(scope.get("headers", []))
            forwarded = (
                headers.get(b"x-matched-path", b"").decode("utf-8")
                or headers.get(b"x-forwarded-uri", b"").decode("utf-8")
            )
            if forwarded and "/api/" in forwarded:
                target = forwarded[forwarded.find("/api/"):]
                scope["path"] = target.split("?")[0]
                scope["raw_path"] = scope["path"].encode("utf-8")

    await fastapi_app(scope, receive, send)
