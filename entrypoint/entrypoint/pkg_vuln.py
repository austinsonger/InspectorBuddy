import json
import logging
import requests
from typing import List

class Vulnerability:
    """
    Vulnerability is an object for marshalling vulnerability findings
    from Inspector's JSON into a Python object that can be queried and manipulated.
    """
    def __init__(self):
        self.vuln_id = "null"
        self.severity = "null"
        self.description = "null"
        self.resource_type = "null"
        self.resource_id = "null"

def get_json_value(key: str, inspector_scan_json: dict):
    value = inspector_scan_json.get(key)
    return value

def get_json_value_or_throw_fatal_error(key: str, inspector_scan_json: dict):
    value = get_json_value(key, inspector_scan_json)
    if not value:
        logging.fatal(f"expected JSON with key '{key}' but it was not found")
    return value

def get_inspector_scan_body(inspector_scan_json):
    scan_json = json.loads(inspector_scan_json)
    scan_body = get_json_value("findings", scan_json)
    if not scan_body:
        logging.fatal("expected JSON with key 'findings' but none was found")
    return scan_body

def parse_vulns(inspector_scan_json: str) -> List[Vulnerability]:
    scan_body = get_inspector_scan_body(inspector_scan_json)
    vulnerabilities = []

    for finding in scan_body:
        vuln = Vulnerability()
        vuln.vuln_id = finding.get("arn", "null")
        vuln.severity = finding.get("severity", "null")
        vuln.description = finding.get("description", "null")
        vuln.resource_type = finding.get("resource", {}).get("type", "null")
        vuln.resource_id = finding.get("resource", {}).get("id", "null")
        vulnerabilities.append(vuln)

    return vulnerabilities

def generate_csv_report(vulnerabilities: List[Vulnerability]) -> str:
    csv_output = "ID,SEVERITY,DESCRIPTION,RESOURCE_TYPE,RESOURCE_ID\n"

    for vuln in vulnerabilities:
        clean_description = vuln.description.replace(',', '')
        csv_row = f"{vuln.vuln_id},{vuln.severity},{clean_description},{vuln.resource_type},{vuln.resource_id}\n"
        csv_output += csv_row

    return csv_output

def write_csv_report(inspector_scan_path: str, dst_file: str) -> bool:
    with open(inspector_scan_path, 'r') as file:
        inspector_scan_json = file.read()

    vulnerabilities = parse_vulns(inspector_scan_json)
    if not vulnerabilities:
        logging.info("No vulnerabilities found, skipping CSV report")
        return False

    csv_output = generate_csv_report(vulnerabilities)
    logging.info(f"Writing vulnerability CSV report to: {dst_file}")
    with open(dst_file, "w") as file:
        file.write(csv_output)

    return True

def create_jira_ticket(jira_url, jira_username, jira_api_token, jira_project_key, vulnerability):
    """
    Creates a Jira ticket for a given vulnerability.
    :param jira_url: Jira URL
    :param jira_username: Jira Username
    :param jira_api_token: Jira API Token
    :param jira_project_key: Jira Project Key
    :param vulnerability: Vulnerability object
    :return: Response from Jira API
    """
    url = f"{jira_url}/rest/api/2/issue"
    headers = {
        "Content-Type": "application/json"
    }
    auth = (jira_username, jira_api_token)
    payload = {
        "fields": {
            "project": {
                "key": jira_project_key
            },
            "summary": f"Vulnerability: {vulnerability.vuln_id} - {vulnerability.severity}",
            "description": f"{vulnerability.description}\n\nResource Type: {vulnerability.resource_type}\nResource ID: {vulnerability.resource_id}",
            "issuetype": {
                "name": "Bug"
            }
        }
    }

    response = requests.post(url, headers=headers, auth=auth, json=payload)

    if response.status_code == 201:
        logging.info(f"Successfully created Jira ticket for vulnerability {vulnerability.vuln_id}")
    else:
        logging.error(f"Failed to create Jira ticket for vulnerability {vulnerability.vuln_id}: {response.text}")

    return response

def create_jira_tickets(jira_url, jira_username, jira_api_token, jira_project_key, vulnerabilities: List[Vulnerability]):
    """
    Creates Jira tickets for a list of vulnerabilities.
    :param jira_url: Jira URL
    :param jira_username: Jira Username
    :param jira_api_token: Jira API Token
    :param jira_project_key: Jira Project Key
    :param vulnerabilities: List of Vulnerability objects
    """
    for vulnerability in vulnerabilities:
        create_jira_ticket(jira_url, jira_username, jira_api_token, jira_project_key, vulnerability)
