from pymongo import MongoClient
from app.core.config import MONGO_URI

client = MongoClient(MONGO_URI)

def get_mongo_client() -> MongoClient:
    return client