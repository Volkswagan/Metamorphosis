#DQ Checks
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql import DataFrame
# Import Deequ modules
from deequ import Check, Analyzer
from deequ.checks import CheckLevel, Check
from deequ.constraints import *
from deequ.analyzers import *

# Read data from the Bronze layer in Delta format
bronze_df = spark.read.format("delta").load("/Application/Bronze/table_name")

# Define Data Quality checks
def run_data_quality_checks(df: DataFrame) -> (DataFrame, DataFrame):
    
    check = Check(spark, CheckLevel.Error, "DQ Checks")
    # Define the checks
    check = check \
        .isComplete("id") \  # Ensure 'id' column has no null values
        .isUnique("id") \  # Ensure 'id' column values are unique
        .isComplete("name") \  # Ensure 'name' column has no null values
        .satisfies("age >= 18 AND age <= 60", "Valid age range") \  # Ensure 'age' is between 18 and 60
        .isNonNegative("salary") \  # Ensure 'salary' column values are non-negative
        .containsPattern("email", r"^[\w\.-]+@[\w\.-]+\.\w+$") \  # Ensure 'email' column values match email pattern
        .containsPattern("phone", r"^\d{10}$") \  # Ensure 'phone' column has 10-digit numbers
        .isNonNegative("transaction_amount") \  # Ensure 'transaction_amount' column is non-negative
        .hasApproxQuantile("income", 0.5, lambda x: x >= 30000) \  # Ensure median income is above a threshold
        .isContainedIn("product_id", ["prod_001", "prod_002", "prod_003"]) \  # Ensure 'product_id' values are valid
        .hasCompleteness("address", lambda x: x >= 0.9) \  # Ensure at least 90% of 'address' column values are non-null
        .hasLength("zip_code", lambda x: x == 5) \  # Ensure 'zip_code' column values have exactly 5 characters

    # Run the checks
    verification_result = Analyzer(spark).verify(df, check)

    # Extract passed and failed records
    dq_passed_df = df.filter(verification_result.successful)
    bad_records_df = df.filter(~verification_result.successful)
    
    return dq_passed_df, bad_records_df

# Perform Data Quality checks
dq_passed_df, bad_records_df = run_data_quality_checks(bronze_df)

dq_passed_df.write.format("delta").mode("overwrite").path("/Application/Silver/table_name")
bad_records_df.write.format("delta").mode("overwrite").path("/Application/Silver_HISTORY/table_name")

##########################################################################
#Upsert / Incremental Load / SCD Type 1
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from delta.tables import DeltaTable


# Define paths to the Delta tables
source_path = "/Application/Bronze/source_table"
target_path = "/Application/Silver/target_table"

# Read data from source and target Delta tables
source_df = spark.read.format("delta").load(source_path)
target_table = DeltaTable.forPath(spark, target_path)

# Define merge conditions and updates
merge_condition = "source.id = target.id"

# Perform the merge (upsert) operation
target_table.alias("target") \
    .merge(
        source_df.alias("source"),
        merge_condition
    ) \
    .whenMatchedUpdate(
        condition="source.updated_at > target.updated_at",  # Ensure latest updates
        set={
            "target.value": col("source.value"),
            "target.updated_at": col("source.updated_at")
        }
    ) \
    .whenNotMatchedInsertAll() \
    .execute()
######################################################################
#SCD Type 2:
targetTable = DeltaTable.forPath(spark, "/FileStore/tables/scd2Demo")
targetDF = targetTable.toDF()
sourceDF = spark.createDataFrame(data=data, schema=schema)
joinDF = sourceDF.join(targetDF,
                       (sourceDF.pk1 == targetDF.pk1) &
                       (sourceDF.pk2 == targetDF.pk2) &
                       (targetDF.active_status == "Y"),
                       "leftouter") \
                .select(sourceDF["*"],
                        targetDF.pkl.alias("target_pk1"),
                        targetDF.pk2.alias("target_pk2"),
                        targetDF.diml.alias("target_diml"))

# Filter rows where hash values of dimensions are different
filterDF = joinDF.filter(xxhash64(joinDF.diml) != xxhash64(joinDF.target_diml))

# Create a MERGEKEY column
mergeDF = filterDF.withColumn("MERGEKEY", concat(filterDF.pkl, filterDF.pk2))

# Create dummy records for non-null target records
dummyDF = filterDF.filter(col("target_pk1").isNotNull()).withColumn("MERGEKEY", lit(None))

# Union mergedDF and dummyDF
scdDF = mergeDF.union(dummyDF)

# Merge into the target table
targetTable.alias("target").merge(
    source=scdDF.alias("source"),
    condition="concat(target.pkl, target.pk2) = source.MERGEKEY and target.active_status = 'Y'",
).whenMatchedUpdate(
    set={
        "active_status": "'N'",
        "end_date": "current_date"
    }
).whenNotMatchedInsert(
    values={
        "pk1": "source.pk1",
        "pk2": "source.pk2",
        "diml": "source.diml",
        "active_status": "'Y'",
        "start_date": "current_date",
        "end_date": "to_date('9999-12-31', 'yyyy-MM-dd')"
    }
).execute()

###############################################
# DB Concurrent Read:
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

hdfs_location = "g://Application/raw/table"
df.write.format("parquet") \
    .mode("overwrite") \
    .save(hdfs_location)

# Stop Spark session
spark.stop()

###############################################
#Logger:
from google.cloud import logging as cloud_logging

logging_client = cloud_logging.Client()
logger = logging_client.logger("databricks-data-quality")

try:
    logger.log_text(f"Writing updated data to Silver layer at path: {silver_path}")
    df.write.format("delta").mode("overwrite").option("mergeSchema", "true").save(silver_path)
    logger.log_text("SCD Type 1 pipeline completed successfully")
except Exception as e:
    logger.log_text(f"Error occurred: {str(e)}", severity="ERROR")
    print(f"An error occurred: {e}")

###################################################
#db secrets:
secret_value = dbutils.secrets.get(scope="my_scope", key="my_secret_key")

# NB 1
input_value = dbutils.widgets.get("input_value")
output_value = int(input_value) + 2
def add_numbers(a, b):
    return a + b
dbutils.notebook.exit(str(output_value))

#NB 2
notebook_result = dbutils.notebook.run("/Shared/other_notebook", 60, {"input_value": input_value})
print(notebook_result)
result = add_numbers(3, 5)
print(f"Result of addition: {result}")

###################################################
#Word Count:
df = spark.read.format("text") \
            .load("gs://input.txt")

count_df = df.select(explode(split("value", " ")).alias("word")) \
                .groupBy("word").count().sort("count", ascending=False)
count_df.write.format("csv") \
    .mode("overwrite") \
    .save("gs://output")

count_rdd = df.rdd.flatMap(lambda line: line.split(" "))\
                .map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
count_rdd.saveAsTextFile("gs://output2.txt")

###################################################
#Mislenious:
def is_even(number):
    return number % 2 == 0
is_even_udf = udf(is_even, BooleanType())
df1 = df.withColumn("is_even", is_even_udf(df["number"]))



