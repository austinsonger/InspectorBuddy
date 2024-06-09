import logging
import boto3
import json
from entrypoint import pkg_vuln

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
        findings_detail = pkg_vuln.process_findings_to_json(findings)
        print(f"Findings: {findings_detail}")
        pkg_vuln.set_github_actions_output('inspector_scan_results', findings_detail)
        return 0
    except Exception as e:
        logging.error(f"Failed to fetch findings: {e}")
        return 1
