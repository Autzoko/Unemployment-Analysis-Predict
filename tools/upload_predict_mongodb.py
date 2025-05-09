import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

PROCESSED_DATA_DIR='dataset/predict'
ENV_FILE='.env.dev'

def load_mongo_config(env_file=ENV_FILE):
    load_dotenv(env_file)
    mongo_uri = os.getenv('MONGO_URI')
    mongo_pred = os.getenv("MONGO_PREDICTION_DB")
    
    if not mongo_uri or not mongo_pred:
        raise ValueError("MONGO_URI and MONGO_DB must be set in the environment variables.")
    return mongo_uri, mongo_pred

COLLECTION_NAME = "PredictionData"

CSV_DIR = os.path.join(os.path.dirname(__file__), '../dataset/predict')

def upload_predictions():
    mongo_uri, mongo_pred = load_mongo_config()
    client = MongoClient(mongo_uri)
    db = client[mongo_pred]
    collection = db[COLLECTION_NAME]

    for filename in os.listdir(CSV_DIR):
        if filename.endswith('.csv'):
            filepath = os.path.join(CSV_DIR, filename)
            df = pd.read_csv(filepath)

            df = df[['year', 'period', 'value', 'state_name']].copy()
            df['month'] = df['period'].str.extract(r'M(\d{2})').astype(int)
            df['year'] = df['year'].astype(int)
            df['unemployment_rate'] = df['value'].astype(float)
            df['state'] = df['state_name'].str.strip()

            records = df[['state', 'year', 'month', 'unemployment_rate']].to_dict(orient='records')

            if records:
                collection.insert_many(records)
                print(f"Inserted {len(records)} records from file: {filename}")

    client.close()

if __name__ == "__main__":
    upload_predictions()
