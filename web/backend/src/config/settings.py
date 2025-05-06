from dotenv import load_dotenv
import os

env_path = "/app/.env"
load_dotenv(env_path)

MONGODB_URI = os.getenv("MONGO_URI")
MONGODB_DB = os.getenv("MONGO_DB")
MONGODB_PREDICTION = os.getenv("MONGO_PREDICTION_DB")

if not MONGODB_DB or not MONGODB_URI:
    raise ValueError("MONGODB_URI or MONGODB_DB not set in .env")
