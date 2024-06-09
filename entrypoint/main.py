#!/usr/bin/env python3

import sys
import boto3

def main():
    # Example: Fetch findings from Amazon Inspector
    aws_access_key_id = sys.argv[1]
    aws_secret_access_key = sys.argv[2]
    aws_region = sys.argv[3]
    assessment_run_arn = sys.argv[4]

    client = boto3.client(
        'inspector',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    findings = client.list_findings(assessmentRunArns=[assessment_run_arn])
    print(f"Findings: {findings}")

if __name__ == '__main__':
    main()
