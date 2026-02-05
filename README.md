# ImageScraper 
**Industry-grade Python Image Scraping & Storage Pipeline**

---

##  Project Summary

**ImageScraper** is a production-style Python project that scrapes **high-quality images** from the web using **Selenium**, stores them locally in a **topic-wise folder structure**, and persists images + metadata into **MongoDB Atlas using GridFS**.

The project is built with **clean architecture**, **modular design**, **logging**, **exception handling**, and **deduplication**, making it fully **resume-ready** and **industry aligned**.

---

##  Key Learning Outcomes

- Selenium automation (real browser control)
- Web scraping best practices
- MongoDB Atlas + GridFS
- Clean Python project structure
- Logging & configuration management
- CLI-based applications
- Git & GitHub workflow
- Deployment awareness

---

##  Features

-  Scrape images by keyword (e.g. `cat`, `audi`, `new york`)
-  Auto-create topic-wise image folders
-  Duplicate detection using SHA-256 checksum
-  Convert `.webp` images → high-quality `.jpg`
-  Skip very small / low-quality images
-  Store images in MongoDB GridFS
-  Store searchable metadata
-  Centralized logging
-  CLI-based execution
-  Cloud-ready (MongoDB Atlas)

---

##  Project Structure

```

ImageScraper/
│
├── src/
│   ├── config/
│   │   └── settings.py
│   │
│   ├── database/
│   │   ├── mongo_client.py
│   │   ├── image_repository.py
│   │   └── image_fetcher.py
│   │
│   ├── downloader/
│   │   └── image_downloader.py
│   │
│   ├── logging_config/
│   │   └── logger.py
│   │
│   ├── scraper/
│   │   └── image_scraper.py
│   │
│   ├── scripts/
│   │   └── export_images.py
│   │
│   ├── utils/
│   │   └── helpers.py
│   │
│   └── main.py
│
├── images/               # Local scraped images (ignored in Git)
├── exported_images/      # Exported from DB (ignored in Git)
├── logs/                 # App logs (ignored in Git)
│
├── .env                  # Environment variables (ignored)
├── .gitignore
├── requirements.txt
└── README.md

````

---

##  Tech Stack

- **Python 3.10+**
- **Selenium**
- **webdriver-manager**
- **Requests**
- **Pillow (PIL)**
- **MongoDB Atlas**
- **GridFS**
- **Logging**

---

##  Environment Variables

Create a `.env` file in the project root:

```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/
DATABASE_NAME=image_scraper
BASE_IMAGE_DIR=images
LOG_LEVEL=INFO
```

>  Never commit `.env` to GitHub.

---

## ️ Running the Scraper

### Basic Command

```
python -m src.main --query "cat" --num 10
```

### Example

```
python -m src.main --query "audi" --num 50 --headless
```

### CLI Arguments

| Argument     | Description         |
| ------------ | ------------------- |
| `--query`    | Search keyword      |
| `--num`      | Number of images    |
| `--headless` | Run Chrome headless |

---

##  Image Storage Logic

### Local Folder Structure

```
images/
 └── audi/
     ├── audi_1.jpg
     ├── audi_2.jpg
     └── audi_3.jpg
```

### MongoDB

* **GridFS** → stores image bytes
* **image_metadata** collection → stores:

  * filename
  * query
  * url
  * checksum
  * created_at

---

##  Quality Filters Applied

* Skip images `< 10 KB`
* Ignore thumbnails & encrypted images
* Convert `.webp` → `.jpg` (quality = 95)
* SHA-256 checksum deduplication
* Selenium stale element handling

---

##  Export Images from MongoDB

```
python -m src.scripts.export_images --query "cat" --limit 10
```

Exports images into `exported_images/`.

---

##  Logging

Logs are written to:

```
logs/app.log
```

Includes:

* Scraping progress
* Errors & retries
* Duplicate skips
* Database operations

---

##  GitHub Push (CMD Only)

### Step 1: Go to Project Root

```
D:
cd "D:\Python Environment\PythonProject\ImageScraper"
```

---

### Step 2: Initialize Git

```
git init
```

---

### Step 3: Add Files

```
git add .
```

---

### Step 4: Commit

```
git commit -m "Initial commit - ImageScraper project"
```

---

### Step 5: Create GitHub Repo (Web)

* Go to [https://github.com](https://github.com)
* Click **New Repository**
* Name: `image-scraper-python`
* Public
* Do NOT add README / .gitignore

---

### Step 6: Link Remote Repo

```
git remote add origin https://github.com/<your github id>/image-scraper-python.git
```

---

### Step 7: Push to GitHub

```
git branch -M main
git push -u origin main
```

---

##  Deployment Notes (Important)

 **Selenium scraping is NOT suitable for free cloud platforms like Heroku.**

Recommended:

* Run scraper **locally**
* Convert project into **FastAPI API**
* Use background workers (Celery / cron jobs)

MongoDB Atlas works perfectly in cloud.

---

## Resume Bullet Points

* Built a **Python-based image scraping pipeline** using Selenium
* Designed **modular architecture** with clean separation of concerns
* Integrated **MongoDB Atlas + GridFS** for binary storage
* Implemented **deduplication using SHA-256**
* Added **logging, error handling, and config management**
* Developed **CLI-based execution flow**

---

##  Author

**Aniket Biradar**

Python | Backend | Automation

India 🇮🇳