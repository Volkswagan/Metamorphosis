# Databricks notebook source
# Replace these variables with your own values
gcs_bucket_name = "<your-gcs-bucket-name>"
mount_name = "/mnt/<your-mount-name>"
secret_scope = "gcs-secrets"
secret_key = "gcp-service-account-key"

# Fetch the service account key from Databricks secrets
service_account_key = dbutils.secrets.get(scope=secret_scope, key=secret_key)

# Mount the GCS bucket
dbutils.fs.mount(
  source = f"gs://{gcs_bucket_name}",
  mount_point = mount_name,
  extra_configs = {
    "google.cloud.auth.service.account.json.keyfile": service_account_key
  }
)


# COMMAND ----------

"""
Steps to Implement the Solution:
1. Create a Databricks Access Token: You will need an access token to authenticate API requests to Databricks.
2. Set Up a Cloud Function: Write a Cloud Function in Python that gets triggered by a GCS event (e.g., file creation).
3. Call Databricks API from the Cloud Function: Use the Cloud Function to make an API request to Databricks to run a specific notebook.
-------------------------------------------------------------------------------------------------------------------
import requests
import base64
from google.cloud import storage

def trigger_databricks_notebook(data, context):
    # Define Databricks API parameters
    DATABRICKS_INSTANCE = "https://<your-databricks-instance>"
    DATABRICKS_TOKEN = "<your-databricks-token>"
    JOB_ID = "<your-databricks-job-id>"

    # Extract information about the uploaded file from the event data
    bucket_name = data['bucket']
    file_name = data['name']

    print(f"File {file_name} uploaded to {bucket_name}")

    # Make API request to trigger Databricks notebook job
    url = f"{DATABRICKS_INSTANCE}/api/2.1/jobs/run-now"

    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "job_id": JOB_ID,
        "notebook_params": {
            "bucket_name": bucket_name,
            "file_name": file_name
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Databricks notebook triggered successfully.")
    else:
        print(f"Failed to trigger Databricks notebook. Response: {response.text}")
-------------------------------------------------------------------------------------------------------
import base64
import json
import requests
from google.cloud import logging
from google.cloud import secretmanager

# Initialize Cloud Logging client
logging_client = logging.Client()
logger = logging_client.logger("databricks-trigger-logs")

# Function to trigger Databricks job
def trigger_databricks_job(event, context):
    try:
        # Access secrets from Secret Manager
        secret_manager_client = secretmanager.SecretManagerServiceClient()
        databricks_token_secret = secret_manager_client.access_secret_version(
            request={"name": "projects/YOUR_PROJECT_ID/secrets/DATABRICKS_TOKEN/versions/latest"}
        )
        databricks_token = databricks_token_secret.payload.data.decode("UTF-8")

        databricks_instance = "https://<your-databricks-instance>"
        job_id = "<your-databricks-job-id>"
        
        # Define API URL and headers
        url = f"{databricks_instance}/api/2.1/jobs/run-now"
        headers = {
            "Authorization": f"Bearer {databricks_token}",
            "Content-Type": "application/json"
        }

        # Define payload with dynamic parameters if needed
        payload = {
            "job_id": job_id,
            "notebook_params": {
                "run_date": "2024-09-01"  # Example dynamic parameter
            }
        }

        # Send API request to start the job
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            logger.log_text("Databricks job triggered successfully.")
        else:
            logger.log_text(f"Failed to trigger Databricks job: {response.text}", severity="ERROR")
            raise Exception(f"Databricks job trigger failed with status code {response.status_code}")

    except Exception as e:
        logger.log_text(f"Error in Cloud Function: {str(e)}", severity="ERROR")
        notify_failure_via_email(str(e))  # Example function to send an email on failure

def notify_failure_via_email(error_message):
    # Use another Cloud Function or any email service to notify on failure
    pass
"""

# COMMAND ----------

from pyspark.sql.functions import col
from delta.tables import DeltaTable

# Load new data
last_run_time = ... # Retrieve last run timestamp
df_incremental = spark.read.format("source_format").load("source_path").filter(col("timestamp") > last_run_time)

# Transform data
transformed_df = df_incremental.withColumn("new_column", ...)

# Upsert data into Delta table
delta_table = DeltaTable.forPath(spark, "delta_table_path")
delta_table.alias("t").merge(
    transformed_df.alias("s"),
    "t.id = s.id"
).whenMatchedUpdate(
    set={
        "column1": "s.column1",
        "column2": "s.column2"
    }
).whenNotMatchedInsertAll().execute()

# Update last processed time
new_last_run_time = df_incremental.agg({"timestamp": "max"}).collect()[0][0]
# Save new_last_run_time to metadata store or table


# COMMAND ----------

DeltaTable.createIfNotExists(spark) \
    .tableName("table_wise_emp") \
    .addColumns(schema) \
    .location(path) \
    .execute()

df.write.option("mergeSchema", "true").format("delta").mode("append").save(path)

rdf = spark.read.format("delta") \
        .option("timestampAsOf", "2024-07-27T19:37:11.000+00:00") \
        .option("versionAsOf", 1) \
        .load(path)
rdf.show()

delta_instance = DeltaTable.forPath(spark, path)
delta_instance.delete((col("employee_id") == 4) & (col("age") == 28))

delta_instance.update(
    condition=(col("employee_id") == 5) & (col("first_name") == "Mike"),
    set={"department": "'New_Finance'"}
)

delta_instance.restoreToTimestamp("2024-07-27T19:37:05.000+00:00")
delta_instance.restoreToVersion(1)

rdf = delta_instance.toDF()
rdf.show()

# COMMAND ----------

#SCD Type 1
delta_instance = DeltaTable.forPath(spark, delta_path)

delta_instance.alias("target").merge(
    updates_df.alias("source"),
    "target.employee_id = source.employee_id"
).whenMatchedUpdate(set={
    "department": col("source.department"),
    "updated_at": current_timestamp()
}).whenNotMatchedInsert(values={
    "employee_id": col("source.employee_id"),
    "department": col("source.department"),
    "created_at": current_timestamp(),
    "updated_at": current_timestamp()
}).execute()

rdf = delta_instance.toDF()
rdf.show()


# COMMAND ----------

#SCD Type 2
joinedDF = sourceDF.join(targetDF, (sourceDF.pk1 == targetDF.pk1) & (sourceDF.pk2 == targetDF.pk2) & (targetDF.active_status == 'Y'), "left") \
    .select(sourceDF["*"], targetDF.pk1.alias("target_pk1"), targetDF.pk2.alias("target_pk2"), targetDF.dim1.alias("target_dim1"))
filterDF = joinedDF.filter(xxhash64(joinedDF.dim1) != xxhash64(joinedDF.target_dim1))
mergeDF = filterDF.withColumn("MERGEKEY", concat(filterDF.pk1, filterDF.pk2))
dummyDF = filterDF.filter("target_pk1 is not null").withColumn("MERGEKEY", lit(None))
scdDF = mergeDF.union(dummyDF)
targetTable.alias("target").merge(
    source = scdDF.alias("source"),
    condition = "concat(target.pk1, target.pk2) = source.MERGEKEY and target.active_status = 'Y'"
).whenMatchedUpdate(
    set = {
        "active_status" : "'N'",
        "end_date" : current_date()
    }
).whenNotMatchedInsert(
    values = {
        "pk1" : "source.pk1",
        "pk2" : "source.pk2",
        "dim1" : "source.dim1",
        "active_status" : "'Y'",
        "start_date" : current_date(),
        "end_date" : "to_date('9999-12-31', 'yyyy-MM-dd')"
    }
).execute()
resultDF = targetTable.toDF()
resultDF.show(truncate=False)

# COMMAND ----------

ALTER TABLE silver_table SET TBLPROPERTIES (delta.enableChangeDataFeed = true)

changes_df = spark.read.format("delta").option("readChangeData", True).option("startingVersion", 2).table("silver_table")

changes_df.show()

# COMMAND ----------


window_spec = Window.partitionBy("Country", "Product").orderBy(col("_commit_version").desc())
df_latest_version = spark.read.format("delta").option("versionAsOf", 5).table("silver_table")\
                            .filter(col("_change_type") != 'update_preimage') \
                            .withColumn("rank", rank().over(window_spec))\
                            .filter(col("rank") == 1)
df_latest_version.show()
# Create or replace a temporary view with the latest version of the data
df_latest_version.createOrReplaceTempView("silver_Table_latest_version")


df_gold = spark.read.format("delta").load(gold_table_path)
df_silver_latest = spark.table("silver_Table_latest_version")

# Define a DataFrame for updates
df_updates = df_silver_latest.filter(col("_change_type") == "update_postimage") \
            .join(df_gold, ["Country", "Product"], "inner") \
            .select(df_silver_latest["Country"], df_silver_latest["Product"], 
            (df_silver_latest["Sales"] / df_silver_latest["Stock"]).alias("SalesRate"))

df_deletes = df_silver_latest.filter(col("_change_type") == "delete") \
    .join(df_gold, ["Country", "Product"], "inner")

df_inserts = df_silver_latest.filter(col("_change_type").isNull() | (col("_change_type") == "insert")) \
    .select("Country", "Product", (col("Sales") / col("Stock")).alias("SalesRate"))

df_gold.alias("target").merge(
    df_updates.alias("source"),
    "target.Country = source.Country AND target.Product = source.Product"
).whenMatchedUpdate(set={
    "SalesRate": col("source.SalesRate")
}).execute()


df_gold.alias("target").join(
    df_deletes.alias("source"),
    ["Country", "Product"],
    "left_anti"
).write.format("delta").mode("overwrite").save(gold_table_path)

df_inserts.write.format("delta").mode("append").save(gold_table_path)

# Optionally: Verify the results
df_gold.show()

