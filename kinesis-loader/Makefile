.PHONY: create-role

AWS_USER_ID=""
EKS_CLUSTER_NAME=""
S3_RAW_DATA_BUCKET="mysense-raw-data-bucket"
FIREHOSE_STREAM="mysense-raw-data-stream"
KINESIS_LOAD_ROLE="firehose_delivery_role"
KINESIS_LOAD_POLICY="mysense-firehose-policy"
ECR_REPO_NAME="mysense-app/kinesis-loader"

create-role:
	aws iam create-role --role-name ${KINESIS_LOAD_ROLE}

create-policy:
	aws iam create-policy --policy-name ${KINESIS_LOAD_POLICY} --cli-input-json file://iam-policy.json

attach-role-policy: create-raw-data-bucket create-firehose-stream create-role create-policy
	aws iam attach-role-policy --role-name ${KINESIS_LOAD_ROLE} --policy-arn arn:aws:iam::${AWS_USER_ID}:policy/${KINESIS_LOAD_POLICY}

create-raw-data-bucket:
	aws s3 mb s3://${S3_RAW_DATA_BUCKET}

create-firehose-stream: attach-role-policy
	aws firehose create-delivery-stream --delivery-stream-name ${FIREHOSE_STREAM} --cli-input-json file://kinesis-stream.json

create-ecr-repo:
	aws ekr create-repository --repository-name ${ECR_REPO_NAME}

build:
	docker build -t kinesis-loader .

tag: build
	docker tag kinesis-loader ${AWS_USER_ID}.dkr.ecr.us-east-2.amazonaws.com/${ECR_REPO_NAME}:latest

push: tag
	docker push ${AWS_USER_ID}.dkr.ecr.us-east-2.amazonaws.com/${ECR_REPO_NAME}:latest

run:
	kubectl apply -f kube-job.yml
