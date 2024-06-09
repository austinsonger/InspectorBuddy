import logging
import os
import subprocess

def configure_aws_cli(aws_access_key_id: str, aws_secret_access_key: str, aws_region: str) -> bool:
    """
    Configures the AWS CLI with provided credentials and region.
    :param aws_access_key_id: AWS Access Key ID
    :param aws_secret_access_key: AWS Secret Access Key
    :param aws_region: AWS Region
    :return: True if configuration is successful, False otherwise
    """
    try:
        subprocess.run(['aws', 'configure', 'set', 'aws_access_key_id', aws_access_key_id], check=True)
        subprocess.run(['aws', 'configure', 'set', 'aws_secret_access_key', aws_secret_access_key], check=True)
        subprocess.run(['aws', 'configure', 'set', 'region', aws_region], check=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to configure AWS CLI: {e}")
        return False

def verify_aws_cli() -> bool:
    """
    Verifies that the AWS CLI is installed and configured correctly.
    :return: True if AWS CLI is installed and configured, False otherwise
    """
    try:
        result = subprocess.run(['aws', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            logging.info(f"AWS CLI version: {result.stdout.strip()}")
            return True
        else:
            logging.error(f"AWS CLI not found or not configured properly: {result.stderr.strip()}")
            return False
    except Exception as e:
        logging.error(f"Error verifying AWS CLI: {e}")
        return False

def prepare_environment(aws_access_key_id: str, aws_secret_access_key: str, aws_region: str) -> bool:
    """
    Prepares the environment for running AWS Inspector scans.
    :param aws_access_key_id: AWS Access Key ID
    :param aws_secret_access_key: AWS Secret Access Key
    :param aws_region: AWS Region
    :return: True if environment is prepared successfully, False otherwise
    """
    if not verify_aws_cli():
        logging.error("AWS CLI is not installed or configured properly.")
        return False
    
    if not configure_aws_cli(aws_access_key_id, aws_secret_access_key, aws_region):
        logging.error("Failed to configure AWS CLI with provided credentials and region.")
        return False
    
    return True
