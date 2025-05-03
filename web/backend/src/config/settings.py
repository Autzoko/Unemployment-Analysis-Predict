from dotenv import load_dotenv
import os

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..', '.env.dev'))
load_dotenv(env_path)

MONGODB_URI = os.getenv("MONGO_URI")
MONGODB_DB = os.getenv("MONGO_DB")

if not MONGODB_DB or not MONGODB_URI:
    raise ValueError("MONGODB_URI or MONGODB_DB not set in .env.dev")
