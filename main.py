import os
import logging
from dotenv import load_dotenv
from database import MongoDBConnector
from scraper import InstagramConnector

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

def main():
    MONGO_URI = os.getenv("MONGO_URI")
    if not MONGO_URI:
        logger.error("MONGO_URI is missing. Check your .env file.")
        return

    DB_NAME = "SmartConseilTest"
    COLLECTION_NAME = "social_media_posts"
    SUBJECT_HASHTAG = "jacqueschirac" 
    MAX_POSTS = 5 

    db_connector = MongoDBConnector(MONGO_URI, DB_NAME, COLLECTION_NAME)
    try:
        db_connector.connect()
    except Exception as e:
        logger.error(f"Exiting due to database connection failure: {e}")
        return

    scraper = InstagramConnector()
    
    logger.info(f"Initiating extraction for subject: {SUBJECT_HASHTAG}")
    posts = scraper.fetch_posts_by_hashtag(SUBJECT_HASHTAG, MAX_POSTS)

    if posts:
        logger.info(f"Successfully extracted {len(posts)} posts. Saving to DB...")
        for post in posts:
            db_connector.insert_post(post)
        logger.info("Process completed successfully.")
    else:
        logger.warning("No posts were found or extracted.")

if __name__ == "__main__":
    main()