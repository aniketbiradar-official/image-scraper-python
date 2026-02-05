# src/scraper/image_scraper.py
from typing import List, Optional
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

from io import BytesIO
from PIL import Image

from src.logging_config.logger import get_logger
from src.utils.helpers import sanitize_filename, sha256_bytes, ext_from_content_type
from src.database.mongo_client import MongoDBClient
from src.database.image_repository import ImageRepository
from src.downloader.image_downloader import ImageDownloader
from src.config.settings import BASE_IMAGE_DIR
from src.utils.helpers import get_topic_image_dir

logger = get_logger("ImageScraperPipeline")

class ImageScraperPipeline:
    def __init__(self, headless: bool = True, driver_path: Optional[str] = None, use_manager: bool = True):
        self.headless = headless
        self.driver_path = driver_path
        self.use_manager = use_manager
        self.downloader = ImageDownloader()
        # database client + repository
        self.mongo = MongoDBClient()
        self.repo = ImageRepository(self.mongo)

    def build_driver(self):
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )

        try:
            if self.driver_path and os.path.exists(self.driver_path):
                service = Service(executable_path=self.driver_path)
            elif self.use_manager:
                bin_path = ChromeDriverManager().install()
                service = Service(executable_path=bin_path)
            else:
                service = Service()
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except WebDriverException:
            logger.exception("Failed starting webdriver")
            raise

    def fetch_image_urls(self, query: str, max_links_to_fetch: int = 20) -> List[str]:
        driver = self.build_driver()
        image_urls = set()

        try:
            search_url = f"https://www.bing.com/images/search?q={query}&form=HDRSC2"
            driver.get(search_url)

            time.sleep(2)  # allow images to load

            thumbnails = []

            for _ in range(5):  # scroll 5 times
                thumbnails.extend(driver.find_elements(By.CSS_SELECTOR, "img.mimg"))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)

            thumbnails = thumbnails[:max_links_to_fetch]

            for thumb in thumbnails:
                if len(image_urls) >= max_links_to_fetch:
                    break

                try:
                    src = thumb.get_attribute("src")

                    if src and src.startswith("http"):
                        image_urls.add(src)
                        logger.info("Collected Bing image URL")

                except Exception:
                    continue

            return list(image_urls)

        finally:
            try:
                driver.quit()
            except Exception:
                pass

    def ensure_images_for_query(self, query: str, required_count: int) -> List[dict]:
        # return metadata documents for up to required_count images (existing + newly saved)
        existing_count = self.repo.count_images(query)
        logger.info("Existing images for '%s': %d", query, existing_count)
        if existing_count >= required_count:
            logger.info("Already have enough images; returning existing metadata")
            return self.repo.list_for_query(query, limit=required_count)

        to_add = required_count - existing_count
        logger.info("Need to add %d images for query '%s'", to_add, query)

        # fetch candidate URLs (fetch extra to allow for duplicates)
        candidate_urls = self.fetch_image_urls(query, max_links_to_fetch=to_add * 20)
        saved_meta = []
        for url in candidate_urls:
            if len(saved_meta) >= to_add:
                break
            img_bytes, content_type = self.downloader.download(url)
            if not img_bytes:
                continue
            # Skip very small images (likely icons / tracking pixels)
            if len(img_bytes) < 10_000:  # ~10 KB
                logger.info("Skipping very small image")
                continue
            checksum = sha256_bytes(img_bytes)
            if self.repo.checksum_exists(checksum):
                logger.info("Duplicate detected by checksum, skipping url=%s", url)
                continue
            # Create topic-specific folder
            topic_dir = get_topic_image_dir(BASE_IMAGE_DIR, query)

            image_index = existing_count + len(saved_meta) + 1
            # Convert WEBP to JPG for easier viewing
            if content_type == "image/webp":
                image = Image.open(BytesIO(img_bytes)).convert("RGB")
                filename = sanitize_filename(f"{query}_{image_index}") + ".jpg"
                local_path = os.path.join(topic_dir, filename)
                image.save(local_path, "JPEG", quality=95)
            else:
                filename = sanitize_filename(f"{query}_{image_index}") + ext_from_content_type(content_type)
                local_path = os.path.join(topic_dir, filename)
                with open(local_path, "wb") as f:
                    f.write(img_bytes)

            logger.info("Saved image locally at %s", local_path)

            # Save image to MongoDB
            meta = self.repo.save_image(
                image_bytes=img_bytes,
                filename=filename,
                query=query,
                url=url,
                content_type=content_type
            )
            if meta:
                saved_meta.append(meta)

        # return up to required_count metadata
        return self.repo.list_for_query(query, limit=required_count)
