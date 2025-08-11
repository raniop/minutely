# Unified Video Downloader

Downloads videos (CNN, Mako, Fox Sports, CBS) by:
1) Trying yt-dlp directly
2) Falling back to Playwright to capture .m3u8 (and downloading it)
3) Falling back to Selenium if needed
Exports ffprobe metadata to JSON.

## Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

## Run
python3 combined_video_downloader.py

Outputs:
- videos -> downloads_combined/
- metadata -> combined_metadata_output.json
- debug log -> combined_debug_log.txt
