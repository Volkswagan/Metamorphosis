### Comparison:

| Feature          | VACUUM                     | OPTIMIZE                          | Z-ORDER                            |
|------------------|----------------------------|-----------------------------------|------------------------------------|
| **Purpose**      | Garbage collection, frees up storage by deleting old data files | File compaction, reduces the number of small files | Data clustering to improve query performance on specific columns |
| **Key Benefit**  | Reduces storage usage and improves metadata management | Improves query performance by reducing file I/O overhead | Improves query performance for range-based queries by clustering similar data together |
| **How It Works** | Deletes files that are older than the specified retention period | Combines small files into larger ones for better query performance | Reorganizes data within files based on the values of specific columns |
| **Use Case**     | Clean up old files and reduce storage costs after data updates | Improve query performance by reducing the number of files scanned | Optimize for range queries and filtering on specific columns |
| **Example**      | `VACUUM delta_table RETAIN 168 HOURS;` | `OPTIMIZE delta_table;`           | `OPTIMIZE delta_table ZORDER BY (column1);` |
| **Limitations**  | Time travel for older versions is lost; must be used cautiously | Resource-intensive for large tables; doesn’t cluster data | Resource-intensive; only benefits queries filtering on the specified columns |

---

- **Use VACUUM**:
  - When you want to clean up old files and free up storage after updates, deletes, or merges.
  - When storage costs or managing old data becomes problematic.

- **Use OPTIMIZE**:
  - When your Delta table has accumulated too many small files due to frequent inserts or updates.
  - To improve the performance of queries by reducing the number of files scanned.

- **Use Z-ORDER**:
  - When you frequently run range-based queries or queries that filter on specific columns.
  - To improve query performance on tables with large datasets by organizing data more efficiently based on commonly queried columns.

### Conclusion:
- **VACUUM** helps manage storage by removing old, unused files.
- **OPTIMIZE** improves query performance by reducing file counts, improving data compaction.
- **Z-ORDER** enhances query performance by clustering data based on specific columns, especially for range queries or filters.

---

#### Example: Normal Partitioning     
```sql
CREATE TABLE transactions
USING DELTA
PARTITIONED BY (year)
AS SELECT * FROM original_data;
```

#### Example: Liquid Clustering 
There’s no need to specify partitioning. Instead, after data insertion, you can run:
```sql
OPTIMIZE delta_table
ZORDER BY (PK Column)
```

### Comparison:

| Feature                         | Normal Partitioning                           | Liquid Clustering                      |
|----------------------------------|-----------------------------------------------|----------------------------------------|
| **Data Organization**            | Static partitions based on specific columns   | Dynamic and adaptive clustering        |
| **Performance Benefit**          | Improves query performance by partition pruning when filtering on partition columns | Improves query performance dynamically based on query patterns |
| **Flexibility**                  | Must predefine partitions and can’t change easily | Automatically adapts to query patterns without static partition boundaries |
| **Handling Skew**                | Can suffer from skew if partition values are imbalanced | Automatically adjusts for better balance |
| **Write Overhead**               | High write overhead when partitions get imbalanced or hot | Lower write overhead, as clustering adapts dynamically |
| **Partitioning Size Management** | Over-partitioning (many small files) or under-partitioning (few large files) can degrade performance | Automatically manages file sizes and layouts |
| **Maintenance**                  | Manual maintenance needed to manage partition skew and performance over time | Self-healing and maintenance-free as it dynamically optimizes data |
| **Z-ordering**                   | Must be applied separately (manual optimization step) | Often used in conjunction with Z-ordering for automatic optimization |
| **Use Cases**                    | Best when data is naturally partitioned (e.g., date, region) and queries frequently filter on those columns | Best for complex queries with dynamic filtering needs across multiple columns |

---

###REORDER:
```sql
ALTER TABLE table_name CHANGE COLUMN col35 FIRST
ALTER TABLE table_name CHANGE COLUMN col35 AFTER col10
```


Databricks Security Features:
Column Level Encryption
RBAC
Audit Logging
MFA

Spark Cache is in-memory persist
DBIO/DISK Cache/Delta cache is in disk persist

only take required partitons from the remote and place it in disk + efficient decompression + optimal data format = delta cache
spark.conf.set("spark.databricks.io.cache.enabled", "true")
```sql
CACHE SELECT * FROM delta_table
```


OPTIMIZE = Combine small files and create a new big and create a latest json file with latest details but nothing gets deleted.
VACCUM = default retain time is 168 HOURS or 7 Days, 
spark.conf.set("spark.databricks.delta.retentionDurationCheck.enabled", "False")

Delta Lake = parquet + json logs

Use Parquet Files when you need a highly efficient columnar storage format for read-heavy analytics and can manage without transactional guarantees or versioning.
Use Delta Lake when you need ACID compliance, concurrent writing, time-travel, and the ability to handle both batch and streaming data in a unified, scalable data pipeline. Delta Lake builds on top of Parquet, adding these advanced features and making it ideal for more dynamic and complex environments.


Spark Backend:
When we submit a Spark job using the spark-submit command, specifying YARN as ResourceManager receives the job request and allocates resources (containers) to the Spark application.
YARN launches a Spark ApplicationMaster (AM) in a container, which is responsible for managing the Spark job.
The Spark ApplicationMaster requests resources (containers) from the ResourceManager based on the job's requirements.
The ApplicationMaster starts Spark executors in containers on different nodes in the cluster.
The Spark Driver converts the job into a Directed Acyclic Graph (DAG) of stages and tasks.
The Driver schedules tasks and sends them to the executors.
Executors execute the tasks and process the data. They shuffle data between tasks if necessary.
Executors perform the data transformations and actions as defined in your Spark job.
Intermediate data might be stored in memory (for faster access) or on disk if necessary.
After all tasks are completed, the results are collected by the Driver.
The ApplicationMaster deallocates resources and shuts down the executors.

Modes:
Client Mode: The Spark Driver runs on the machine where you submit the job (e.g., your laptop or a gateway node). The driver communicates with the cluster's executors remotely and the executors run on the cluster.
Cluster Mode: The Spark Driver runs inside the cluster, typically on one of the cluster's worker nodes. Submitting a job to the cluster, and both the driver and executors run on the cluster's nodes.

Coalesce vs Repartiton:
coalesce is better than repartition while decreasing the number of partitions because it does not involve a full shuffle of data across nodes. It just merges existing partitions.


Partitioning vs Bucketing in Hive:
1. Partitioning:
Splits data into subdirectories based on column values.
Speeds up query execution by scanning only relevant partitions.
Use when querying based on discrete column values (e.g., dates, countries).

Queries filter frequently on specific columns (e.g., date ranges).
Reducing scan time is critical.
low cardinality

2. Bucketing:
Divides data into fixed-size buckets (files) based on a hash of the column value.
Helps with efficient joins by aligning the same bucketed data across tables.
Use when partitioning isn’t feasible or when you need uniform file sizes.

Joins need to be optimized across large datasets.
You want to avoid too many small partitions (too many small files).
high cardinality


CREATE TABLE sales_part_bucketed (product_id INT, sale_amount DECIMAL(10, 2)) PARTITIONED BY (sale_date STRING) CLUSTERED BY (product_id) INTO 10 BUCKETS STORED AS PARQUET; -- Load data into the table with both partitioning and bucketing LOAD DATA INPATH '/data/sales_data' INTO TABLE sales_part_bucketed PARTITION (sale_date='2024-09-19');

df.write.partitionBy('sale_date').bucketBy(10, 'product_id').sortBy('product_id').format('parquet').mode('overwrite')
.save('/path/to/output/directory')

Partitioning comes first because it is the most granular way to prune data. The engine can ignore entire folders (partitions) that do not match the query, significantly reducing the amount of data read. Bucketing comes second because it operates within each partition. Use both to avoid too many small partitions (over-partitioning) and too few large partitions (under-partitioning), ensuring even distribution of data within partitions.






1. PERMISSIVE(default), DROPMALFORMED, FAILFAST ERRORIFEXIST(default), ingore, append, overwrite

2. SQL Order of Execution: from, join, on, where, group by, having, select, distinct, order by, limit

Node size: 16 CPU cores, 64 GB RAM. Executors per node: 3 executors. Executor size: 5 CPU cores, 21 GB RAM.

Total capacity depends on the number of nodes N: 16xN
CPU cores, 64×𝑁GB RAM. Total parallel tasks: 15×𝑁 | 15×N tasks (depending on N). Parallel tasks with 4 executors: 20 tasks. Number of tasks for 10.1 GB CSV: 81 tasks.

Spark Submit Command:
$SPARK_HOME/bin/spark-submit \
    --master yarn \
    --deploy-mode cluster \
    --num-executors 10 \          # Number of executors to use
    --executor-memory 4G \       # Memory allocated per executor
    --executor-cores 2 \          # Number of cores per executor
    --driver-memory 2G \          # Memory allocated for the driver
    --conf spark.sql.shuffle.partitions=200 \ # Configuration for shuffle partitions
    --jars /path/to/extra.jar \    # Path to any extra JARs needed (optional)
    --py-files /path/to/other_dependencies.zip \ # Paths to additional Python files or dependencies
    /path/to/your_script.py \      # Path to your main PySpark script   
    $input_path $output_path $edl_eff_dt

1. Data Warehouse vs. Data Lake vs. Data Mart
Data Warehouse: A centralized repository optimized for storing and querying structured data from various sources for business intelligence and reporting.
Data Lake: A storage system designed to hold vast amounts of raw data in its native format, supporting structured, semi-structured, and unstructured data for various analytics workloads.
Data Mart: A subset of a data warehouse tailored to meet the needs of a specific department or business line, often optimized for quick querying and reporting.

2. Fact Table
Fact Table: A central table in a star or snowflake schema that stores quantitative data (facts) for analysis and is linked to dimension tables.

3. Dimension Table
Dimension Table: A table in a star or snowflake schema that stores attributes (dimensions) related to the data in a fact table, providing context for analysis.

4. Star Schema
Star Schema: A database schema design that organizes data into fact and dimension tables, with the fact table at the center and dimension tables radiating outward like a star.

5. Snowflake Schema
Snowflake Schema: A normalized form of star schema where dimension tables are further divided into related tables, reducing redundancy and optimizing storage.

6. Factless Fact Table
Factless Fact Table: A fact table that captures events without any associated quantitative data, typically used to track occurrences or events.

7. Master Table
Master Table: A table that holds a primary set of data about entities such as customers, products, or employees, serving as a reference point in a database.

8. Transaction Table
Transaction Table: A table that records business transactions and events, often containing timestamped entries with detailed transaction data.
9. SCD Type 1
SCD Type 1: A Slowly Changing Dimension method where old data is overwritten with new data, preserving only the current state without maintaining historical data.

10. SCD Type 2
SCD Type 2: A Slowly Changing Dimension method that maintains historical data by adding new records for changes, allowing for the tracking of changes over time.

11. Databricks Catalog
Databricks Catalog: A unified metadata store in Databricks that enables data discovery, governance, and management across different data assets like tables, files, and machine learning models.

12. Map vs. FlatMap
Map: A transformation in Spark that applies a function to each element of an RDD, DataFrame, or Dataset, returning a new RDD with the same number of elements.
FlatMap: A transformation in Spark that applies a function to each element of an RDD, DataFrame, or Dataset, and flattens the results, returning a new RDD with potentially more or fewer elements than the input.

13. How to Handle Data Loss
How to Handle Data Loss: Implement backup and recovery strategies, use fault-tolerant storage systems, and employ data replication and redundancy techniques to prevent and recover from data loss.

14. How to Handle Initial and Incremental Load
How to Handle Initial and Incremental Load: Use initial full data loads to populate databases or data lakes and incremental loads to regularly update or append new and changed data efficiently.

15. Delta Table vs. Parquet Table
Delta Table: A versioned and ACID-compliant storage format based on Parquet that supports efficient data updates, deletes, upserts, and time travel capabilities.
Parquet Table: A columnar storage format optimized for read-heavy analytics workloads, offering efficient compression and encoding, but lacking native support for ACID transactions or time travel.
