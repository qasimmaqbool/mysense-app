from pyspark.sql import SQLContext
import pyspark.sql.functions as functions
import boto3

from pyspark import SparkContext

S3_PATH = 's3a://prediction-data-parquet/*.snappy.parquet'


if __name__ == "__main__":
    sc = SparkContext(appName="Aggregator")
    sql_context = SQLContext(sc)
    df = sql_context.read.parquet(S3_PATH)
    x = df.select('signal', 'orgs_bvid').filter("signal != ''")
    z = x.groupBy('signal').agg(functions.countDistinct('orgs_bvid').alias("count"))

    table_name = 'signalcounts'
    dynamodb = boto3.resource('dynamodb', 'us-east-2')
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'signal',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'orgs_count',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'signal',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'orgs_count',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    res = z.collect()  # now that we are done with calculations, convert to a list in order to easily iterate

    with table.batch_writer() as batch:
        for value in res:
            batch.put_item(
                Item={
                    'signal': value['signal'],
                    'orgs_count': value['count']
                }
            )
