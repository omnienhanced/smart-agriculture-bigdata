from pyspark.sql import SparkSession


spark = (
    SparkSession.builder
    .appName("AgricultureSparkSQL")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


input_path = "hdfs://localhost:9000/smart-agriculture/input/agriculture_data.csv"


df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)


# Create temporary SQL table
df.createOrReplaceTempView("agriculture")


print("\n========== TOTAL RECORDS ==========\n")

spark.sql("""
    SELECT COUNT(*) AS total_records
    FROM agriculture
""").show()


print("\n========== CROP PRODUCTION ==========\n")

spark.sql("""
    SELECT
        crop,
        ROUND(AVG(yield_tonnes_ha), 2) AS average_yield,
        ROUND(SUM(production_tonnes), 2) AS total_production
    FROM agriculture
    GROUP BY crop
    ORDER BY total_production DESC
""").show()


print("\n========== DISTRICT PRODUCTION ==========\n")

spark.sql("""
    SELECT
        district,
        ROUND(SUM(production_tonnes), 2) AS total_production
    FROM agriculture
    GROUP BY district
    ORDER BY total_production DESC
    LIMIT 10
""").show()


print("\n========== BEST YIELDING CROPS ==========\n")

spark.sql("""
    SELECT
        crop,
        ROUND(AVG(yield_tonnes_ha), 2) AS average_yield
    FROM agriculture
    GROUP BY crop
    ORDER BY average_yield DESC
""").show()


print("\n========== YEARLY PRODUCTION ==========\n")

spark.sql("""
    SELECT
        year,
        ROUND(SUM(production_tonnes), 2) AS production
    FROM agriculture
    GROUP BY year
    ORDER BY year
""").show()


spark.stop()
