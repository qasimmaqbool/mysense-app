## AWS Glue Aggregator Job ##
This directory includes code to create and run an ETL job on AWS Glue. The basic task of the job is to read CSV data 
from S3 and write it back as re-partitioned Parquet files. 

### How it works ###
* Firstly, we create a Glue Classifier which defines the structure of our CSV data. The file `glue-classifier.json` 
includes a specification for how to define a classifier.
* Next, we define a Glue Crawler that reads (or crawls) S3 data and makes it usable in a Glue job by creating a Glue
database. The spec for this crawler can be found in `glue-classifier.json`.
* Once created, we need to run the crawler to initialize our Glue database. If data is being written to S3 continually, 
the crawler would also need to run periodically in order to bring in data for our ETL job. 
* After the crawler has successfully run, we can launch the ETL job which will perform any necessary transformations 
and write data back to S3 in Parquet format. The definition of this job is present in `glue-job.json` while 
`mysense-csv-aggregator.py` contains the Python code to be executed. 

### How to run it ###
* Add AWS_USER_ID in Makefile to specify the AWS project.
* Set the S3 buckets and other resource values accordingly in all 3 JSON specification files.
* `make run` will perform all the steps listed above.