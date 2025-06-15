from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType

# 1 Build Spark Session
spark = SparkSession.builder \
    .appName("KafkaStream") \
    .master("spark://spark-master:7077") \
    .getOrCreate()
    
# Define schema matching your JSON messages
schema = StructType([
    StructField("count", IntegerType()),
    StructField("ts", DoubleType())
])

# parse the json value and select fields
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "test-1") \
    .load()
    
parsed = df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.count", "data.ts")
    
# write to console 
query = parsed.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()
    
query.awaitTermination()