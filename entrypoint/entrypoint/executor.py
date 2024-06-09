import subprocess
import logging

def invoke_command(bin, args) -> int:
    """
    Invokes a command and streams its output in real-time.
    :param bin: The binary to execute
    :param args: A list of arguments for the binary
    :return: The exit code of the command
    """
    cmd = [bin] + args
    logging.info(f"Executing command: {' '.join(cmd)}")
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    
    rc = process.poll()
    return rc
