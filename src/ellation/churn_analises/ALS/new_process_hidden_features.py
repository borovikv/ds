import datetime

import pyspark.sql.functions as f
from pyspark.ml.recommendation import ALS


def load_csv(path):
    return spark.read.format("csv") \
        .option("inferSchema", True) \
        .option("header", True) \
        .option("sep", ",") \
        .load(path) \
        .na \
        .fill(0)


rankParam = 5
normalizedViewershipFileName = 's3://codemobs-datalab/ml/features_hidden_2018/'

dfViewNormalizedWithMedia = load_csv(normalizedViewershipFileName)

dfViewForAls = dfViewNormalizedWithMedia.select('userIdInt', 'mediaIdInt', 'implicitRating')
als = ALS(
    maxIter=10,
    rank=rankParam,
    regParam=0.3,
    implicitPrefs=True,
    alpha=0.01,
    userCol="userIdInt",
    itemCol="mediaIdInt",
    ratingCol="implicitRating",
    coldStartStrategy="drop"
)
model = als.fit(dfViewForAls)

featuresDF = model.userFactors
dfUserIdMap = dfViewNormalizedWithMedia.select('userId', 'userIdInt').distinct()
result = featuresDF.join(dfUserIdMap, featuresDF.id == dfUserIdMap.userIdInt).select("userId", "features")

for i in range(rankParam):
    result = result.withColumn('f{}'.format(i + 1), f.col('features').getItem(i))

version = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
path = "s3://codemobs-datalab/ml/vladimir/hidden_features/v={version}".format(version=version)
result.drop("features").write.save(path, format='csv', header=True)
