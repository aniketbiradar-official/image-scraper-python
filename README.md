# ImageScraper 

ImageScraper is a production-style image scraping pipeline built using Python and Selenium.  
It downloads high-quality images from Bing Images, stores them in topic-wise local folders, and persists image data and metadata in MongoDB Atlas using GridFS.

The project follows industry-standard practices such as modular architecture, structured logging, exception handling, deduplication, and configuration management. It is designed to be resume-ready and extensible for real-world use cases.

---

##  Features

- Scrapes images from Bing Images using Selenium
- Automatically creates topic-wise folders (e.g., images/cat/)
- Duplicate image detection using SHA-256 checksum
- Filters out very small and low-quality images
- Converts WebP images to JPEG for better compatibility
- Stores images and metadata in MongoDB Atlas using GridFS
- Command-line interface (CLI) support
- Structured logging and error handling
- Modular and scalable project structure

---

##  Tech Stack

- Python 3.11+
- Selenium
- webdriver-manager
- MongoDB Atlas
- GridFS
- Pillow
- Requests
- python-dotenv
- Logging

---

##  Project Structure

ImageScraper/

├── src/

│   ├── config/

│   │   └── settings.py

│   ├── database/

│   │   ├── mongo_client.py

│   │   ├── image_repository.py

│   │   └── image_fetcher.py

│   ├── downloader/

│   │   └── image_downloader.py

│   ├── logging_config/

│   │   └── logger.py

│   ├── scraper/

│   │   └── image_scraper.py

│   ├── scripts/

│   │   └── export_images.py

│   ├── utils/

│   │   └── helpers.py

│   └── main.py

│
├── images/               # Auto-generated topic-wise images (gitignored)

├── logs/                 # Application logs (gitignored)

├── .env                  # Environment variables (gitignored)

├── requirements.txt

├── .gitignore

└── README.md

---

##  Setup Instructions

### Step 1: Clone the Repository

git clone https://github.com/<your-username>/image-scraper-python.git  
cd image-scraper-python

---

### Step 2: Create and Activate Virtual Environment

python -m venv .venv

Windows:
.venv\Scripts\activate

Linux / macOS:
source .venv/bin/activate

---

### Step 3: Install Dependencies

pip install -r requirements.txt

---

### Step 4: Configure Environment Variables

Create a `.env` file in the project root with the following content:

MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net  
DATABASE_NAME=image_scraper

Important: Do NOT commit the `.env` file to GitHub.

---

##  How to Run

Run the application using the CLI:

python -m src.main --query "cat" --num 10

Example:

python -m src.main --query "audi" --num 50

---

##  Output

Local images are saved in topic-wise folders:

images/

└── audi/

    ├── audi_1.jpg
    ├── audi_2.jpg
    ├── audi_3.jpg
    └── ...

MongoDB Collections Used:
- fs.files
- fs.chunks
- image_metadata

---

##  Design Decisions

- Bing Images is used instead of Google Images due to better scraping stability
- Checksum-based deduplication prevents storing duplicate images
- Quality-first approach ensures low-value images are skipped
- WebP to JPEG conversion improves cross-platform compatibility
- Modular design allows easy extension to APIs or frontends

---

##  Future Enhancements

- FastAPI-based image retrieval API
- Asynchronous scraping for better performance
- Image resolution-based filtering
- Dockerization
- Web-based frontend interface

---

## 👤 Author

Aniket Biradar

---

## 📄 License

This project is intended for educational and portfolio purposes only.
