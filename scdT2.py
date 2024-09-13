from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat, lit, xxhash64
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from delta.tables import DeltaTable

# Create a Spark session
spark = SparkSession.builder.appName("CDC_SCD_Type2").getOrCreate()

# Load your source and target DataFrames (sourceDF and targetDF)
targetTable = DeltaTable.forPath(spark, "/FileStore/tables/scd2Demo")
targetDF = targetTable.toDF()

# Define the schema for sourceDF
schema = StructType([
    StructField("pk1", StringType(), True),
    StructField("pk2", StringType(), True),
    StructField("diml", IntegerType(), True),
    StructField("dim2", IntegerType(), True),
    StructField("dim3", IntegerType(), True),
    StructField("dim4", IntegerType(), True)
])

# Create sample data for sourceDF
data = [
    (111, 'Unitl', 200, 500, 800, 400),
    (222, "Unit2", 800, 1300, 800, 500),
    (444, "Unit4", 100, None, 700, 300)
]
sourceDF = spark.createDataFrame(data=data, schema=schema)

# Join sourceDF and targetDF
joinDF = sourceDF.join(targetDF,
                       (sourceDF.pk1 == targetDF.pk1) &
                       (sourceDF.pk2 == targetDF.pk2) &
                       (targetDF.active_status == "Y"),
                       "leftouter") \
    .select(sourceDF["*"],
            targetDF.pkl.alias("target_pk1"),
            targetDF.pk2.alias("target_pk2"),
            targetDF.diml.alias("target_diml"),
            targetDF.dim2.alias("target_dim2"),
            targetDF.dim3.alias("target_dim3"),
            targetDF.dim4.alias("target_dim4"))

# Filter rows where hash values of dimensions are different
filterDF = joinDF.filter(xxhash64(joinDF.diml, joinDF.dim2, joinDF.dim3, joinDF.dim4) !=
                         xxhash64(joinDF.target_diml, joinDF.target_dim2, joinDF.target_dim3, joinDF.target_dim4))

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
        "dim2": "source.dim2",
        "dim3": "source.dim3",
        "dim4": "source.dim4",
        "active_status": "'Y'",
        "start_date": "current_date",
        "end_date": "to_date('9999-12-31', 'yyyy-MM-dd')"
    }
).execute()

# Stop the Spark session
spark.stop()
