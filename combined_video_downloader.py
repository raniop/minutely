#!/usr/bin/env python3
import os, re, json, time, logging, subprocess
from urllib.parse import urlparse
from pathlib import Path

import yt_dlp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from playwright.sync_api import sync_playwright

URLS = [
    "https://edition.cnn.com/2025/07/16/world/video/maynard-gaza-hospitals-nada-bashir-digvid",
    "https://www.mako.co.il/pzm-soldiers/Article-b1fa03b6e651891027.htm",
    "https://www.foxsports.com/watch/fmc-5kls1t8t846wq6fu",
    "https://www.cbssports.com/watch/nfl/video/is-it-a-surprise-that-micah-parsons-is-being-strung-along-by-cowboys"
]

OUTPUT_DIR = Path("downloads_combined")
DEBUG_LOG = "combined_debug_log.txt"
METADATA_FILE = "combined_metadata_output.json"
HEADER_ALLOWLIST = {"user-agent", "referer", "origin", "authorization", "cookie", "x-forwarded-for"}

logging.basicConfig(filename=DEBUG_LOG, level=logging.DEBUG, format="%(asctime)s - %(message)s")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_output_path(url):
    domain = urlparse(url).netloc.replace(".", "_")
    return OUTPUT_DIR / f"{domain}_video.mp4"

from urllib.parse import urlparse
import os

def try_ytdlp(url, output_path, headers=None):
    try:
        if ".m3u8" in url:
            domain = urlparse(url).netloc.replace(".", "_")
            output_name = str(output_path)
        else:
            output_name = str(output_path)

        cmd = [
            "yt-dlp",
            url,
            "--force-generic-extractor",  # 💥 הכי חשוב!
            "--referer", "https://www.foxsports.com",
            "--user-agent", "Mozilla/5.0",
            "-o", output_name,
            "--no-playlist",
            "--merge-output-format", "mp4",
            "-f", "bestvideo+bestaudio/best"
        ]

        subprocess.run(cmd, check=True)
        logging.info(f"✅ yt-dlp success: {url}")
        return True
    except Exception as e:
        logging.warning(f"❌ yt-dlp failed: {url} – {e}")
        return False





def extract_m3u8_selenium(url):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(10)
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for frame in iframes:
            try:
                driver.switch_to.frame(frame)
                m3u8s = re.findall(r'https[^"\\s]+\\.m3u8', driver.page_source)
                if m3u8s:
                    driver.quit()
                    return m3u8s[0], {"referer": url}
                driver.switch_to.default_content()
            except Exception:
                driver.switch_to.default_content()
                continue
        m3u8s = re.findall(r'https[^"\\s]+\\.m3u8', driver.page_source)
        driver.quit()
        return (m3u8s[0], {"referer": url}) if m3u8s else (None, None)
    except Exception as e:
        logging.error(f"❌ Selenium error: {e}")
        return None, None

def extract_m3u8_playwright(url):
    try:
        with sync_playwright() as p:
            is_mako = "mako.co.il" in url
            browser = p.chromium.launch(headless=not is_mako, slow_mo=250 if is_mako else 0)
            context = browser.new_context()
            page = context.new_page()

            m3u8_holder = {"url": None, "headers": {}}

            def on_request(req):
                if ".m3u8" in req.url and not m3u8_holder["url"]:
                    print(f"🎯 Found m3u8 request: {req.url}")
                    m3u8_holder["url"] = req.url
                    # capture only whitelisted headers to pass to yt-dlp
                    h = {}
                    for k, v in req.headers.items():
                        if k.lower() in HEADER_ALLOWLIST:
                            h[k.lower()] = v
                    # ensure referer is set
                    h.setdefault("referer", url)
                    m3u8_holder["headers"] = h

            page.on("request", on_request)
            print(f"🌐 Opening page (Playwright) for: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=60000)

            # give the page some time; click to trigger players if needed
            for _ in range(30):
                if m3u8_holder["url"]:
                    break
                try:
                    page.mouse.click(400, 300)
                except Exception:
                    pass
                time.sleep(1)

            browser.close()
            return m3u8_holder["url"], m3u8_holder["headers"]
    except Exception as e:
        logging.error(f"❌ Playwright error: {e}")
        return None, None

def extract_metadata(path):
    try:
        result = subprocess.run([
            "ffprobe", "-v", "quiet", "-print_format", "json",
            "-show_format", "-show_streams", str(path)
        ], capture_output=True, text=True)
        return json.loads(result.stdout) if result.stdout else {}
    except Exception as e:
        logging.warning(f"Metadata error: {e}")
        return {}

all_metadata = []

for url in URLS:
    print(f"⬇️ Trying yt-dlp for: {url}")
    output_path = get_output_path(url)
    metadata = {}

    if try_ytdlp(url, output_path):
        print(f"✅ Downloaded directly: {output_path.name}")
        metadata = extract_metadata(output_path)
    else:
        print("🌐 Trying Playwright...")
        m3u8_url, headers = extract_m3u8_playwright(url)

        if m3u8_url:
            print(f"🎯 Found m3u8: {m3u8_url}")
            if try_ytdlp(m3u8_url, output_path, headers):
                print(f"✅ Downloaded via m3u8: {output_path.name}")
                metadata = extract_metadata(output_path)
            else:
                print("❌ Failed to download via Playwright m3u8")
        else:
            print("🌐 Playwright failed. Trying Selenium...")
            m3u8_url, headers = extract_m3u8_selenium(url)
            if m3u8_url:
                print(f"🎯 Found m3u8 (Selenium): {m3u8_url}")
                if try_ytdlp(m3u8_url, output_path, headers):
                    print(f"✅ Downloaded via Selenium m3u8: {output_path.name}")
                    metadata = extract_metadata(output_path)
                else:
                    print("❌ Failed to download via Selenium m3u8")
            else:
                print("❌ No m3u8 found at all")

    all_metadata.append({
        "url": url,
        "output": output_path.name,
        "metadata": metadata
    })

with open(METADATA_FILE, "w", encoding="utf-8") as f:
    json.dump(all_metadata, f, indent=2, ensure_ascii=False)

print("\\n🎉✅ All done! Check downloads_combined/")
