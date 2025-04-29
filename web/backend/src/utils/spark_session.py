from pyspark.sql import SparkSession
from config.settings import MONGODB_URI
from utils.logger import get_logger

logger = get_logger(__name__)

_spark_session = None

def get_spark_session() -> SparkSession:
    global _spark_session
    if _spark_session is None:
        logger.info("Initializing Spark session...")
        _spark_session = SparkSession.builder \
            .appName("UnemploymentData") \
            .config("spark.mongodb.input.uri", MONGODB_URI) \
            .config("spark.mongodb.output.uri", MONGODB_URI) \
            .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
            .getOrCreate()
    
    return _spark_session


def stop_spark_session():
    global _spark_session
    if _spark_session is not None:
        logger.info("Stopping Spark session...")
        _spark_session.stop()
        _spark_session = None