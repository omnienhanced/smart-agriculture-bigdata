from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    sum,
    max,
    min,
    count,
    round,
    desc
)


# --------------------------------------------------
# 1. Create Spark Session
# --------------------------------------------------

spark = (
    SparkSession.builder
    .appName("MaharashtraSmartAgriculture")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# --------------------------------------------------
# 2. Read Dataset from HDFS
# --------------------------------------------------

input_path = "hdfs://localhost:9000/smart-agriculture/input/agriculture_data.csv"

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)


# --------------------------------------------------
# 3. Display Dataset Information
# --------------------------------------------------

print("\n================ DATASET SCHEMA ================\n")

df.printSchema()

print("\n================ FIRST 10 RECORDS ================\n")

df.show(10, truncate=False)

print("\n================ TOTAL RECORDS ================\n")

print("Total records:", df.count())


# --------------------------------------------------
# 4. Basic Statistics
# --------------------------------------------------

print("\n================ STATISTICS ================\n")

df.describe(
    "rainfall_mm",
    "temperature_c",
    "humidity_pct",
    "soil_ph",
    "nitrogen_kg_ha",
    "phosphorus_kg_ha",
    "potassium_kg_ha",
    "yield_tonnes_ha"
).show()


# --------------------------------------------------
# 5. Crop-wise Analysis
# --------------------------------------------------

print("\n================ CROP-WISE ANALYSIS ================\n")

crop_analysis = (
    df.groupBy("crop")
    .agg(
        count("*").alias("records"),
        round(avg("yield_tonnes_ha"), 2).alias("average_yield"),
        round(sum("production_tonnes"), 2).alias("total_production")
    )
    .orderBy(desc("average_yield"))
)

crop_analysis.show(truncate=False)


# --------------------------------------------------
# 6. District-wise Analysis
# --------------------------------------------------

print("\n================ DISTRICT-WISE ANALYSIS ================\n")

district_analysis = (
    df.groupBy("district")
    .agg(
        count("*").alias("records"),
        round(avg("yield_tonnes_ha"), 2).alias("average_yield"),
        round(sum("production_tonnes"), 2).alias("total_production")
    )
    .orderBy(desc("total_production"))
)

district_analysis.show(15, truncate=False)


# --------------------------------------------------
# 7. Season-wise Analysis
# --------------------------------------------------

print("\n================ SEASON-WISE ANALYSIS ================\n")

season_analysis = (
    df.groupBy("season")
    .agg(
        count("*").alias("records"),
        round(avg("yield_tonnes_ha"), 2).alias("average_yield"),
        round(sum("production_tonnes"), 2).alias("total_production")
    )
)

season_analysis.show(truncate=False)


# --------------------------------------------------
# 8. Region-wise Analysis
# --------------------------------------------------

print("\n================ REGION-WISE ANALYSIS ================\n")

region_analysis = (
    df.groupBy("region")
    .agg(
        count("*").alias("records"),
        round(avg("yield_tonnes_ha"), 2).alias("average_yield"),
        round(sum("production_tonnes"), 2).alias("total_production")
    )
    .orderBy(desc("total_production"))
)

region_analysis.show(truncate=False)


# --------------------------------------------------
# 9. Rainfall Analysis
# --------------------------------------------------

print("\n================ RAINFALL ANALYSIS ================\n")

rainfall_analysis = (
    df.groupBy("crop")
    .agg(
        round(avg("rainfall_mm"), 2).alias("average_rainfall"),
        round(avg("yield_tonnes_ha"), 2).alias("average_yield")
    )
    .orderBy(desc("average_yield"))
)

rainfall_analysis.show(truncate=False)


# --------------------------------------------------
# 10. Soil Analysis
# --------------------------------------------------

print("\n================ SOIL ANALYSIS ================\n")

soil_analysis = (
    df.groupBy("crop")
    .agg(
        round(avg("soil_ph"), 2).alias("average_soil_ph"),
        round(avg("nitrogen_kg_ha"), 2).alias("average_nitrogen"),
        round(avg("phosphorus_kg_ha"), 2).alias("average_phosphorus"),
        round(avg("potassium_kg_ha"), 2).alias("average_potassium")
    )
)

soil_analysis.show(truncate=False)


# --------------------------------------------------
# 11. Top Producing Districts
# --------------------------------------------------

print("\n================ TOP 10 DISTRICTS ================\n")

district_analysis.limit(10).show(truncate=False)


# --------------------------------------------------
# 12. Top Crops
# --------------------------------------------------

print("\n================ TOP CROPS ================\n")

crop_analysis.limit(10).show(truncate=False)


# --------------------------------------------------
# 13. Save Processed Data to HDFS
# --------------------------------------------------

output_path = "hdfs://localhost:9000/smart-agriculture/output/processed"

(
    df.write
    .mode("overwrite")
    .option("header", "true")
    .csv(output_path)
)

print("\nProcessed data successfully saved to HDFS.")


# --------------------------------------------------
# 14. Stop Spark
# --------------------------------------------------

spark.stop()

print("\n================ JOB COMPLETED ================\n")
