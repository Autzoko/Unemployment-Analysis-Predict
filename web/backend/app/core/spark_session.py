from pyspark.sql import SparkSession
from app.core.config import MONGO_URI, MONGO_DB

spark = SparkSession.builder \
    .appName("UnemploymentPlatform") \
    .config("spark.mongodb.read.connection.uri", f"{MONGO_URI}/{MONGO_DB}") \
    .config("spark.mongodb.write.connection.uri", f"{MONGO_URI}/{MONGO_DB}") \
    .getOrCreate()