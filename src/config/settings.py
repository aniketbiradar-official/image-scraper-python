# src/config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = "image_scraper"

IMAGE_COLLECTION = "image_metadata"

BASE_IMAGE_DIR = os.path.join(os.getcwd(), "images")
