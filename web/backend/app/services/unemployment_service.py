from app.core.spark_session import spark
from app.core.config import MONGO_DB, MONGO_URI

from pyspark.sql.functions import col, substring, lit

from app.services.state_mapping import STATE_CODE_TO_NAME

def get_state_data(year: int, month: int, indicator_code: str = "03"):
    all_collection_uri = [
        f'{MONGO_URI}/{MONGO_DB}.states_{state_name}' for state_name in STATE_CODE_TO_NAME.values()
    ]
    period = f"M{month:02}"
    if indicator_code == '03':
        result_df = None

        for collection_uri in all_collection_uri:
            df = spark.read.format('mongodb') \
                .option("uri", collection_uri) \
                .load()
            
            if df.rdd.isEmpty():
                continue

            df = df.withColumn("indicator_code", substring(col("series_id"), -2, 2))

            df_filtered = df.filter(
                (col("year") == year) &
                (col("period") == period) &
                (col("indicator_code") == "03")
            ).select(
                lit(collection_uri[7:]).alias("State"),
                "value"
            )

            if result_df is None:
                result_df = df_filtered
            else:
                result_df = result_df.union(df_filtered)
        
        if result_df is None:
            raise ValueError("No matching data found")
        
        pdf = result_df.toPandas()
        return pdf
    else:
        return None




    
    


