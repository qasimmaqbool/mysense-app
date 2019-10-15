## Mysense App
Loads data from a CSV into S3 via Firehose, transforms it to Parquet through a 
Glue ETL job, and finally aggregates counts of orgs per signal in an EMR Spark job.

#### How to run? 
 - An (almost-completely) automated setup is provided with user required to make a few manual entries and run GNU make commands
 - Pre-req: set up AWS CLI with valid credentials and a default region

### Kinesis-Loader
 - Add AWS_USER_ID to `kinesis-loader/Makefile`
 - If you have an existing EKS cluster (its 2019, you should!), add its name to EKS_CLUSTER_NAME variable in the same Makefile. 
 - If no EKS cluster is available, use [this guide](https://hackernoon.com/quickly-spin-up-an-aws-eks-kubernetes-cluster-using-cloudformation-3d59c56b292e) to set one up quickly 
 - To start loading CSV data to S3, run these commands in `kinesis-loader` directory: 
   - `make create-firehose-stream`
   - `make create-ecr-repo`
   - `make run` Note: `kubectl` should be configured to work with a Kubernetes cluster for this to succeed
 - Optional: remove the EKS cluster now if not needed.

### Glue ETL Job
 - Add AWS_USER_ID to `kinesis-loader/Makefile`
 - First, we need to bring the data from S3 in to Glue Data Catalog. For this, run commands in `glue-job` directory: 
    - `make create-crawler` 
    - `make start-crawler`
 - Once the Data Catalog table has been created, we can run the ETL job: 
    - `make run`
 
### EMR Spark Aggregation
 - To provision a cluster, we first need to run: 
    - `make create-emr-cluster`
 - The output of the command above should be inserted as EMR_CLUSTER_ID in `aggregator/Makefile`
 - To launch the Spark job, execute: 
    - `make run`
 - Wait for the EMR step to complete. The aggregate counts should now be visible in a DynamoDB table called "signalcounts"
  