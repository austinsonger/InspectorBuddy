# EC2 Vulnerability Scanfor Amazon Inspector (Plus Jira Intergration)

Amazon Inspector is a vulnerability management service that scans AWS workloads for known software vulnerabilities.

This GitHub Action allows you to scan EC2 instances for software vulnerabilities using Amazon Inspector from your GitHub Actions workflows. Both agent-based and agentless scans are supported. Additionally, this action can create Jira tickets for each new individual vulnerability detected.


## Overview
This action works by utilizing Amazon Inspector to scan specified EC2 instances for known vulnerabilities.

## Prerequisites

- Required: You must have an active AWS account to use this action. 
- Required: You must have read access to the InspectorScan API. 
- Required: You must configure AWS authentication for use in GitHub action workflows.
- Required: Create a GitHub Actions workflow if you do not already have one.
- Optional: Configure Jira authentication if you want to create Jira tickets for each new vulnerability. You need the Jira URL, Jira username, and Jira API token.

## Usage

### Quick Start

Perform the following steps to quickly add this action to your GitHub Actions pipeline:

```yaml
name: Scan EC2 Instances with Amazon Inspector
on: [push]
jobs:
 daily_job:
   runs-on: ubuntu-latest

   # change this to match your GitHub Secrets environment
   environment:
     name: your_github_secrets_environment

   steps:

     # modify this block based on how you authenticate to AWS
     # make sure you have permission to access the Inspector ScanEC2 API
     # https://docs.aws.amazon.com/inspector/latest/user/configure-cicd-account.html#cicd-iam-role
     - name: Configure AWS credentials
       uses: aws-actions/configure-aws-credentials@v4
       with:
         aws-region: "us-east-1"
         role-to-assume: "arn:aws:iam::<AWS_ACCOUNT_ID>:role/<IAM_ROLE_NAME>"

     # Check out your repository if needed
     - name: Checkout this repository
       uses: actions/checkout@v4

     # modify this block to scan your intended EC2 instances
     - name: Inspector Scan
       id: inspector
       uses: ./path/to/your/action
       with:
         aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
         aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
         aws-region: ${{ secrets.AWS_REGION }}
         assessment-run-arn: 'arn:aws:inspector:us-west-2:123456789012:assessment-run/assessment-run-id'
         agentless: true # Set to true to use agentless scans

         # Jira integration parameters (optional)
         jira-url: ${{ secrets.JIRA_URL }}
         jira-username: ${{ secrets.JIRA_USERNAME }}
         jira-api-token: ${{ secrets.JIRA_API_TOKEN }}
         jira-project-key: ${{ secrets.JIRA_PROJECT_KEY }}

         # If enabled, this setting will display Inspector's vulnerability scan findings
         # as a GitHub actions step summary. See here for an example step summary:
         # https://github.com/aws-actions/vulnerability-scan-github-action-for-amazon-inspector/actions/runs/8800085041
         display_vulnerability_findings: "enabled"

         # Set vulnerability thresholds; if the number of vulnerabilities is
         # equal to or greater than any of the specified thresholds, this
         # action will set the 'vulnerability_threshold_exceeded'
         # output flag to 1.
         critical_threshold: 1
         high_threshold: 1
         medium_threshold: 1
         low_threshold: 1
         other_threshold: 1

         # Additional input arguments are available to control scan behavior.
         # See 'action.yml' for additional input/output options.


     # The following steps illustrate how to
     # display scan results in the GitHub Actions job terminal.
     - name: Display Inspector vulnerability scan results (JSON)
       run: cat ${{ steps.inspector.outputs.inspector_scan_results }}

     - name: Display Inspector vulnerability scan results (CSV)
       run: cat ${{ steps.inspector.outputs.inspector_scan_results_csv }}

     - name: Display Inspector vulnerability scan results (Markdown)
       run: cat ${{ steps.inspector.outputs.inspector_scan_results_markdown }}


     # The following steps illustrate how to
     # upload scan results as a GitHub actions job artifact
     - name: Upload Scan Results
       uses: actions/upload-artifact@v4
       with:
         name: Inspector Vulnerability Scan Artifacts
         path: |
           ${{ steps.inspector.outputs.inspector_scan_results }}
           ${{ steps.inspector.outputs.inspector_scan_results_csv }}
           ${{ steps.inspector.outputs.inspector_scan_results_markdown }}

       # This step illustrates how to add custom logic if
       # the vulnerability threshold is exceeded. This example
       # simply prints the 'vulnerability_threshold_exceeded' value
       # to the GitHub actions job terminal.
       # Replace 'echo' with 'exit' if you want to fail the job.
     - name: On vulnerability threshold exceeded
       run: echo ${{ steps.inspector.outputs.vulnerability_threshold_exceeded }}

```



### Configuring Vulnerability Scan Outputs

By default, this action only displays the number of vulnerabilities detected in the GitHub Actions job terminal. Detailed findings are optional and configurable as JSON, CSV, or Markdown.

The below example shows how to enable action outputs in various locations and formats.

```yaml
- name: Scan EC2 instances
  id: inspector
  uses: ./path/to/your/action
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: ${{ secrets.AWS_REGION }}
    assessment-run-arn: 'arn:aws:inspector:us-west-2:123456789012:assessment-run/assessment-run-id'
    agentless: true
    display_vulnerability_findings: "enabled"

# Display Inspector results in the GitHub Actions terminal
- name: Display Inspector vulnerability scan results (JSON)
  run: cat ${{ steps.inspector.outputs.inspector_scan_results }}

- name: Display Inspector vulnerability scan results (CSV)
  run: cat ${{ steps.inspector.outputs.inspector_scan_results_csv }}

- name: Display Inspector vulnerability scan results (markdown)
  run: cat ${{ steps.inspector.outputs.inspector_scan_results_markdown }}


# Upload Inspector outputs as a .zip that can be downloaded
# from the GitHub actions job summary page.
- name: Upload Scan Results
  id: inspector
  uses: actions/upload-artifact@v4
  with:
    name: Inspector Vulnerability Scan Artifacts
    path: |
      ${{ steps.inspector.outputs.inspector_scan_results }}
      ${{ steps.inspector.outputs.inspector_scan_results_csv }}

```

### Configuring Vulnerability Thresholds

This action allows the user to set vulnerability thresholds.

Vulnerability thresholds can be used to support custom logic, such as failing the workflow if any vulnerabilities are found.

```yaml
- name: Invoke Amazon Inspector Scan
  id: inspector
  uses: ./path/to/your/action
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: ${{ secrets.AWS_REGION }}
    assessment-run-arn: 'arn:aws:inspector:us-west-2:123456789012:assessment-run/assessment-run-id'
    agentless: true
    display_vulnerability_findings: "enabled"

    # If the number of vulnerabilities equals or exceeds
    # any of the specified vulnerability thresholds, this action
    # sets a flag, 'vulnerability_threshold_exceeded' to 1, else 0.
    # To ignore thresholds for a given severity, set its value to 0.
    # This example sets 'vulnerability_threshold_exceeded' flag if
    # one or more criticals, highs, or medium severity vulnerabilities
    # are found; lows and other type vulnerabilities will not set
    # the 'vulnerability_threshold_exceeded' flag.
    critical_threshold: 1
    high_threshold: 1
    medium_threshold: 1
    low_threshold: 0
    other_threshold: 0

# Fail the job with 'exit 1' if vuln threshold flag is set
- name: On vulnerability threshold exceeded
  run: exit ${{ steps.inspector.outputs.vulnerability_threshold_exceeded }}

```


## Action Inputs and Outputs


### Input Options

| **Name**                       | **Description**                                              | **Required** | **Default** |
| ------------------------------ | ------------------------------------------------------------ | ------------ | ----------- |
| aws-access-key-id              | AWS Access Key ID for accessing Amazon Inspector             | True         | -           |
| aws-secret-access-key          | AWS Secret Access Key for accessing Amazon Inspector         | True         | -           |
| aws-region                     | AWS Region where your EC2 instances are located              | True         | -           |
| assessment-run-arn             | Amazon Inspector Assessment Run ARN                          | True         | -           |
| display_vulnerability_findings | If set to "enabled", the action will display detailed vulnerability findings in the action summary page | True         | disabled    |
| critical_threshold             | Specifies the number of critical vulnerabilities needed to set the 'vulnerability_threshold_exceeded' flag | False        | 0           |
| high_threshold                 | Specifies the number of high vulnerabilities needed to set the 'vulnerability_threshold_exceeded' flag | False        | 0           |
| medium_threshold               | Specifies the number of medium vulnerabilities needed to set the 'vulnerability_threshold_exceeded' flag | False        | 0           |
| low_threshold                  | Specifies the number of low vulnerabilities needed to set the 'vulnerability_threshold_exceeded' flag | False        | 0           |
| other_threshold                | Specifies the number of other vulnerabilities needed to set the 'vulnerability_threshold_exceeded' flag | False        | 0           |

### Output Options

| **Name**                         | **Description**                                              |
| -------------------------------- | ------------------------------------------------------------ |
| inspector_scan_results           | The file path to the Inspector vulnerability scan findings in JSON format |
| inspector_scan_results_csv       | The file path to the Inspector vulnerability scan findings in CSV format |
| inspector_scan_results_markdown  | The file path to the Inspector vulnerability scan findings in markdown format |
| vulnerability_threshold_exceeded | This variable is set to 1 if any vulnerability threshold was exceeded, otherwise it is 0. This variable can be used to trigger custom logic, such as failing the job if vulnerabilities were detected |










