import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

PROCESSED_DATA_DIR='dataset/processed'
ENV_FILE='.env.dev' #change to .env when deploying

def load_mongo_config(env_file=ENV_FILE):
    load_dotenv(env_file)
    mongo_uri = os.getenv('MONGO_URI')
    mongo_db = os.getenv('MONGO_DB')
    
    if not mongo_uri or not mongo_db:
        raise ValueError("MONGO_URI and MONGO_DB must be set in the environment variables.")
    return mongo_uri, mongo_db

def upload_csv_to_mongo(csv_path, collection, series_id=None):
    try:
        df = pd.read_csv(csv_path)
        if df.empty:
            return
        
        if series_id:
            df['series_id'] = series_id

        collection.insert_many(df.to_dict(orient='records'))
        print(f"Uploaded {len(df)} records to {collection.name} from {csv_path}")
    except Exception as e:
        print(f"Failed to upload {csv_path}: {e}")
    
def upload_all(processed_root=PROCESSED_DATA_DIR):
    mongo_uri, mongo_db = load_mongo_config()
    
    client = MongoClient(mongo_uri)
    db = client[mongo_db]

    for root, _, files in os.walk(processed_root):
        for file in files:
            if not file.endswith('.csv'):
                continue

            file_path = os.path.join(root, file)
            rel_parts = os.path.relpath(file_path, processed_root).split(os.sep)

            if rel_parts[0] == 'states':
                state_name = rel_parts[1]
                series_id = os.path.splitext(file)[0]
                collection_name = f"states_{state_name}"
                collection = db[collection_name]
                upload_csv_to_mongo(file_path, collection, series_id)
            else:
                collection = db["basic_info"]
                upload_csv_to_mongo(file_path, collection)
    client.close()
    print("All files uploaded to MongoDB.")

if __name__ == "__main__":      
    upload_all()
# This script uploads CSV files from the processed dataset directory to MongoDB.
# It uses the pymongo library to connect to MongoDB and insert records.
# The script first loads MongoDB configuration from environment variables using dotenv.
# It then traverses the processed dataset directory, identifies CSV files, and uploads them to the appropriate MongoDB collections.
