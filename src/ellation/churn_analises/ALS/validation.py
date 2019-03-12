import pyspark.sql.functions as F

df_train_full = ''

display(
    df_train_full.groupBy('churn').agg(
        F.avg('free_seconds'),
        F.avg('paid_seconds'),
        F.avg('total_days'),
        F.avg('avg_sd'),
        F.avg('avg_iat'),
        F.avg('five_or_less'),
        F.avg('ten_or_less'),
        F.avg('fifteen_or_less'),
        F.avg('twenty_or_less'),
        F.avg('more_than_twenty'),
        F.avg('skip_ratio'),
        F.avg('sum_consumption_time'),
        F.avg('std_sd'),
        F.avg('std_iat'),
        F.avg('total_streams'),
        F.avg('std_free_seconds'),
        F.avg('std_paid_seconds'),
        F.avg('f1'),
        F.avg('f2'),
        F.avg('f3'),
        F.avg('f4'),
        F.avg('f5'),
    )
)
