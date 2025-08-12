# 📄 README_RUN.md

## 🎯 מטרת הקובץ
הורדת סרטוני וידאו באופן אוטומטי מאתרים כמו Mako, FoxSports, CNN, CBS ועוד, באמצעות `combined_video_downloader.py`.

---

## 🛠️ דרישות מקדימות

1. Python 3.9+
2. Chrome מותקן במחשב
3. ChromeDriver תואם לגרסת Chrome  
   להורדה: https://chromedriver.chromium.org/
4. yt-dlp מותקן (מומלץ להתקין דרך pip)
5. הפעלת venv

---

## 🗂️ מבנה תיקיות (לפני ההרצה)

```
your_project_folder/
├── combined_video_downloader.py
├── combined_metadata_output.json
├── requirements.txt
├── README_RUN.md
```

---

## ⚙️ התקנות (פעם אחת בלבד)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -U yt-dlp
```

---

## ▶️ הרצת הסקריפט

```bash
python3 combined_video_downloader.py
```

---

## 📁 תוצרי ההורדה

- כל הסרטונים יישמרו בתיקייה:
  ```
  downloads_combined/
  ```

- אם ההורדה נכשלה, יופיע לוג מתאים בקובץ:
  ```
  combined_debug_log.txt
  ```

- עם סיום ההרצה יווצר קובץ CSV בשם:
  ```
  combined_metadata_output.csv
  ```

---

## 🧪 בדיקה מהירה (לא חובה)

```bash
python3 combined_video_downloader.py --test
```

---

## ❗ הערות

- ודא ש־ChromeDriver נמצא ב־PATH או בתיקייה הנוכחית.
- אפשר להפעיל גם על Windows אך הדוגמאות ניתנו ל־macOS/Linux.