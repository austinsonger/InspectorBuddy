import json
import logging
from entrypoint.pkg_vuln import Vulnerability, vulns_to_obj, fatal_assert

def validate_scan_results(scan_results_json):
    findings = json.loads(scan_results_json)
    vulnerabilities = vulns_to_obj(findings)
    
    if not vulnerabilities:
        logging.error("No vulnerabilities found in the scan results.")
        return False
    
    for vuln in vulnerabilities:
        logging.info(f"Vulnerability found: {vuln.vuln_id} - {vuln.severity} - {vuln.description}")
    
    return True

def main():
    import sys
    if len(sys.argv) != 2:
        logging.error("Usage: validate_inspector_scan.py <scan_results_json>")
        sys.exit(1)
    
    scan_results_json = sys.argv[1]
    is_valid = validate_scan_results(scan_results_json)
    fatal_assert(is_valid, "Validation failed.")

if __name__ == "__main__":
    main()
