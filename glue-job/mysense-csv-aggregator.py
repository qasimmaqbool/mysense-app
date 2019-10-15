import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
## @type: DataSource
## @args: [database = "prediction-raw", table_name = "prediction_data_raw", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database="prediction-raw", table_name="2019", transformation_ctx="datasource0")
# datasource0 = glueContext.create_dynamic_frame_from_options("s3", {'paths': ["s3://prediction-data-raw/2019/10/13/20/"], 'recurse': True, 'groupFiles': 'inPartition', 'groupSize': '104857600'}, format="csv")
## @type: ApplyMapping
## @args: [mapping = [("col0", "long", "col0", "long"), ("col1", "double", "col1", "double"), ("col2", "string", "col2", "string"), ("col3", "string", "col3", "string"), ("col4", "string", "col4", "string"), ("col5", "string", "col5", "string"), ("col6", "long", "col6", "long"), ("col7", "string", "col7", "string"), ("col8", "string", "col8", "string"), ("col9", "string", "col9", "string"), ("col10", "string", "col10", "string"), ("col11", "double", "col11", "double"), ("col12", "string", "col12", "string"), ("partition_0", "string", "partition_0", "string"), ("partition_1", "string", "partition_1", "string"), ("partition_2", "string", "partition_2", "string"), ("partition_3", "string", "partition_3", "string")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]
applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("col0", "long", "ID", "long"), ("col1", "double", "sentiment", "double"), ("col2", "string", "orgs_bvid", "string"), ("col3", "string", "sub_signal", "string"), ("col4", "string", "source", "string"), ("col5", "string", "orgs", "string"), ("col6", "long", "corp-ctapproved_exists", "long"), ("col7", "string", "title", "string"), ("col8", "string", "similarityClusterID", "string"), ("col9", "string", "signal", "string"), ("col10", "string", "rowKey", "string"), ("col11", "double", "similarityScore", "double"), ("col12", "string", "timestamp", "string"), ("partition_0", "string", "partition_0", "string"), ("partition_1", "string", "partition_1", "string"), ("partition_2", "string", "partition_2", "string"), ("partition_3", "string", "partition_3", "string")], transformation_ctx = "applymapping1")
## @type: ResolveChoice
## @args: [choice = "make_struct", transformation_ctx = "resolvechoice2"]
## @return: resolvechoice2
## @inputs: [frame = applymapping1]
resolvechoice2 = ResolveChoice.apply(frame = applymapping1, choice = "make_struct", transformation_ctx = "resolvechoice2")
## @type: DropNullFields
## @args: [transformation_ctx = "dropnullfields3"]
## @return: dropnullfields3
## @inputs: [frame = resolvechoice2]
dropnullfields3 = DropNullFields.apply(frame = resolvechoice2, transformation_ctx = "dropnullfields3")
## @type: DataSink
## @args: [connection_type = "s3", connection_options = {"path": "s3://prediction-data-parquet"}, format = "parquet", transformation_ctx = "datasink4"]
## @return: datasink4
## @inputs: [frame = dropnullfields3]
datasink4 = glueContext.write_dynamic_frame.from_options(frame = dropnullfields3, connection_type = "s3", connection_options = {"path": "s3://prediction-data-parquet"}, format = "parquet", transformation_ctx = "datasink4")
job.commit()