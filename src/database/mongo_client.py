# src/database/mongo_client.py
from pymongo import MongoClient, ASCENDING
import gridfs
from src.logging_config.logger import get_logger
from src.config.settings import MONGO_URI, DATABASE_NAME

logger = get_logger("MongoDBClient")

class MongoDBClient:
    def __init__(self, uri: str = None, dbname: str = None):
        uri = uri or MONGO_URI
        dbname = dbname or DATABASE_NAME
        if not uri:
            raise ValueError("MONGO_URI not set in environment (.env)")

        self.client = MongoClient(uri)
        self.db = self.client[dbname]
        self.fs = gridfs.GridFS(self.db)
        # ensure indexes for performance
        self.db["image_metadata"].create_index([("query", ASCENDING)])
        self.db["image_metadata"].create_index([("checksum", ASCENDING)])
        logger.info("Connected to MongoDB database=%s", dbname)
