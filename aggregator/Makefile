
EMR_CLUSTER_NAME=mysense-agg-cluster
S3_CODE_BUCKET=predict-aggregator-code
EMR_CLUSTER_ID=""

upload-install-deps-script:
	aws s3 cp install-deps.sh s3://${S3_CODE_BUCKET}/install-deps.sh

create-emr-cluster: upload-install-deps-script
	aws emr create-cluster --name ${EMR_CLUSTER_NAME} \
    --release-label emr-5.9.0 --ec2-attributes InstanceProfile=EMR_EC2_DefaultRole --service-role EMR_DefaultRole \
    --applications Name=Spark --bootstrap-actions Path=s3://${S3_CODE_BUCKET}/install-deps.sh \
    --instance-groups InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m4.large InstanceGroupType=CORE,InstanceCount=2,InstanceType=m4.large

upload-job-script:
	aws s3 cp aggregator-pyspark.py s3://${S3_CODE_BUCKET}/aggregator-pyspark.py

run: upload-job-script
	aws emr add-steps --cluster-id ${EMR_CLUSTER_ID} --steps Type=spark,Name=MysenseAggregator,Args=[--deploy-mode,cluster,s3://${S3_CODE_BUCKET}/aggregator-pyspark.py],ActionOnFailure=CONTINUE

shutdown-emr-cluster:
	aws emr terminate-clusters --cluster-ids ${EMR_CLUSTER_ID}
