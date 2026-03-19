import logging
import requests
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.binary import Binary
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MongoDBConnector:
    """Class to manage MongoDB connections and data insertion."""
    
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.collection = None

    def connect(self) -> None:
        """Establishes connection to MongoDB Atlas."""
        try:
            self.client = MongoClient(self.uri)
            self.client.admin.command('ping') 
            self.collection = self.client[self.db_name][self.collection_name]
            logger.info("Successfully connected to MongoDB Atlas.")
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def _download_image_as_binary(self, image_url: str) -> Binary | None:
        """Private method to download an image and convert to BSON Binary."""
        try:
            # Wikimedia requires a descriptive User-Agent, not a fake Browser.
            headers = {
                "User-Agent": "SmartConseil_Scraper_Task/1.0 (mohamedmoamen.tlili@gmail.com)"
            }
            response = requests.get(image_url, headers=headers, timeout=15)
            response.raise_for_status()
            return Binary(response.content)
        except requests.exceptions.RequestException as e:
            logger.warning(f"Could not download image: {e}")
            return None

    def insert_post(self, post_data: Dict[str, Any]) -> None:
        """Inserts a single post into the MongoDB collection along with its image binary."""
        if self.collection is not None:
            try:
                if post_data.get('image_url'):
                    binary_image = self._download_image_as_binary(post_data['image_url'])
                    post_data['image_binary'] = binary_image
                
                self.collection.insert_one(post_data)
                logger.info(f"Inserted post successfully: {post_data.get('post_id')}")
            except Exception as e:
                logger.error(f"Error inserting document: {e}")
        else:
            logger.error("Database not connected. Call connect() first.")