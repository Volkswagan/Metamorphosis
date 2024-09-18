1. You can add new columns to a Parquet schema. When you read old Parquet files with a schema that has new columns, the missing columns will have null values in the resulting data.
2. You can remove columns from a schema. When you read Parquet files with columns that are no longer present in the schema, those columns will be ignored.
3. The schema evolution feature in Parquet does not automatically handle type changes.
4. The order of columns in Parquet files is not enforced, so the schema order can be different from the original schema when reading the data.
5. You cannot change the contents of an existing Parquet file directly. To update or modify data, you typically need to create new Parquet files or overwrite existing ones. This often involves writing the updated data to new files and possibly deleting or archiving the old files.
---
When we submit a Spark job using the spark-submit command, specifying YARN as the cluster manager.
The YARN ResourceManager receives the job request and allocates resources (containers) to the Spark application.
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
---
1. coalesce is better than repartition while decreasing the number of partitions because it does not involve a full shuffle of data across nodes. It just merges existing partitions.
2. Client Mode: The Spark Driver runs on the machine where you submit the job (e.g., your laptop or a gateway node). The driver communicates with the cluster's executors remotely and the executors run on the cluster.
3. Cluster Mode: The Spark Driver runs inside the cluster, typically on one of the cluster's worker nodes. Submitting a job to the cluster, and both the driver and executors run on the cluster's nodes.
---
### **1. `map` vs `flatMap` vs `mapPartitions`**

**1.1 `map`**
- **Function**: Applies a function to each element in an RDD or DataFrame, producing one output element for each input element.
- **Use Case**: When you need to transform each element individually and produce a single element per input element.
- **Example**:
  ```python
  rdd = sc.parallelize([1, 2, 3])
  mapped_rdd = rdd.map(lambda x: x * 2)  # Output: [2, 4, 6]
  ```

**1.2 `flatMap`**
- **Function**: Applies a function to each element in an RDD or DataFrame, producing zero or more output elements for each input element. It "flattens" the results into a single RDD.
- **Use Case**: When each input element can produce multiple output elements, or when you need to flatten nested collections.
- **Example**:
  ```python
  rdd = sc.parallelize([1, 2, 3])
  flat_mapped_rdd = rdd.flatMap(lambda x: [x, x * 2])  # Output: [1, 2, 2, 4, 3, 6]
  ```

**1.3 `mapPartitions`**
- **Function**: Applies a function to each partition of the RDD or DataFrame, producing an iterator for each partition. This allows you to perform operations on an entire partition rather than individual elements.
- **Use Case**: When you want to process data in bulk for each partition, which can be more efficient than processing each element individually.
- **Example**:
  ```python
  def process_partition(iterator):
      yield sum(iterator)

  rdd = sc.parallelize([1, 2, 3, 4], 2)  # Two partitions
  partition_sums = rdd.mapPartitions(process_partition)  # Output: [3, 7]
  ```

### **2. `reduceByKey` vs `groupByKey`**

**2.1 `reduceByKey`**
- **Function**: Combines values with the same key using a specified reduce function. It performs a local reduction on each partition before shuffling data to the reducer, which is more efficient.
- **Use Case**: When you want to aggregate or combine values by key in an efficient manner.
- **Example**:
  ```python
  rdd = sc.parallelize([('a', 1), ('b', 2), ('a', 3)])
  reduced_rdd = rdd.reduceByKey(lambda x, y: x + y)  # Output: [('a', 4), ('b', 2)]
  ```

**2.2 `groupByKey`**
- **Function**: Groups values with the same key into a collection (e.g., a list). It involves a shuffle operation and does not perform any aggregation before shuffling, which can be less efficient.
- **Use Case**: When you need to group values by key and are planning to perform additional processing on the grouped data.
- **Example**:
  ```python
  rdd = sc.parallelize([('a', 1), ('b', 2), ('a', 3)])
  grouped_rdd = rdd.groupByKey()  # Output: [('a', [1, 3]), ('b', [2])]
  ```

### **3. Hash Partitioning vs Range Partitioning**

**3.1 Hash Partitioning**
- **Function**: Distributes data across partitions based on the hash value of the key. It ensures that records with the same key are sent to the same partition but does not consider the range of key values.
- **Use Case**: When you need even distribution of data across partitions and are not concerned about the order of keys.
- **Example**: Using `rdd.partitionBy(numPartitions)` where the partitioning function is based on hashing.

**3.2 Range Partitioning**
- **Function**: Distributes data across partitions based on specified ranges of key values. It is used to partition data such that each partition contains data within a certain range of key values.
- **Use Case**: When you need ordered data within partitions or when the data distribution is not uniform and you want to manage ranges of keys.
- **Example**: Using `rdd.keyBy(lambda x: x).partitionBy(numPartitions, lambda x: x[0])` where the partitioning function is based on key ranges.

