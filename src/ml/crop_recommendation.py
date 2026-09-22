from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


# --------------------------------------------------
# 1. Create Spark Session
# --------------------------------------------------

spark = (
    SparkSession.builder
    .appName("MaharashtraCropRecommendation")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# --------------------------------------------------
# 2. Read Agriculture Dataset from HDFS
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


print("\n================ DATASET ================\n")
print("Total records:", df.count())


# --------------------------------------------------
# 3. Select Features
# --------------------------------------------------

features = [
    "rainfall_mm",
    "temperature_c",
    "humidity_pct",
    "soil_ph",
    "nitrogen_kg_ha",
    "phosphorus_kg_ha",
    "potassium_kg_ha"
]


data = df.select(
    *features,
    "crop"
).dropna()


# --------------------------------------------------
# 4. Convert Crop Name to Numerical Label
# --------------------------------------------------

label_indexer = StringIndexer(
    inputCol="crop",
    outputCol="label",
    handleInvalid="keep"
)


# --------------------------------------------------
# 5. Combine Features
# --------------------------------------------------

assembler = VectorAssembler(
    inputCols=features,
    outputCol="features",
    handleInvalid="skip"
)


# --------------------------------------------------
# 6. Random Forest Classifier
# --------------------------------------------------

classifier = RandomForestClassifier(
    featuresCol="features",
    labelCol="label",
    numTrees=50,
    seed=42
)


# --------------------------------------------------
# 7. Create ML Pipeline
# --------------------------------------------------

pipeline = Pipeline(
    stages=[
        label_indexer,
        assembler,
        classifier
    ]
)


# --------------------------------------------------
# 8. Train/Test Split
# --------------------------------------------------

train_data, test_data = data.randomSplit(
    [0.8, 0.2],
    seed=42
)

print("Training records:", train_data.count())
print("Testing records:", test_data.count())


# --------------------------------------------------
# 9. Train Model
# --------------------------------------------------

print("\n================ TRAINING MODEL ================\n")

model = pipeline.fit(train_data)


# --------------------------------------------------
# 10. Make Predictions
# --------------------------------------------------

predictions = model.transform(test_data)


print("\n================ SAMPLE PREDICTIONS ================\n")

predictions.select(
    "crop",
    "prediction",
    "probability"
).show(20, truncate=False)


# --------------------------------------------------
# 11. Evaluate Model
# --------------------------------------------------

evaluator = MulticlassClassificationEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="accuracy"
)

accuracy = evaluator.evaluate(predictions)

print("\n================ MODEL PERFORMANCE ================\n")

print("Accuracy:", round(accuracy * 100, 2), "%")


# --------------------------------------------------
# 12. Save Model
# --------------------------------------------------

model_path = (
    "hdfs://localhost:9000/"
    "smart-agriculture/output/crop_model"
)

model.write().overwrite().save(model_path)

print("\nModel saved to:")
print(model_path)


# --------------------------------------------------
# 13. Stop Spark
# --------------------------------------------------

spark.stop()

print("\n================ CROP MODEL COMPLETED ================\n")
