spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --name my_pyspark_job \
  --num-executors 4 \
  --executor-memory 4G \
  --executor-cores 2 \
  --driver-memory 2G \
  --conf spark.dynamicAllocation.enabled=true \
  --conf spark.shuffle.service.enabled=true \
  --conf spark.speculation=true \
  --conf spark.executor.memoryOverhead=512M \
  --files hdfs:///path/to/my_config_file.conf \
  --py-files my_dependencies.zip \
  --jars hdfs:///path/to/jar/my_jar_dependency.jar \
  s3a://my-bucket/pyspark_jobs/my_pyspark_job.py \
  --input s3a://my-bucket/input_data/ \
  --output s3a://my-bucket/output_data/


PERMISSIVE(default), DROPMALFORMED, FAILFAST
ERRORIFEXIST(default), ingore, append, overwrite

SQL Order of Execution: from, join, on, where, group by, having, select, distinct, order by, limit

Node size: 16 CPU cores, 64 GB RAM.
Executors per node: 3 executors.
Executor size: 5 CPU cores, 21 GB RAM.

Total capacity depends on the number of nodes N: 16×𝑁 CPU cores, 64×𝑁GB RAM.
Total parallel tasks: 15×𝑁 | 15×N tasks (depending on N).
Parallel tasks with 4 executors: 20 tasks.
Number of tasks for 10.1 GB CSV: 81 tasks.

"Number of stages = number of wide transformation + 1 [N + 1 stages:
1 initial stage: All operations before the first wide transformation.
N stages for N wide transformations: Each shuffle caused by a wide transformation starts a new stage.]"
In narrow transformation, the number of partitions, before and after a transformation remains the same only.
If we have 15 partitions, then it will create a total of 16 tasks, 1 for Driver and 1 for each partitions.
OLAP -> Denormalized. Star and Snowflake Schema
OLTP -> Normalized, None
Caching = Storing Data on-heap [On-heap = This is the memory allocated within the Java Virtual Machine (JVM) heap space.], df.cache() = df.persist(StorageLevel.MEMORY_ONLY)
A stage represents a set of tasks that can be executed together without requiring a shuffle.
Logical units in the worker node which we call executor
Number of jobs = 1, stages = 3, tasks = 16 (2048/128) for 2 wide transformation, 1 action on 2 GB data
orderby or sort and all of the aggregated fucntion does not run in parallel
api does not return multiline json, it only returns single line json and it does not require json flattening
Sudden data volume gain on persist(StorageLevel.MEMORY_ONLY), this will first cache as much as possible and for uncached data, it will recompute
Sort-Merge Join = Two datasets are very large or the dataset is already sorted or high cardinality join keys.
Shuffle-Hash Join = Two moderate-sized datasets, unsorted data, and when you want to avoid the overhead of sorting but cannot broadcast due to memory or data size constraints.
Broadcast Join = One dataset is very big and other one is small
Databricks runtime version = 13.3 LTS, Spark 3.0, Python 3
Before Spark 2.2 there was RBO, after that we have CBO
Spark submit -> driver -> creates lineage graph -> action is called -> lineage to execution plan -> worker nodes -> logical units in the worker node which we call executor (jvm with on-heap memory + cores),  executes the tasks
To remove cache data, we need to use the command unpersist()
"By default, Spark uses hash partitioning Joins: When performing a join operation, Spark will hash the join keys to partition the data across different nodes.
GroupBy: When aggregating data by grouping, Spark uses hash partitioning to ensure that all records with the same key end up in the same partition."
"Range Partitioning: For certain operations, you might want to use range partitioning instead of hash partitioning. Range partitioning can be specified using methods like repartition() or partitionBy() on DataFrames, which allows you to define how data should be split into partitions based on a range of values.
# Example of repartitioning with a specified number of partitions
df_repartitioned = df.repartition(10)
# Example of range partitioning for a specific column
df_partitioned = df.partitionBy('column_name')"
checkpoint always stores the intermediate stage in the disk.
"Parquet (Column Based) [WORM]-> OLAP -> denormalized
AVRO (Row Based) [stores schema in JSON]-> OLTP -> normalized
Snappy (less cpu intensive, hence better in querying) -> splitable file format
Gzip (better compression, hence good for storage) -> non-splitable file format"
"RDD only use on-heap memory but in DF/DS we have freedom to choose on-heap or off-heap memory to minimize the GC.
spark.conf.set(""""spark.memory.offHeap.enabled"""", """"true"""")
spark.conf.set(""""spark.memory.offHeap.size"""", """"2g"""") "
Spark creates a DAG (Directed Acyclic Graph) of stages and tasks. The driver schedules tasks and distributes them across executors. Executors perform the tasks, shuffle data if needed, and return results.
Sure, here’s a detailed overview addressing your questions:

1. **Cluster Configuration for 100 GB of Data:**
   - **Determine Data Size Per Partition:** Check the size of data partitions. Ideally, partitions should be between 128 MB and 1 GB to balance between parallelism and overhead.
   - **Choose Instance Type and Count:** Select instance types based on your workload's requirements. For 100 GB of data, you might start with 4-8 nodes with memory optimized instances (like `r5` or `m5` in AWS). Adjust based on performance testing.
   - **Specify Executor and Core Configurations:** Ensure each executor has sufficient memory to hold its portion of data. For instance, if using `r5.xlarge` instances with 32 GB memory, you might configure 4-8 cores and 4-8 executors per node depending on your job's characteristics.

2. **Submission and Internal Spark Workings:**
   - **Submission:** When you submit a job, Spark sends the job to the cluster manager (like YARN or Kubernetes) which then allocates resources (executors).
   - **Spark Workings:** Spark creates a DAG (Directed Acyclic Graph) of stages and tasks. The driver schedules tasks and distributes them across executors. Executors perform the tasks, shuffle data if needed, and return results.

3. **Driver Memory and Spilling:**
   - **Driver Memory:** This is the memory allocated to the driver process, which handles job scheduling and task coordination.
   - **Spilling to Disk:** Driver memory spills to disk when the driver's memory usage exceeds its allocated memory, particularly for large data structures or when the job's metadata exceeds available memory.

4. **Memory Manager:**
   - **Function:** Spark’s memory manager manages memory allocation for execution (storing RDD partitions) and storage (caching and shuffling).
   - **Components:** It includes Unified Memory Management (for combining execution and storage) and manages memory using spillable structures to disk to prevent out-of-memory errors.

5. **Out of Memory (OOM) Exceptions:**
   - **Driver Node:** OOM occurs if the driver tries to hold too much data or perform large operations in memory (e.g., large collect operations).
   - **Executor Node:** OOM occurs when an executor runs out of memory due to handling large partitions, insufficient memory allocation, or excessive shuffling.

6. **Executor Memory:**
   - **Definition:** Executor memory is allocated to each executor for task execution and storage.
   - **Distribution:** It is divided between storage (for caching) and execution (for processing tasks).
   - **Spilling to Disk:** Executors spill data to disk when the in-memory storage or execution data exceeds the available memory.

7. **Pools in Databricks:**
   - **Definition:** Pools are a set of idle, reusable virtual machines that can be used to provision clusters faster and reduce cluster start times.
   - **Use:** Pools help manage cluster resources efficiently and reduce the cost of frequently created clusters.
   - **Creation:** Pools can be created in the Databricks workspace UI under the "Pools" section by specifying the pool name, instance types, and size.

8. **Workloads on Standard Clusters:**
   - **Types:** Standard clusters can handle a range of workloads including ETL jobs, data exploration, data analysis, and model training. They are typically used for batch processing and general-purpose jobs.

9. **Types of Clusters and Choosing the Right One:**
   - **Types:** Databricks offers Standard, High-Concurrency, and Single Node clusters. Standard is for general use, High-Concurrency is optimized for concurrent workloads, and Single Node is for debugging.
   - **Choosing:** Select based on workload type. For interactive queries or many concurrent users, High-Concurrency is ideal. For general batch processing, Standard clusters work well.

10. **Cluster Modes:**
    - **Modes:** Databricks clusters operate in Standard, High-Concurrency, and Single Node modes.
    - **Purpose:** Standard for general-purpose workloads, High-Concurrency for concurrent query execution, and Single Node for local development and debugging.

11. **Databricks Runtimes:**
    - **Types:** Databricks Runtimes include the standard runtime, the ML runtime (optimized for machine learning), and the Photon runtime (optimized for performance). Each runtime is tailored for different types of workloads.

12. **Calling One Notebook from Another:**
    - **Method:** Use `%run /path/to/other/notebook` to execute another notebook’s code in the current notebook. This imports variables and functions from the other notebook.

13. **Accessing Variables from Another Notebook:**
    - **Method:** Use `%run /path/to/other/notebook` to access variables and functions defined in the other notebook.

14. **Exiting a Notebook and Returning Output Data:**
    - **Method:** Use `dbutils.notebook.exit()` to return output data from a notebook, which can then be accessed by the calling notebook.

15. **Creating Internal and External Tables:**
    - **Internal Tables:** Created using SQL `CREATE TABLE ...` command without specifying external storage. The table data is managed within the Databricks workspace.
    - **External Tables:** Created using SQL `CREATE TABLE ... USING ... LOCATION ...` command, where you specify an external location (e.g., S3 bucket or ADLS) where data is stored.

Here are one-liner definitions for each of the terms you've requested:

### 1. Data Warehouse vs. Data Lake vs. Data Mart
- **Data Warehouse**: A centralized repository optimized for storing and querying structured data from various sources for business intelligence and reporting.
- **Data Lake**: A storage system designed to hold vast amounts of raw data in its native format, supporting structured, semi-structured, and unstructured data for various analytics workloads.
- **Data Mart**: A subset of a data warehouse tailored to meet the needs of a specific department or business line, often optimized for quick querying and reporting.

### 2. Fact Table
- **Fact Table**: A central table in a star or snowflake schema that stores quantitative data (facts) for analysis and is linked to dimension tables.

### 3. Dimension Table
- **Dimension Table**: A table in a star or snowflake schema that stores attributes (dimensions) related to the data in a fact table, providing context for analysis.

### 4. Star Schema
- **Star Schema**: A database schema design that organizes data into fact and dimension tables, with the fact table at the center and dimension tables radiating outward like a star.

### 5. Snowflake Schema
- **Snowflake Schema**: A normalized form of star schema where dimension tables are further divided into related tables, reducing redundancy and optimizing storage.

### 6. Factless Fact Table
- **Factless Fact Table**: A fact table that captures events without any associated quantitative data, typically used to track occurrences or events.

### 7. Master Table
- **Master Table**: A table that holds a primary set of data about entities such as customers, products, or employees, serving as a reference point in a database.

### 8. Transaction Table
- **Transaction Table**: A table that records business transactions and events, often containing timestamped entries with detailed transaction data.

### 9. SCD Type 1
- **SCD Type 1**: A Slowly Changing Dimension method where old data is overwritten with new data, preserving only the current state without maintaining historical data.

### 10. SCD Type 2
- **SCD Type 2**: A Slowly Changing Dimension method that maintains historical data by adding new records for changes, allowing for the tracking of changes over time.

### 11. Databricks Catalog
- **Databricks Catalog**: A unified metadata store in Databricks that enables data discovery, governance, and management across different data assets like tables, files, and machine learning models.

### 12. Map vs. FlatMap
- **Map**: A transformation in Spark that applies a function to each element of an RDD, DataFrame, or Dataset, returning a new RDD with the same number of elements.
- **FlatMap**: A transformation in Spark that applies a function to each element of an RDD, DataFrame, or Dataset, and flattens the results, returning a new RDD with potentially more or fewer elements than the input.

### 13. How to Handle Data Loss
- **How to Handle Data Loss**: Implement backup and recovery strategies, use fault-tolerant storage systems, and employ data replication and redundancy techniques to prevent and recover from data loss.

### 14. How to Handle Initial and Incremental Load
- **How to Handle Initial and Incremental Load**: Use initial full data loads to populate databases or data lakes and incremental loads to regularly update or append new and changed data efficiently.

### 15. Delta Table vs. Parquet Table
- **Delta Table**: A versioned and ACID-compliant storage format based on Parquet that supports efficient data updates, deletes, upserts, and time travel capabilities.
- **Parquet Table**: A columnar storage format optimized for read-heavy analytics workloads, offering efficient compression and encoding, but lacking native support for ACID transactions or time travel.