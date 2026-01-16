# src/database/image_fetcher.py
from typing import List
from bson import ObjectId
from src.database.mongo_client import MongoDBClient
from src.logging_config.logger import get_logger

logger = get_logger("ImageFetcher")

class ImageFetcher:
    def __init__(self):
        self.mongo = MongoDBClient()
        self.db = self.mongo.db
        self.fs = self.mongo.fs
        self.meta = self.db["image_metadata"]

    def fetch_metadata_by_query(self, query: str, limit: int = 10) -> List[dict]:
        return list(
            self.meta.find({"query": query})
            .sort("created_at", -1)
            .limit(limit)
        )

    def fetch_image_bytes(self, gridfs_id: ObjectId) -> bytes:
        return self.fs.get(gridfs_id).read()
