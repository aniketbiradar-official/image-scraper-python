# src/scripts/export_images.py

import argparse
import os
from io import BytesIO
from PIL import Image

from src.database.image_fetcher import ImageFetcher
from src.utils.helpers import ensure_dir, sanitize_filename
from src.logging_config.logger import get_logger

logger = get_logger("ExportImages")

BASE_OUTPUT_DIR = "exported_images"


def export_images(query: str, limit: int):
    fetcher = ImageFetcher()

    # 🔹 Fetch ONLY metadata for this query
    metadata_list = fetcher.fetch_metadata_by_query(query, limit)

    if not metadata_list:
        logger.warning("No images found for query='%s'", query)
        return

    logger.info("Found %d images for query='%s'", len(metadata_list), query)

    # 🔹 Create per-query folder
    topic_dir = os.path.join(BASE_OUTPUT_DIR, sanitize_filename(query))
    ensure_dir(topic_dir)

    for idx, meta in enumerate(metadata_list, start=1):
        image_bytes = fetcher.fetch_image_bytes(meta["gridfs_id"])

        filename = f"{sanitize_filename(query)}_{idx}.jpg"
        output_path = os.path.join(topic_dir, filename)

        try:
            # 🔹 Convert everything → JPG
            image = Image.open(BytesIO(image_bytes)).convert("RGB")
            image.save(output_path, "JPEG", quality=95)

            logger.info("Saved image: %s", output_path)

        except Exception as e:
            logger.error("Failed to export image %d: %s", idx, e)


def main():
    parser = argparse.ArgumentParser(description="Export images from MongoDB by query")
    parser.add_argument("--query", required=True, help="Search query (e.g. lion, cat)")
    parser.add_argument("--limit", type=int, default=20, help="Number of images to export")

    args = parser.parse_args()

    export_images(args.query, args.limit)


if __name__ == "__main__":
    main()
