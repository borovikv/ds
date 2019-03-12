from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import VectorAssembler


def under_sampling(df_train_full):
    df_class_0 = df_train_full[df_train_full['churn'] == 0]
    df_class_1 = df_train_full[df_train_full['churn'] == 1]
    sampling_ratio = 0.083717
    sampling_ratio = df_class_1.count() / df_class_0.count()
    df_class_0_s = df_class_0.sample(False, sampling_ratio, seed=0)
    trainingData = df_class_1.union(df_class_0_s)
    trainingData.groupBy('churn').count().show()
    return trainingData


def load_csv(path):
    # CSV options
    return spark.read.format("csv") \
        .option("inferSchema", True) \
        .option("header", True) \
        .option("sep", ",") \
        .load(path) \
        .na \
        .fill(0)


def scoring(prediction):
    evaluator = MulticlassClassificationEvaluator(labelCol="churn", predictionCol="prediction", metricName="f1")
    f1 = evaluator.evaluate(prediction)
    tp = prediction[(prediction.churn == 1) & (prediction.prediction == 1)].count() * 1.0
    tn = prediction[(prediction.churn == 0) & (prediction.prediction == 0)].count() * 1.0
    fp = prediction[(prediction.churn == 0) & (prediction.prediction == 1)].count() * 1.0
    fn = prediction[(prediction.churn == 1) & (prediction.prediction == 0)].count() * 1.0
    print("F1 score:", f1)
    print("True Negatives:", round(tn / (tn + fp), 2), "False Positives:", round(fp / (tn + fp), 2))
    print("False Negatives:", round(fn / (fn + tp), 2), "True Positives:", round(tp / (fn + tp), 2))


featureCols = [
    "free_seconds",
    "paid_seconds",
    "total_days",
    "avg_sd",
    "avg_iat",
    "five_or_less",
    "ten_or_less",
    "fifteen_or_less",
    "twenty_or_less",
    "more_than_twenty",
    "skip_ratio",
    "sum_consumption_time",
    "std_sd",
    "std_iat",
    "total_streams",
    "std_free_seconds",
    "std_paid_seconds",
    "f1",
    "f2",
    "f3",
    "f4",
    "f5",
]

df_features_17 = load_csv('s3://codemobs-datalab/ml/features_17_2018_clear_check/')
version = '20190301_084913'
hidden_features_df = load_csv('s3://codemobs-datalab/ml/vladimir/hidden_features/v=%s/' % version)
df = df_features_17.join(hidden_features_df, df_features_17.dwed_account_key == hidden_features_df.userId)

data = VectorAssembler(inputCols=featureCols, outputCol="features").transform(df)
(df_train_full, testData) = data.randomSplit([0.7, 0.3], seed=15)
trainingData = under_sampling(df_train_full)

model = RandomForestClassifier(labelCol="churn", featuresCol="features", numTrees=56, maxDepth=12)
model = model.fit(trainingData)
prediction = model.transform(testData)
scoring(prediction)
