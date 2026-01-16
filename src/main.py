# src/main.py
import argparse
from src.logging_config.logger import get_logger
from src.scraper.image_scraper import ImageScraperPipeline

logger = get_logger("Main")

def main():
    parser = argparse.ArgumentParser(description="ImageScraper pipeline")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--num", type=int, default=10, help="Number of images required")
    parser.add_argument("--no-manager", dest="use_manager", action="store_false", help="Disable webdriver-manager")
    parser.add_argument("--driver", default=None, help="Path to chromedriver.exe (optional)")
    parser.add_argument("--headless", action="store_true", help="Run headless browser")
    args = parser.parse_args()

    pipeline = ImageScraperPipeline(headless=args.headless, driver_path=args.driver, use_manager=args.use_manager)
    results = pipeline.ensure_images_for_query(args.query, args.num)
    logger.info("Returned %d image metadata documents", len(results))
    for r in results:
        logger.info("meta: filename=%s url=%s created_at=%s", r.get("filename"), r.get("url"), r.get("created_at"))

if __name__ == "__main__":
    main()

# How to run
# python -m src.main --query "Narendra Modi" --num 100