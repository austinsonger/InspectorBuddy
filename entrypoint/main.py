#!/usr/bin/env python3

import sys
import boto3
from entrypoint import cli, installer, log_conf, orchestrator

def main():
    # Initialize CLI arguments
    args = cli.init(sys.argv[1:])

    # Initialize logger
    log_conf.init(enable_verbose=True)

    # Prepare the environment
    if not installer.prepare_environment(args.aws_access_key_id, args.aws_secret_access_key, args.aws_region):
        sys.exit(1)

    # Execute the main orchestration
    ret = orchestrator.execute(args)
    sys.exit(ret)

if __name__ == '__main__':
    main()
