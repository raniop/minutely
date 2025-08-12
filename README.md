# 🎥 Video Scraper Challenge

This repository contains my solution to the **Video Scraper Challenge** home assignment, which involves extracting video content and metadata from multiple major websites.

---

## 🧠 Objective

1. **Manually extract** embedded video files from 4 URLs.
2. **Collect metadata** for each video: title, date, duration, etc.
3. **Automate** the full process using a Python script.
4. **Document** the approach and tools used.

---

## 🌐 Target URLs

* [CNN](https://edition.cnn.com/2025/07/16/world/video/maynard-gaza-hospitals-nada-bashir-digvid)
* [Mako](https://www.mako.co.il/pzm-soldiers/Article-b1fa03b6e651891027.htm)
* [Fox Sports](https://www.foxsports.com/watch/fmc-5kls1t8t846wq6fu)
* [CBS Sports](https://www.cbssports.com/watch/nfl/video/is-it-a-surprise-that-micah-parsons-is-being-strung-along-by-cowboys)

---

## ⚙️ Tools & Technologies

| Tool / Library   | Purpose                              |
| ---------------- | ------------------------------------ |
| `yt-dlp`         | Video extraction & metadata          |
| `ffmpeg`         | Duration & resolution extraction     |
| `Playwright`     | Browser automation for dynamic sites |
| `BeautifulSoup4` | Metadata scraping from HTML          |
| `json`, `csv`    | Output formatting                    |
| `Python 3.x`     | Main scripting language              |

---

## 🧩 Project Structure

```
.
├── combined_video_downloader.py     # Main script
├── combined_metadata_output.json    # Output metadata
├── requirements.txt                 # Python dependencies
├── downloads_combined/              # Downloaded video files (not uploaded)
└── README.md                        # Project documentation
```

---

## 🧪 Manual Extraction Summary

Video files were downloaded using `yt-dlp` where possible. For more restricted platforms (e.g. Mako, Fox), `Playwright` was used to discover the `.m3u8` URL.

Metadata (title, date, duration, resolution, tags) was collected using:

* `yt-dlp` metadata extractors
* `ffmpeg` for resolution/duration
* HTML scraping with `BeautifulSoup`

---

## 🤖 Automation Script

The script:

1. Accepts a list of URLs
2. Attempts direct extraction via `yt-dlp`
3. If failed, launches `Playwright` to find m3u8
4. Downloads the video
5. Extracts metadata (title, date, tags, duration, resolution)
6. Outputs to `combined_metadata_output.json`

Run with:

```bash
python combined_video_downloader.py
```

---

## 📄 Sample Metadata Output

```json
{
  "title": "Inside Gaza's collapsing hospitals",
  "url": "https://edition.cnn.com/...",
  "duration": "00:02:48",
  "resolution": "1920x1080",
  "categories": ["World", "Gaza"],
  "author": "Nada Bashir",
  "downloaded_file": "cnn_gaza.mp4"
}
```

---

## 📦 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

Ensure you have `ffmpeg` installed and accessible via your system's PATH.

---

## 🧠 Notes & Limitations

* Some platforms (e.g. Mako) require browser-based scraping to access the video stream URL.
* `yt-dlp` is preferred but not always sufficient alone.
* Videos were **not committed** to the repo due to GitHub size limits. You can re-download by running the script.

---

## 🙋 About the Author

Rani Ophir
💻 iOS & Python developer
🌐 [https://github.com/raniop](https://github.com/raniop)
