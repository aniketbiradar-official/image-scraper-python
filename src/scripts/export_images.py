# src/scripts/export_images.py
import os
from src.database.image_fetcher import ImageFetcher
from src.utils.helpers import ensure_dir
from src.logging_config.logger import get_logger

logger = get_logger("ExportImages")

OUTPUT_DIR = "exported_images"

def main():
    query = "cat"   # 🔁 change this to any search term
    limit = 10

    ensure_dir(OUTPUT_DIR)

    fetcher = ImageFetcher()
    metadata_list = fetcher.fetch_metadata_by_query(query, limit)

    logger.info("Found %d images for query='%s'", len(metadata_list), query)

    for idx, meta in enumerate(metadata_list, start=1):
        image_bytes = fetcher.fetch_image_bytes(meta["gridfs_id"])
        filename = meta.get("filename", f"{query}_{idx}.jpg")

        output_path = os.path.join(OUTPUT_DIR, filename)

        with open(output_path, "wb") as f:
            f.write(image_bytes)

        logger.info("Saved image: %s", output_path)

if __name__ == "__main__":
    main()
