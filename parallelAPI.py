import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, explode, lit
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, IntegerType

spark = SparkSession.builder.appName("REST_API_with_PySpark_DF").getOrCreate()

schema = StructType([
    StructField("field1", StringType(), True),
    StructField("field2", IntegerType(), True),
    # ... Define other fields based on the API's response
])

@udf(returnType=ArrayType(schema))
def fetch_data(offset: int, limit: int):
    endpoint = "https://api.example.com/data"
    params = {
        "offset": offset,
        "limit": limit
    }
    response = requests.get(endpoint, params=params)
    return response.json()  # assuming API returns a list of records

total_records = requests.get("https://api.example.com/data", params={"offset": 0, "limit": 1}).json().get('total', 0)
records_per_page = 500

offsets_df = spark.range(0, total_records, records_per_page).select(col("id").alias("offset"), lit(records_per_page).alias("limit"))
response_df = offsets_df.withColumn("response", fetch_data("offset", "limit"))
results_df = response_df.select(explode("response"))