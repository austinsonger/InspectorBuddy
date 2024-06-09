#!/usr/bin/env python3

import sys
import boto3
from entrypoint import cli, installer

def main():
    # Initialize CLI arguments
    args = cli.init(sys.argv[1:])

    # Prepare the environment
    if not installer.prepare_environment(args.aws_access_key_id, args.aws_secret_access_key, args.aws_region):
        sys.exit(1)

    client = boto3.client(
        'inspector',
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        region_name=args.aws_region
    )

    findings = client.list_findings(assessmentRunArns=[args.assessment_run_arn])
    print(f"Findings: {findings}")

if __name__ == '__main__':
    main()
