from app.core.spark_session import spark
from app.core.config import MONGO_DB, MONGO_URI
from app.core.mongo_client import get_mongo_client

def load_state_mapping() -> dict:
    '''
    Return <State-Full-Name, State-Code> mapping.
    '''
    full_collection_uri = f"{MONGO_URI}/{MONGO_DB}.basic_info"

    df = spark.read.format("mongo") \
        .option("uri", full_collection_uri) \
        .load()
    
    pdf = df.toPandas()
    mapping = dict(zip(pdf['area_code'], pdf['area_text']))
    return {v: k for k, v in mapping.items()}

def get_area_code_by_area_name(area_name: str) -> str:
    client = get_mongo_client()
    db = client[MONGO_DB]
    collection = db["basic_info"]

    result = collection.find_one({"area_text": area_name})

    if not result:
        raise ValueError(f'Area: {area_name} not found in database')
    
    return result["area_code"]