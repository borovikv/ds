import pandas as pd
from matplotlib import pyplot as plt
from pyspark.ml.classification import DecisionTreeClassifier, RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import Normalizer, VectorAssembler


def under_sample(df_train_full):
    df_train_full.groupBy('churn').count().show()
    df_class_0 = df_train_full[df_train_full['churn'] == 0]
    df_class_1 = df_train_full[df_train_full['churn'] == 1]
    ratio = 1.0 * df_class_1.count() / df_class_0.count()
    df_class_0_s = df_class_0.sample(False, ratio, seed=0)

    result = df_class_1.union(df_class_0_s)
    return result


def ExtractFeatureImp(featureImp, dataset, featuresCol):
    list_extract = []
    for i in dataset.schema[featuresCol].metadata["ml_attr"]["attrs"]:
        list_extract = list_extract + dataset.schema[featuresCol].metadata["ml_attr"]["attrs"][i]
    varlist = pd.DataFrame(list_extract)
    varlist['score'] = varlist['idx'].apply(lambda x: featureImp[x])
    return (varlist.sort_values('score', ascending=False))


def load_csv(path):
    return spark.read.format("csv") \
        .option("inferSchema", True) \
        .option("header", True) \
        .option("sep", ",") \
        .load(path) \
        .na \
        .fill(0)


def print_confusion_matrix_1(df):
    tp = df[(df.churn == 1) & (df.prediction == 1)].count() * 1.0
    tn = df[(df.churn == 0) & (df.prediction == 0)].count() * 1.0
    fp = df[(df.churn == 0) & (df.prediction == 1)].count() * 1.0
    fn = df[(df.churn == 1) & (df.prediction == 0)].count() * 1.0
    confusion = [[tn, fp], [fn, tp]]
    d = pd.DataFrame(confusion, index=['not churn', 'churn'], columns=['predicted not churn', 'predicted churn'])
    print('before normalisation')
    print(d)
    d = d.div(d.sum(axis=1), axis=0)
    print('after normalisation')
    print(d)
    print('F1 = ', F1(tp, fp, fn))
    tp1 = d['predicted not churn']['not churn']
    fp1 = d['predicted churn']['not churn']
    fn1 = d['predicted not churn']['churn']
    print('F1 = ', F1(tp1, fp1, fn1))


def F1(TP, FP, FN):
    recall = TP / (TP + FN)
    precision = TP / (TP + FP)
    f1 = 2 * recall * precision / (recall + precision)
    return f1


def normalize_data(data):
    normalizer = Normalizer(inputCol="features", outputCol="norm_features")
    ndata = normalizer.transform(data)
    return ndata


features_path = "s3://codemobs-datalab/ml/features/2019-03-27/e901434/main/"

df_features = load_csv(features_path)

data = df_features
featureCols = [
    "mins_watched_after_launch_week",
    "mins_watched_within_launch_week",
    "total_days",
    "avg_sd",
    "avg_iat",
    "zero",
    "one_to_five",
    "six_to_ten",
    "eleven_to_fifteen",
    "sixteen_to_twenty",
    "twenty_one_or_more",
    "skip_ratio",
    "sum_consumption_time",
    "std_sd",
    "std_iat",
    "total_streams",
    "std_mins_watched_after_launch_week",
    "std_mins_watched_within_launch_week",
    "previous_subscriptions_count"
]
assembler = VectorAssembler(inputCols=featureCols, outputCol="features")
data = assembler.transform(data)

(df_train_full, validation_data) = data.randomSplit([0.7, 0.3], seed=0)

training_data = under_sample(df_train_full)
training_data.groupBy('churn').count().show()

rmc = RandomForestClassifier(labelCol="churn", featuresCol="features", numTrees=56, maxDepth=12)
dtc = DecisionTreeClassifier(labelCol="churn", featuresCol="features", maxDepth=5)

models = [rmc, dtc]
evaluator = MulticlassClassificationEvaluator(labelCol="churn", predictionCol="prediction", metricName="f1")

# -----------------------------------------------------------------------------------------------------------------

f1_by_model = []
for model in models:
    model = model.fit(training_data)
    df = model.transform(validation_data)
    f1_by_model.append({'model': model.__class__.__name__, 'f1': evaluator.evaluate(df)})
    print_confusion_matrix_1(df)

print(pd.DataFrame(f1_by_model))

# -----------------------------------------------------------------------------------------------------------------


df_class_0 = training_data[training_data['churn'] == 0].sample(False, 0.01, seed=0).cache()
df_class_1 = training_data[training_data['churn'] == 1].sample(False, 0.01, seed=0).cache()


def binned_df(df, feature):
    pdf = df.toPandas()
    pdf['binned'] = pd.cut(pdf[feature], bins=10, labels=range(10))
    pdf = pdf.groupby('binned').count()
    return pd.to_numeric(pdf.index), pdf.previous_subscriptions_count


columns = 3
fig, ax = plt.subplots(7, columns, figsize=(15, 30))
for i, f in enumerate(featureCols):
    r = (i + columns) // columns - 1
    c = i % columns
    ax[r][c].set_title(f)

    x, y = binned_df(df_class_0, f)
    ax[r][c].scatter(x, y, marker='^', c='r', s=80, edgecolors='w')

    x, y = binned_df(df_class_1, f)
    ax[r][c].scatter(x, y, marker='o', c='g', s=80, edgecolors='w')

fig.subplots_adjust(hspace=0.5)

display(fig)
