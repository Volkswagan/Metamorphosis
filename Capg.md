### **External Tables vs Internal Tables in Hive**
- **Internal Tables**:
  - Managed by Hive, data is stored in the Hive warehouse.
  - When the table is dropped, the data is also deleted from the filesystem.
  - Use case: When Hive is responsible for both data and metadata.
- **External Tables**:
  - Hive only manages metadata; data is stored externally (outside Hive warehouse).
  - Dropping the table does not delete the data.
  - Use case: When data is shared with other tools or systems, or managed outside Hive.

---

### **Join Strategies in Hive**
1. **Map Join (Broadcast Join)**:
   - Smaller table is broadcasted to all nodes.
   - Faster for joins with small tables.
   - Use when one table is significantly smaller.
2. **Shuffle Join (Common Join)**:
   - Data is shuffled between nodes.
   - Used for large table joins.
   - Can be slower due to network shuffling.
3. **Sort-Merge Join**:
   - Sorts data before performing the join.
   - Efficient for large, pre-sorted datasets.
   - Use when both tables are large and can be sorted on join keys.

---

### **Partitioning vs Bucketing in Hive**
- **Partitioning**:
  - Splits data into subdirectories based on column values.
  - Speeds up query execution by scanning only relevant partitions.
  - Use when querying based on discrete column values (e.g., dates, countries).
- **Bucketing**:
  - Divides data into fixed-size buckets (files) based on a hash of the column value.
  - Helps with efficient joins by aligning the same bucketed data across tables.
  - Use when partitioning isn’t feasible or when you need uniform file sizes.

---

### **When to Use Partitioning vs Bucketing**
- **Use Partitioning** when:
  - Queries filter frequently on specific columns (e.g., date ranges).
  - Reducing scan time is critical.
  - low cardinality
- **Use Bucketing** when:
  - Joins need to be optimized across large datasets.
  - You want to avoid too many small partitions (too many small files).
  - high cardinality
    
CREATE TABLE sales_part_bucketed (product_id INT, sale_amount DECIMAL(10, 2)) 
PARTITIONED BY (sale_date STRING) CLUSTERED BY (product_id) INTO 10 BUCKETS
STORED AS PARQUET;
-- Load data into the table with both partitioning and bucketing
LOAD DATA INPATH '/data/sales_data' INTO TABLE sales_part_bucketed PARTITION (sale_date='2024-09-19');

df.write.partitionBy('sale_date').bucketBy(10, 'product_id').sortBy('product_id').format('parquet').mode('overwrite') \
    	.save('/path/to/output/directory')

  1. Partitioning comes first because it is the most granular way to prune data. The engine can ignore entire folders (partitions) that do not match the query, significantly reducing the amount of data read. Bucketing comes second because it operates within each partition. Use both to avoid too many small partitions (over-partitioning) and too few large partitions (under-partitioning), ensuring even distribution of data within partitions.
  2. 

---

### **Simple Optimization Techniques in Hive**
1. **Use Partition Pruning**:
   - Query only the relevant partitions to avoid full table scans.
2. **Enable Compression**:
   - Use efficient formats (e.g., Parquet or ORC) with compression to reduce storage and IO costs.
3. **Use Map Join**:
   - Enable **`hive.auto.convert.join=true`** to automatically use Map Join for small tables.
4. **Avoid Small Files**:
   - Combine small files using **`hive.merge.mapfiles`** and **`hive.merge.smallfiles.avgsize`** to reduce the number of files processed.
5. **Use Bucketing for Joins**:
   - When joining large tables, bucket them on the same column to reduce shuffle.
6. **Optimize Table Format**:
   - Use ORC or Parquet for columnar storage and better performance with large datasets.
7. **Fact about hive**:
	- Hive does not enforce data integrity constraints like primary keys, foreign keys, or unique constraints. It relies on external tools or applications to ensure data integrity.

---
```sql
CREATE DATABASE IF NOT EXISTS my_database
COMMENT 'This is my new database'
LOCATION 'hdfs://cluster-dev/user/hive/warehouse/my_database'
WITH DBPROPERTIES ('creator'='souvik', 'created_date'='2024-09-18');

CREATE EXTERNAL TABLE pnd.pnd_user_info (
  user_id decimal(15,0),
  info varchar(100),
  edl_1st_upd_ts timestamp
)
PARTITIONED BY (edl_eff_dt int)
STORED AS PARQUET
LOCATION 'hdfs://cluster-dev/bsn/data/pnd/pnd_user_info';

alter table tab add columns(col4 string, col5 int);
alter table tab change column col1 col1 int after col3;
alter table tab change column col2 new_col2 string;
alter table tab rename to tab1;
alter table tab1 replace columns(id int, name string);
alter table tab1 set tblproperties('auto.purge'='true');
alter table tab1 set fileformat avro;

from emp_tab 
insert into table developer_tab 
select col1,col2 where col2 ='Developer' 
insert into table manager_tab 
select col1,col2 where col2='Mgr';

--ACID Tables: 1. Internal 2. ORC 3. Bucketed 4. Transaction = true

--Set hive.txn.manager = org.apache.hadoop.hive.ql.lockmgr.DbTxnManager
--Set hive.support.concurrency = true
-- Set hive.enforce.bucketing = true
--Set hive.exec.dynamic.partition.mode = nonstrict
--Enable hive.support.concurrency
==Enable hive.enforce.bucketing properties.

CREATE TABLE database_name.table_name (
    column1 STRING,
    column2 INT
)
CLUSTERED BY (column2) INTO 5 BUCKETS
STORED AS ORC
TBLPROPERTIES (
    'transactional'='true',
    'transactional_properties'='insert_only' -- Optional, 'insert_only' allows only inserts
);

--not this
DELETE FROM sales_data
WHERE acc_creation_year < '2023-01-01'
--do this
ALTER TABLE sales_data DROP PARTITION (acc_creation_year=2022);

```
---
SFTP (CSV) -> RAW (parquet) -> DATA (parquet) -> ANALYTICAL ()
1. Parquet handles nested data structures (e.g., arrays, maps) better than ORC in most analytical queries, which is common in analytics workloads.
2. Parquet often achieves better compression ratios for specific types of data, particularly with numeric-heavy data.
3. Parquet tends to perform better in read-heavy analytical queries where the goal is to scan, aggregate, or filter large datasets across multiple columns.
4. Parquet (Column Based) [WORM]-> OLAP -> denormalized
5. AVRO (Row Based) [stores schema in JSON]-> OLTP -> normalized
6. Snappy (less cpu intensive, hence better in querying)
7. Gzip (better compression, hence good for storage, but cpu intensive) 
---
1. checkpoint always stores the intermediate stage in the disk.
2. RDD only use on-heap memory but in DF/DS we have freedom to choose on-heap or off-heap memory to minimize the GC.
    spark.conf.set(""""spark.memory.offHeap.enabled"""", """"true"""")
    spark.conf.set(""""spark.memory.offHeap.size"""", """"2g"""")
---

```python
# job.py
from pyspark.sql import SparkSession
import sys

def etl(input_path, output_path, edl_eff_dt):
  spark = SparkSession.builder.appName("MyJOb").getOrCreate()
  input_df = spark.read.option("header", True).csv(input_path)
  transformed_df = input_df.filter(col("some_column").isNotNull())
  transformed_df = transformed_df.withColumn("edl_eff_dt", lit(edl_eff_dt))
  transformed_df.write.mode("overwrite").partitionBy("edl_eff_dt").format("parquet").save(output_path)
spark.stop()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: spark-submit job.py <input_path> <output_path> <edl_eff_dt>")
        sys.exit(-1)
    input_path = sys.argv[1]  # HDFS raw layer input file path
    output_path = sys.argv[2]  # HDFS data layer output path
    edl_eff_dt = sys.argv[3]  # Effective date in yyyymmdd format
    etl(input_path, output_path, edl_eff_dt)
```

```bash
#!/bin/bash

# Usage function to provide help when needed
usage() {
  echo "Usage: $0 edl_eff_dt"
  exit 1
}

# Check if the correct number of arguments are provided
if [ "$#" -ne 3 ]; then
    usage
fi

# Assign input arguments to variables
from_date=$1
to_date=$2

# Path to the Spark home directory
SPARK_HOME="/path/to/spark"

# Spark submit command to run the PySpark job
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

# Check if the Spark job was successful
if [ $? -eq 0 ]; then
    echo "Spark job completed successfully."
else
    echo "Spark job failed."
    exit 1
fi
```
```bash
./run_spark_job.sh 2024-01-01 2024-12-31
```

