import datetime

import pyspark.sql.functions as f
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row, Window

normalizedViewershipFileName = 's3://codemobs-datalab/ml/features_hidden_2018/'
mediaFileName = 's3://codemobs-datalab/ml/cr_media/'


def normalizedViewershipMapper(line):
    fields = line.split(',')
    return Row(
        userIdInt=int(fields[0]),
        userId=str(fields[1].encode("utf-8")),
        mediaId=str(fields[2].encode("utf-8")),
        latestEventSent=fields[4],
        avgFracViewed=float(fields[6]),
        isCompletelyWatched=str(fields[5].encode("utf-8"))
    )


def mediaMapper(line):
    fields = line.split(',')
    return Row(
        mediaId=str(fields[0].encode("utf-8")),
        typ=str(fields[1].encode("utf-8")),
        title=str(fields[2].encode("utf-8")),
    )


dfMedia = spark.createDataFrame(
    spark.sparkContext.textFile(mediaFileName).map(mediaMapper)) \
    .withColumn("mediaIdInt", f.row_number().over(Window().orderBy("mediaId")))

dfViewNormalized = spark.createDataFrame(
    spark.sparkContext.textFile(normalizedViewershipFileName).map(normalizedViewershipMapper))

dfViewNormalizedWithMedia = dfViewNormalized.join(dfMedia, "mediaId").cache()

dfPopularity = dfViewNormalizedWithMedia \
    .select('mediaIdInt', 'mediaId') \
    .groupby('mediaIdInt', 'mediaId') \
    .agg(f.count('mediaIdInt').alias('countMedia')) \
    .withColumn('expPopular',
                f.exp(-1 * f.col('countMedia') / f.max('countMedia').over(Window().orderBy(f.desc('countMedia'))))) \
    .select('mediaIdInt', 'mediaId', 'expPopular') \
    .cache()

dfViewForAls = dfViewNormalizedWithMedia \
    .join(dfPopularity, ['mediaIdInt', 'mediaId']) \
    .withColumn('implicitRating', f.col('avgFracViewed') * f.col('expPopular')) \
    .select('userIdInt', 'mediaIdInt', 'implicitRating')

# Build the recommendation model using ALS on the training data
maxIterParam = 10
rankParam = 5
regParam = 0.3
alphaParam = 0.01
als = ALS(
    maxIter=maxIterParam,
    rank=rankParam,
    regParam=regParam,
    implicitPrefs=True,
    alpha=alphaParam,
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
