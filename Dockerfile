FROM python:3.11-slim

# Install system dependencies (FFmpeg for video/audio merging and MP3 conversion)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY Youtube_Downloader/backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Create temp_downloads folder with write permissions
RUN mkdir -p /app/Youtube_Downloader/temp_downloads /app/temp_downloads

ENV PORT=10000
EXPOSE 10000

CMD ["sh", "-c", "uvicorn backend.main:app --app-dir Youtube_Downloader --host 0.0.0.0 --port ${PORT:-10000}"]
