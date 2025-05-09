from pymongo import MongoClient
from config.settings import MONGODB_URI
from utils.logger import get_logger

logger = get_logger(__name__)

_mongo_client = None

def get_mongo_client() -> MongoClient:
    global _mongo_client
    if _mongo_client is None:
        try:
            _mongo_client = MongoClient(
                MONGODB_URI,
                maxPoolSize=50,
                connectTimeoutMS=30000,
                socketTimeoutMS=30000,
                serverSelectionTimeoutMS=30000
            )
            _mongo_client.admin.command("ping")
            logger.info("MongoDB client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize MongoDB client: {e}")
            raise
    return _mongo_client

def close_mongo_client():
    global _mongo_client
    if _mongo_client is not None:
        _mongo_client.close()
        logger.info("MongoDB client closed successfully.")
        _mongo_client = None