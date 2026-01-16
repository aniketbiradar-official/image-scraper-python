# src/downloader/image_downloader.py
import requests
from typing import Tuple, Optional
from src.logging_config.logger import get_logger

logger = get_logger("Downloader")

class ImageDownloader:
    def __init__(self, user_agent: str = "ImageScraper/1.0"):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    def download(self, url: str, timeout: int = 15) -> Tuple[Optional[bytes], Optional[str]]:
        try:
            resp = self.session.get(url, timeout=timeout)
            resp.raise_for_status()
            return resp.content, resp.headers.get("Content-Type")
        except requests.RequestException:
            logger.exception("RequestException while downloading: %s", url)
            return None, None
        except Exception:
            logger.exception("Unexpected error downloading: %s", url)
            return None, None
