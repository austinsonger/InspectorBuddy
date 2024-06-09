#!/bin/sh -l

set -e

AWS_ACCESS_KEY_ID=$1
AWS_SECRET_ACCESS_KEY=$2
AWS_REGION=$3
ASSESSMENT_RUN_ARN=$4

# Configure AWS CLI
aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
aws configure set region "$AWS_REGION"

# Run the main Python script
python3 main.py --aws-access-key-id "$AWS_ACCESS_KEY_ID" --aws-secret-access-key "$AWS_SECRET_ACCESS_KEY" --aws-region "$AWS_REGION" --assessment-run-arn "$ASSESSMENT_RUN_ARN"
