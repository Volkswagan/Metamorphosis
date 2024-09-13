from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("WordCountExample").getOrCreate()


df = spark.read.format("text") \
            .load("dbfs:/FileStore/shared_uploads/souvikdey9510@gmail.com/input.txt")


count_df = df.select(explode(split("value", " ")).alias("word")) \
                .groupBy("word").count().sort("count", ascending=False)

count_df.write.format("csv") \
    .mode("overwrite") \
    .save("dbfs:/FileStore/shared_uploads/souvikdey9510@gmail.com/output")



count_rdd = df.rdd.flatMap(lambda line: line.split(" "))\
                .map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
count_rdd.saveAsTextFile("dbfs:/FileStore/shared_uploads/souvikdey9510@gmail.com/output2.txt")