from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pymongo import MongoClient
import olake

def create_spark_session():
    return (SparkSession.builder
            .appName("MongoDB to Iceberg Sync")
            .config("spark.jars.packages", 
                   "org.apache.iceberg:iceberg-spark-runtime-3.4_2.12:1.3.1,"
                   "org.mongodb.spark:mongo-spark-connector_2.12:10.2.1")
            .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
            .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog")
            .config("spark.sql.catalog.spark_catalog.type", "hive")
            .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog")
            .config("spark.sql.catalog.local.type", "hadoop")
            .config("spark.sql.catalog.local.warehouse", "s3a://warehouse/")
            .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000")
            .config("spark.hadoop.fs.s3a.access.key", "minioadmin")
            .config("spark.hadoop.fs.s3a.secret.key", "minioadmin")
            .config("spark.hadoop.fs.s3a.path.style.access", "true")
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
            .getOrCreate())

def sync_mongodb_to_iceberg():
    # Create Spark session
    spark = create_spark_session()
    
    # Read data from MongoDB
    mongo_df = (spark.read.format("mongodb")
               .option("uri", "mongodb://root:example@localhost:27017/sample_db.orders")
               .load())
    
    # Create Iceberg table
    mongo_df.writeTo("local.db.orders") \
        .tableProperty("format-version", "2") \
        .using("iceberg") \
        .createOrReplace()
    
    print("Successfully synced MongoDB data to Iceberg")
    
    # Query the Iceberg table
    print("\nQuerying Iceberg table:")
    spark.sql("SELECT * FROM local.db.orders LIMIT 5").show()

if __name__ == "__main__":
    sync_mongodb_to_iceberg() 