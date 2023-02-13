from pyspark.sql import SparkSession
import os
import sys
from credentials.credentials import (
    storage_account_name, storage_account_key, storage_container_name)

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

spark = SparkSession.builder\
    .appName("StreamLocalToAzure") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-azure:3.2.1") \
    .master("local[*]")\
    .getOrCreate()
    
spark.conf.set("spark.sql.streaming.schemaInference", True)
spark.conf.set(
 	f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net",
 	storage_account_key)
spark.conf.set(
	"spark.sql.streaming.checkpointLocation",
	f"wasbs://{storage_container_name}@{storage_account_name}.blob.core.windows.net/checkpoint/")

df = spark \
    .readStream \
    .format("binaryFile") \
    .option("maxFilesPerTrigger", 1) \
    .option("cleanSource", "DELETE") \
    .option("startingOffsets", "latest") \
    .load("./device_output/*.png")
      
df.writeStream \
    .outputMode("append") \
    .format("json") \
    .option("path", f"wasbs://{storage_container_name}@{storage_account_name}.blob.core.windows.net/") \
    .start() \
    .awaitTermination();
    
