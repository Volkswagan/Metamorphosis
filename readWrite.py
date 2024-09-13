from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder.appName("OracleToHive").enableHiveSupport().getOrCreate()

# Define Oracle connection properties
oracle_properties = {
    "driver": "oracle.jdbc.driver.OracleDriver",
    "url": "jdbc:oracle:thin:@//your_oracle_host:your_port/your_service_name",
    "user": "your_username",
    "password": "your_password",
    "dbtable": "(select * from table_name where eff_dt between '01SEP2022' AND '30SEP2022') myTable"
}

# Read data from Oracle
df = spark.read.format("jdbc") \
    .options(**oracle_properties) \
    .option("numPartitions", 10) \
    .option("partitionColumn", "id") \
    .option("lowerBound", 1) \
    .option("upperBound", 1000) \
    .load()

hdfs_location = "hdfs:///base/silver/app/table"
df.write.format("parquet") \
    .mode("overwrite") \
    .save(hdfs_location)

# Stop Spark session
spark.stop()
