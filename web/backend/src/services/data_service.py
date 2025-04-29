from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from typing import List
from models.response_model import UnemploymentRateResponse
from config.settings import MONGODB_DB, MONGODB_URI
from utils.logger import get_logger
from utils.spark_session import get_spark_session

logger = get_logger(__name__)

def get_unemployment_data(year: int, month: int) -> List[UnemploymentRateResponse]:
    logger.info(f"Fetching unemployment data for  year={year}, month={month}")

    spark = get_spark_session()

    try:
        basic_info_df = spark.read.format("com.mongodb.spark.sql.DefaultSource") \
            .option("uri", f"{MONGODB_URI}/{MONGODB_DB}.basic_info") \
            .load() \
            .select("area_code", "area_text")
        
        basic_info_df.cache()

        state_mappings = {
            row["area_code"]: row["area_text"]
            for row in basic_info_df.collect()
            if row["area_text"] is not None
        }
        logger.debug(f"Loaded {len(state_mappings)} state mappings")

        state_dfs = []

        for state_code, state_name in state_mappings.items():
            if state_name is None:
                logger.warning(f"Skipped state_code={state_code} since state_name is None")
            collection_name = f"states_{state_name.replace(' ', '')}"

            pipeline = [
                {"$match": {
                    "year": year,
                    "period": f"M{month:02}",
                    "series_id": {"$regex": "03$"}
                }},
                {"$project": {
                    "value": 1,
                    "area_code": state_code
                }}
            ]

            state_df = spark.read.format("com.mongodb.spark.sql.DefaultSource") \
                .option("uri", f"{MONGODB_URI}/{MONGODB_DB}.{collection_name}") \
                .option("pipeline", str(pipeline)) \
                .load()
            
            state_dfs.append(state_df)

        if not state_dfs:
            logger.warning("No state collections found")
            return []
        
        from functools import reduce
        from pyspark.sql import DataFrame

        unioned_df = reduce(DataFrame.unionAll, state_dfs)

        result_df = unioned_df.join(
            basic_info_df,
            unioned_df["area_code"] == basic_info_df["area_code"],
            "inner"
        ).select(
            col("area_text").alias("state"),
            col("value").cast("float")
        )

        results = [
            UnemploymentRateResponse(state=row["state"], value=row["value"])
            for row in result_df.collect()
        ]

        logger.info(f"Retrived {len(results)} unemployment records")
        return results
    
    except Exception as e:
        logger.error(f"Error fetching unemployment data: {str(e)}")
        raise

    finally:
        basic_info_df.unpersist()