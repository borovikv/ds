import datetime

import pyspark.sql.functions as F
import pyspark.sql.functions as func
from dateutil import parser
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row, Window
from pyspark.sql.functions import col, udf
from pyspark.sql.types import *

normalizedViewershipFileName = 's3://codemobs-datalab/ml/features_hidden_2018/'
mediaFileName = 's3://codemobs-datalab/ml/cr_media/'


# Read viewership data from input file
def normalizedViewershipMapper(line):
    fields = line.split(',')
    return Row(
        userIdInt=int(fields[0]),
        userId=str(fields[1].encode("utf-8")),
        mediaId=str(fields[2].encode("utf-8")),
        latestEventSent=parser.parse(fields[4]),
        avgFracViewed=float(fields[6]),
        isCompletelyWatched=str(fields[5].encode("utf-8"))
    )


# Read media data from input file
def mediaMapper(line):
    fields = line.split(',')
    return Row(
        mediaId=str(fields[0].encode("utf-8")),
        typ=str(fields[1].encode("utf-8")),
        title=str(fields[2].encode("utf-8")),
    )


dfMedia = spark.createDataFrame(spark.sparkContext.textFile(mediaFileName).map(mediaMapper)) \
    .withColumn("mediaIdInt", func.row_number().over(Window().orderBy("mediaId")))

dfViewNormalized = spark.createDataFrame(
    spark.sparkContext.textFile(normalizedViewershipFileName).map(normalizedViewershipMapper))

dfViewNormalizedWithMedia = dfViewNormalized.join(dfMedia, "mediaId").cache()

dfUserIdMap = dfViewNormalizedWithMedia.select('userId', 'userIdInt').distinct().cache()
maxUserIdInt = dfUserIdMap.select(func.max("userIdInt")).first()[0]

dfPopularity = dfViewNormalizedWithMedia \
    .select('mediaIdInt', 'mediaId') \
    .groupby('mediaIdInt', 'mediaId') \
    .agg(func.count('mediaIdInt').alias('countMedia')) \
    .withColumn('fracPopular',
                col('countMedia') / func.max('countMedia').over(Window().orderBy(func.desc('countMedia')))) \
    .withColumn('expPopular', (func.exp(-1 * col('fracPopular')))) \
    .select('mediaIdInt', 'mediaId', 'expPopular', 'fracPopular') \
    .cache()

dfViewForAls = dfViewNormalizedWithMedia \
    .join(dfPopularity, ['mediaIdInt', 'mediaId']) \
    .withColumn('implicitRating', udf(lambda x, y: float(x) * float(y), FloatType())('avgFracViewed', 'expPopular')) \
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

featuresDF = model.userFactors \
    .where(col('id') > maxUserIdInt) \
    .withColumn('userIdInt', udf(lambda x: x - maxUserIdInt)('id')) \
    .drop("id")

user_feateures_df = featuresDF.join(dfUserIdMap, featuresDF.userIdInt == dfUserIdMap.userIdInt) \
    .select("userId", "features") \
    .withColumn('f1', F.col('features').getItem(0)) \
    .withColumn('f2', F.col('features').getItem(1)) \
    .withColumn('f3', F.col('features').getItem(2)) \
    .withColumn('f4', F.col('features').getItem(3)) \
    .withColumn('f5', F.col('features').getItem(4)) \
    .drop("features")

version = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
path = "s3://codemobs-datalab/ml/vladimir/hidden_features/v={version}".format(version=version)
user_feateures_df.write.save(path, format='csv', header=True)
