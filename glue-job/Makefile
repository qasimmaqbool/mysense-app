
AWS_USER_ID=""
GLUE_CRAWLER=mysense-app-crawler
GLUE_JOB_NAME=mysense-glue-etl
S3_BUCKET_SCRIPTS=mysense-app-glue-scripts
S3_BUCKET_PARQUET=prediction-data-parquet

create-classifier:
	aws glue create-classifier --cli-input-json file://glue-classifier.json

create-crawler: create-classifier
	aws glue create-crawler --name ${GLUE_CRAWLER} --cli-input-json file://glue-crawler.json

start-crawler:
	aws glue start-crawler --name ${GLUE_CRAWLER}

create-s3-bucket-scripts:
	aws s3 mb s3://${S3_BUCKET_SCRIPTS}

create-s3-bucket-parquet:
	aws s3 mb s3://${S3_BUCKET_PARQUET}

upload-job-script: create-s3-bucket-scripts
	aws s3 cp mysense-csv-aggregator.py s3://${S3_BUCKET_SCRIPTS}/mysense-csv-aggregator.py

create-glue-job: create-s3-bucket-parquet upload-job-script
	aws glue create-job --name ${GLUE_JOB_NAME} --cli-input-json file://glue-job.json

run: create-glue-job
	aws glue start-job-run --job-name ${GLUE_JOB_NAME}