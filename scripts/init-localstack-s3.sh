#!/bin/bash

# aws configure --profile localstack
# access_key=test
# secret_key=test
# region=us-east-1
# aws --profile localstack --endpoint-url=http://localhost:4566 s3 ls
# alias awslocal='aws --profile localstack --endpoint-url=http://localhost:4566'
awslocal s3 mb s3://notgoogleplus-bucket
