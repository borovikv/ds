import io

import boto3
import pandas as pd

BUCKET = 'codemobs-datalab'


def read_prefix_to_df(bucket, prefix, columns):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    prefix_objs = bucket.objects.filter(Prefix=prefix)
    prefix_df = []
    for obj in prefix_objs:
        body = obj.get()['Body'].read()
        df = pd.read_csv(io.BytesIO(body), names=columns)
        prefix_df.append(df)
    return pd.concat(prefix_df)


def load_media():
    read_prefix_to_df(
        BUCKET, prefix='ml/cr_media', columns=['mediaId', 'type', 'title']
    ).to_csv('cr_media.csv', index=False)


def load_viewerships():
    read_prefix_to_df(
        BUCKET,
        prefix='ml/features_hidden_2018/0000_part_00',
        columns=[
            'userIdInt',
            'userId',
            'mediaId',
            'latestEventSent',
            'avgFracViewed',
            'isCompletelyWatched',
        ]
    ).to_csv('normalized_viewership.csv', index=False)

# load_media()
# load_viewerships()
