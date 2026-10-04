FROM python:3.11-slim

# Install system dependencies (FFmpeg for video/audio processing)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Create temp_downloads folder with permissions
RUN mkdir -p /app/temp_downloads

# Port fallback for cloud hosts (Render, Railway, etc.)
ENV PORT=8000
EXPOSE 8000

CMD exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}
