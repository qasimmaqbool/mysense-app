
GLUE_CRAWLER=mysense-app-crawler
GLUE_JOB_NAME=mysense-glue-etl

create-classifier:
	aws glue create-classifier --cli-input-json file://glue-classifier.json

create-crawler: create-classifier
	aws glue create-crawler --name ${GLUE_CRAWLER} --cli-input-json file://glue-crawler.json

start-crawler:
	aws glue start-crawler --name ${GLUE_CRAWLER}

create-s3-bucket-scripts:
	aws s3 mb s3://mysense-app-glue-scripts

upload-job-script: create-s3-bucket-scripts
	aws s3 cp mysense-csv-aggregator.py s3://mysense-app-glue-scripts/mysense-csv-aggregator.py

create-glue-job: upload-job-script
	aws glue create-job --name ${GLUE_JOB_NAME} --cli-input-json file://glue-job.json

run: create-glue-job
	aws glue start-job-run --job-name ${GLUE_JOB_NAME}