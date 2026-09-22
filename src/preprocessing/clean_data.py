from pyspark.sql import SparkSession
from pyspark.sql.functions import col


spark = (
    SparkSession.builder
    .appName("AgricultureDataCleaning")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


input_path = "hdfs://localhost:9000/smart-agriculture/input/agriculture_data.csv"

output_path = "hdfs://localhost:9000/smart-agriculture/output/cleaned"


# Read data
df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)

print("Original records:", df.count())


# Remove duplicate records
df = df.dropDuplicates()

print("After removing duplicates:", df.count())


# Remove records containing null values
df = df.dropna()

print("After removing null values:", df.count())


# Basic filtering
df = df.filter(
    (col("rainfall_mm") >= 0) &
    (col("temperature_c") >= 0) &
    (col("humidity_pct") >= 0) &
    (col("soil_ph") > 0) &
    (col("yield_tonnes_ha") > 0)
)

print("After filtering:", df.count())


# Save cleaned data
(
    df.write
    .mode("overwrite")
    .option("header", "true")
    .csv(output_path)
)

print("Cleaned dataset saved to:")
print(output_path)


spark.stop()
