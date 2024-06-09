import argparse

def init(sys_argv=None) -> argparse.Namespace:
    """
    Initializes the CLI using argparse.
    :param sys_argv: A list of arguments; you should pass sys.argv in most cases.
    Alternatively, you can provide custom values for use in unit tests.
    :return: namespace containing values for each CLI key
    """
    program_description = "Fetch Amazon Inspector EC2 scan results."
    parser = argparse.ArgumentParser(description=program_description)

    parser.add_argument('--aws-access-key-id', type=str, required=True,
                        help='AWS Access Key ID')
    parser.add_argument('--aws-secret-access-key', type=str, required=True,
                        help='AWS Secret Access Key')
    parser.add_argument('--aws-region', type=str, required=True,
                        help='AWS Region')
    parser.add_argument('--assessment-run-arn', type=str, required=True,
                        help='Amazon Inspector Assessment Run ARN')
    parser.add_argument('--agentless', action='store_true', help='Use agentless scan')
    parser.add_argument('--jira-url', type=str, help='Jira URL')
    parser.add_argument('--jira-username', type=str, help='Jira Username')
    parser.add_argument('--jira-api-token', type=str, help='Jira API Token')
    parser.add_argument('--jira-project-key', type=str, help='Jira Project Key')

    args = parser.parse_args(sys_argv) if sys_argv else parser.parse_args()
    
    return args
