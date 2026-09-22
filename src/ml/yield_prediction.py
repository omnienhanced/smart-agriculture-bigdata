from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator


# --------------------------------------------------
# 1. Spark Session
# --------------------------------------------------

spark = (
    SparkSession.builder
    .appName("MaharashtraYieldPrediction")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# --------------------------------------------------
# 2. Read Data
# --------------------------------------------------

input_path = (
    "hdfs://localhost:9000/"
    "smart-agriculture/input/agriculture_data.csv"
)

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)


# --------------------------------------------------
# 3. Features
# --------------------------------------------------

features = [
    "rainfall_mm",
    "temperature_c",
    "humidity_pct",
    "soil_ph",
    "nitrogen_kg_ha",
    "phosphorus_kg_ha",
    "potassium_kg_ha",
    "fertilizer_kg_ha",
    "area_hectares"
]


data = df.select(
    *features,
    "yield_tonnes_ha"
).dropna()


# --------------------------------------------------
# 4. Assemble Features
# --------------------------------------------------

assembler = VectorAssembler(
    inputCols=features,
    outputCol="features"
)


# --------------------------------------------------
# 5. Random Forest Regression
# --------------------------------------------------

regressor = RandomForestRegressor(
    featuresCol="features",
    labelCol="yield_tonnes_ha",
    numTrees=50,
    seed=42
)


# --------------------------------------------------
# 6. Pipeline
# --------------------------------------------------

pipeline = Pipeline(
    stages=[
        assembler,
        regressor
    ]
)


# --------------------------------------------------
# 7. Train/Test Split
# --------------------------------------------------

train_data, test_data = data.randomSplit(
    [0.8, 0.2],
    seed=42
)

print("\n================ DATASET ================\n")

print("Total records:", data.count())
print("Training records:", train_data.count())
print("Testing records:", test_data.count())


# --------------------------------------------------
# 8. Train Model
# --------------------------------------------------

print("\n================ TRAINING ================\n")

model = pipeline.fit(train_data)


# --------------------------------------------------
# 9. Prediction
# --------------------------------------------------

predictions = model.transform(test_data)


print("\n================ PREDICTIONS ================\n")

predictions.select(
    "yield_tonnes_ha",
    "prediction"
).show(20)


# --------------------------------------------------
# 10. RMSE
# --------------------------------------------------

rmse_evaluator = RegressionEvaluator(
    labelCol="yield_tonnes_ha",
    predictionCol="prediction",
    metricName="rmse"
)

rmse = rmse_evaluator.evaluate(predictions)


# --------------------------------------------------
# 11. R2 Score
# --------------------------------------------------

r2_evaluator = RegressionEvaluator(
    labelCol="yield_tonnes_ha",
    predictionCol="prediction",
    metricName="r2"
)

r2 = r2_evaluator.evaluate(predictions)


print("\n================ MODEL PERFORMANCE ================\n")

print("RMSE:", round(rmse, 4))
print("R2 Score:", round(r2, 4))


# --------------------------------------------------
# 12. Save Model
# --------------------------------------------------

model_path = (
    "hdfs://localhost:9000/"
    "smart-agriculture/output/yield_model"
)

model.write().overwrite().save(model_path)

print("\nYield model saved to:")
print(model_path)


# --------------------------------------------------
# 13. Stop Spark
# --------------------------------------------------

spark.stop()

print("\n================ YIELD MODEL COMPLETED ================\n")
