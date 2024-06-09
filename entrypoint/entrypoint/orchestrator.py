import logging

from .cli import init
from .installer import prepare_environment
from .executor import invoke_command
from .pkg_vuln import parse_vulns, create_jira_tickets

def run_scan():
    args = init()

    if not prepare_environment(args.aws_access_key_id, args.aws_secret_access_key, args.aws_region):
        logging.error("Environment preparation failed.")
        return

    # Adjust the command based on agentless or agent-based scan
    if args.agentless:
        cmd = ['aws', 'inspector2', 'start-assessment', '--resource-group-arn', args.assessment_run_arn, '--agentless']
    else:
        cmd = ['aws', 'inspector2', 'start-assessment', '--resource-group-arn', args.assessment_run_arn]

    result_code = invoke_command(cmd[0], cmd[1:])
    
    if result_code != 0:
        logging.error(f"Scan command failed with exit code {result_code}.")
    else:
        logging.info("Scan command executed successfully.")
        
        # Read scan results
        with open('inspector_scan_results.json', 'r') as file:
            inspector_scan_json = file.read()
        
        # Parse vulnerabilities
        vulnerabilities = parse_vulns(inspector_scan_json)
        
        # Create Jira tickets if Jira parameters are provided
        if args.jira_url and args.jira_username and args.jira_api_token and args.jira_project_key:
            create_jira_tickets(args.jira_url, args.jira_username, args.jira_api_token, args.jira_project_key, vulnerabilities)
