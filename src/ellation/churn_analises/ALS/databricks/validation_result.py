import pandas as pd
import pyspark.sql.functions as f
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.recommendation import ALS


def ExtractFeatureImp(featureImp, dataset, featuresCol):
    list_extract = []
    for i in dataset.schema[featuresCol].metadata["ml_attr"]["attrs"]:
        list_extract = list_extract + dataset.schema[featuresCol].metadata["ml_attr"]["attrs"][i]
    varlist = pd.DataFrame(list_extract)
    varlist['score'] = varlist['idx'].apply(lambda x: featureImp[x])
    return varlist.sort_values('score', ascending=False)


def print_confusion_matrix(df):
    tp = df[(df.churn == 1) & (df.prediction == 1)].count() * 1.0
    tn = df[(df.churn == 0) & (df.prediction == 0)].count() * 1.0
    fp = df[(df.churn == 0) & (df.prediction == 1)].count() * 1.0
    fn = df[(df.churn == 1) & (df.prediction == 0)].count() * 1.0
    print(tp, tn, fp, fn)
    # print("True Negatives:", round(tn / (tn + fp), 2), "False Positives:", round(fp / (tn + fp), 2))
    # print("False Negatives:", round(fn / (fn + tp), 2), "True Positives:", round(tp / (fn + tp), 2))
    evaluator = MulticlassClassificationEvaluator(labelCol="churn", predictionCol="prediction", metricName="f1")
    f1 = evaluator.evaluate(df)
    print("F1", f1)


def under_sample(df_train_full):
    df_class_0 = df_train_full[df_train_full['churn'] == 0]
    df_class_1 = df_train_full[df_train_full['churn'] == 1]
    ratio = 1.0 * df_class_1.count() / df_class_0.count()
    df_class_0_s = df_class_0.sample(False, ratio, seed=0)

    result = df_class_1.union(df_class_0_s)
    return result


def load_csv(path):
    return spark.read.format("csv") \
        .option("inferSchema", True) \
        .option("header", True) \
        .option("sep", ",") \
        .load(path) \
        .na \
        .fill(0)


def get_hidden_features_df(path):
    rankParam = 5
    dfViewNormalizedWithMedia = load_csv(path)
    dfViewForAls = dfViewNormalizedWithMedia.select('userIdInt', 'mediaId', 'implicitRating')
    als = ALS(
        maxIter=10,
        rank=rankParam,
        regParam=0.3,
        implicitPrefs=True,
        alpha=0.01,
        userCol="userIdInt",
        itemCol="mediaId",
        ratingCol="implicitRating",
        coldStartStrategy="drop"
    )
    als_model = als.fit(dfViewForAls)
    featuresDF = als_model.userFactors
    dfUserIdMap = dfViewNormalizedWithMedia.select('userId', 'userIdInt').distinct()
    result = featuresDF.join(dfUserIdMap, featuresDF.id == dfUserIdMap.userIdInt).select("userId", "features")
    for i in range(rankParam):
        result = result.withColumn('f{}'.format(i + 1), f.col('features').getItem(i))
    return result.drop("features")


normalizedViewershipFileName = 's3://codemobs-datalab/ml/normalised_viewerships_2019_03_13_2/'
features_path = "s3://codemobs-datalab/ml/features_2019_03_13"
validation_normalized_viewership_path = 's3://codemobs-datalab/ml/to_be_predicted/2019-03-13/normalised_viewerships/'
validation_features_path = "s3://codemobs-datalab/ml/to_be_predicted/2019-03-13/features/"
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
    "total_subscription_days"
]
seed = 15

hidden_features_df = get_hidden_features_df(normalizedViewershipFileName)
df_features = load_csv(features_path)
training_df = df_features.join(hidden_features_df, df_features.dwed_account_key == hidden_features_df.userId)

assembler = VectorAssembler(inputCols=featureCols, outputCol="features")
training_data = assembler.transform(training_df)
(df_train_full, df_test_data) = training_data.randomSplit([0.7, 0.3], seed=seed)
trainingData = under_sample(df_train_full)
trainingData.groupBy('churn').count().show()

rmc = RandomForestClassifier(labelCol="churn", featuresCol="features", numTrees=56, maxDepth=12).fit(trainingData)

test_prediction = rmc.transform(df_test_data)
print_confusion_matrix(test_prediction)
ExtractFeatureImp(rmc.stages[-1].featureImportances, test_prediction, "features").head(30)

hidden_features_df = get_hidden_features_df(validation_normalized_viewership_path)
df_features = load_csv(validation_features_path)
validation_data = df_features.join(hidden_features_df, df_features.dwed_account_key == hidden_features_df.userId)

validation_data = assembler.transform(validation_data)

validation_prediction = rmc.transform(validation_data)
print_confusion_matrix(validation_prediction)
