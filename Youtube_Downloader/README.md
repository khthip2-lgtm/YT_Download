# YouTube Downloader (Python + PySide6 + yt-dlp)

កម្មវិធី Desktop សម្រាប់ដោនឡូតវីដេអូពី YouTube ទាំង **Single Video** និង **Playlist**។

## មុខងារ

- បញ្ចូល Link (single ឬ playlist) → ចុច **Fetch** → បញ្ចីវីដេអូបង្ហាញក្នុងតារាង (No / Title / Url / Status / Action)
- ចុច **Download** ដើម្បីចាប់ផ្តើមដោនឡូតទាំងអស់ ឬចុច Download ក្នុងជួរណាមួយដើម្បីដោនឡូតតែវីដេអូនោះ
- **Stop** បញ្ឈប់ការដោនឡូតភ្លាម
- ជ្រើសរើស **Resolution**: Best / 4k / 2k / 1080p / 720p / 480p / 360p / Audio only
- ជ្រើសរើស **Video type**: MP4 / MKV / WEBM / MP3 (audio) / M4A (audio)
- ជ្រើសរើស **Destination** ដោយប្រើ **Browse** (កម្មវិធីចាំទីតាំងចុងក្រោយ)
- Progress bar ក្នុងជួរនីមួយៗ បង្ហាញ % , ល្បឿន និង ETA

## ការដំឡើង

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python main.py
```

### FFmpeg (ត្រូវការ)

សម្រាប់ការបញ្ចូលគ្នា (merge) វីដេអូ+សំឡេង គុណភាពខ្ពស់ និងការបម្លែងទៅ MP3 ត្រូវមាន **ffmpeg** ក្នុងម៉ាស៊ីន៖

- Windows: ទាញយកពី https://www.gyan.dev/ffmpeg/builds/ រួចដាក់ `ffmpeg.exe` ក្នុង PATH
- macOS: `brew install ffmpeg`
- Ubuntu/Debian: `sudo apt install ffmpeg`

## រចនាសម្ព័ន្ធគម្រោង

```
youtube_downloader/
├── main.py                     # ចំណុចចាប់ផ្តើមកម្មវិធី
├── requirements.txt
├── README.md
└── ytdl_app/
    ├── config.py               # Resolution, Video type, ការចាំ settings
    ├── core/
    │   ├── fetcher.py          # FetchWorker (QThread) – ទាញបញ្ជីវីដេអូ
    │   └── downloader.py       # DownloadWorker (QThread) – ដោនឡូត + progress + stop
    └── ui/
        ├── main_window.py      # Layout តាមរូបភាពគម្រូ
        └── styles.py           # ពណ៌ និង Qt stylesheet
```

## របៀបប្រើ

1. Copy link ពី YouTube (វីដេអូតែមួយ ឬ playlist)
2. Paste ក្នុងប្រអប់ខាងលើ រួចចុច **Fetch** (បើប្រអប់ទទេ កម្មវិធីយកពី clipboard ស្វ័យប្រវត្តិ)
3. ជ្រើស Resolution + Video type + Destination
4. ចុច **Download**

## ចំណាំ

- សូមគោរពច្បាប់រក្សាសិទ្ធិ និងលក្ខខណ្ឌប្រើប្រាស់របស់ YouTube — ដោនឡូតតែមាតិកាដែលអ្នកមានសិទ្ធិ។
- បើ YouTube ប្តូររចនាសម្ព័ន្ធ សូម update៖ `pip install -U yt-dlp`
