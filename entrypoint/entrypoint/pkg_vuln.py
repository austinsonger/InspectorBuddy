import json
import logging
from typing import List

class Vulnerability:
    """
    Vulnerability is an object for marshalling vulnerability findings
    from Inspector's JSON into a Python object that can be queried and manipulated.
    """
    def __init__(self):
        self.vuln_id = "null"
        self.severity = "null"
        self.cvss_score = "null"
        self.description = "null"
        self.resource_type = "null"
        self.resource_id = "null"

def vulns_to_obj(inspector_findings_json) -> List[Vulnerability]:
    """
    Parses JSON from Inspector's API and returns a list of vulnerability objects.
    """
    vuln_list = []

    findings = inspector_findings_json.get("findings", [])
    for finding in findings:
        vuln_obj = Vulnerability()
        vuln_obj.vuln_id = finding.get("arn", "null")
        vuln_obj.severity = finding.get("severity", "null")
        vuln_obj.cvss_score = finding.get("attributes", {}).get("cvss", "null")
        vuln_obj.description = finding.get("description", "null")
        vuln_obj.resource_type = finding.get("resource", {}).get("type", "null")
        vuln_obj.resource_id = finding.get("resource", {}).get("id", "null")
        vuln_list.append(vuln_obj)

    return vuln_list

def process_findings_to_json(findings) -> str:
    """
    Converts findings to a formatted JSON string.
    """
    findings_detail = json.dumps(findings, indent=4)
    return findings_detail

def set_github_actions_output(name: str, value: str):
    """
    Sets the GitHub Actions output.
    """
    logging.info(f"Setting GitHub Actions output - {name}: {value}")
    print(f"::set-output name={name}::{value}")

def fatal_assert(expr: bool, msg: str):
    """
    Asserts a condition and logs an error message if the condition is not met.
    """
    if not expr:
        logging.error(msg)
        exit(1)
