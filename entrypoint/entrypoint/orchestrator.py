import logging
import boto3
import json

def execute(args) -> int:
    logging.info("Starting the Amazon Inspector EC2 scan results fetch process")

    client = boto3.client(
        'inspector',
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        region_name=args.aws_region
    )

    try:
        findings = client.list_findings(assessmentRunArns=[args.assessment_run_arn])
        logging.info("Successfully fetched findings")
        process_findings(findings)
        return 0
    except Exception as e:
        logging.error(f"Failed to fetch findings: {e}")
        return 1

def process_findings(findings):
    logging.info("Processing findings")
    findings_detail = json.dumps(findings, indent=4)
    print(f"Findings: {findings_detail}")

def set_github_actions_output(name: str, value: str):
    logging.info(f"Setting GitHub Actions output - {name}: {value}")
    print(f"::set-output name={name}::{value}")
