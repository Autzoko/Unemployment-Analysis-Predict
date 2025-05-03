import os
import pandas as pd
from pymongo import MongoClient

# MongoDB 配置
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "unemployment_db"
COLLECTION_NAME = "predictions"

# CSV 文件目录
CSV_DIR = os.path.join(os.path.dirname(__file__), '../dataset/predict')

def upload_predictions():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    for filename in os.listdir(CSV_DIR):
        if filename.endswith('.csv'):
            filepath = os.path.join(CSV_DIR, filename)
            df = pd.read_csv(filepath)

            # 清理数据：提取年月、转换类型
            df = df[['year', 'period', 'value', 'state_name']].copy()
            df['month'] = df['period'].str.extract(r'M(\d{2})').astype(int)
            df['year'] = df['year'].astype(int)
            df['unemployment_rate'] = df['value'].astype(float)
            df['state'] = df['state_name'].str.strip()

            # 最终字段结构
            records = df[['state', 'year', 'month', 'unemployment_rate']].to_dict(orient='records')

            if records:
                collection.insert_many(records)
                print(f"Inserted {len(records)} records from file: {filename}")

    client.close()

if __name__ == "__main__":
    upload_predictions()
