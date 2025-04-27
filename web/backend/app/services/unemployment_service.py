from app.core.spark_session import spark
from app.core.config import MONGO_DB, MONGO_URI

from pyspark.sql.functions import col, substring

from app.services.state_mapping import STATE_CODE_TO_NAME

def get_state_data(state_code: str, indicator_code: str = "03"):
    
    pass
    


