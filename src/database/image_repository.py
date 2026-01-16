# src/database/image_repository.py
from datetime import datetime, timezone
from typing import Optional, List
from bson.objectid import ObjectId
from src.logging_config.logger import get_logger

logger = get_logger("ImageRepository")

class ImageRepository:
    def __init__(self, mongo_client):
        self.db = mongo_client.db
        self.fs = mongo_client.fs
        self.meta = self.db["image_metadata"]

    def count_images(self, query: str) -> int:
        return self.meta.count_documents({"query": query})

    def list_for_query(self, query: str, limit: int = 10) -> List[dict]:
        cursor = self.meta.find({"query": query}).sort("created_at", -1).limit(limit)
        return list(cursor)

    def checksum_exists(self, checksum: str) -> bool:
        return self.meta.count_documents({"checksum": checksum}) > 0

    def save_image(self, image_bytes: bytes, filename: str, query: str, url: str, content_type: Optional[str] = None) -> Optional[dict]:
        # compute checksum before calling if caller didn't
        import hashlib
        checksum = hashlib.sha256(image_bytes).hexdigest()
        if self.checksum_exists(checksum):
            logger.info("Checksum exists. Skipping save for %s", filename)
            return None
        try:
            gridfs_id = self.fs.put(image_bytes, filename=filename, content_type=content_type)
            doc = {
                "query": query,
                "filename": filename,
                "gridfs_id": gridfs_id,
                "url": url,
                "checksum": checksum,
                "created_at": datetime.now(timezone.utc)
            }
            self.meta.insert_one(doc)
            logger.info("Saved image metadata id=%s filename=%s", str(gridfs_id), filename)
            return doc
        except Exception:
            logger.exception("Failed to save image/metadata")
            return None

    def get_image_bytes(self, gridfs_id: ObjectId) -> Optional[bytes]:
        try:
            return self.fs.get(gridfs_id).read()
        except Exception:
            logger.exception("Failed to read image bytes from GridFS")
            return None
