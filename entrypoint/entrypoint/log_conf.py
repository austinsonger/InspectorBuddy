import logging

class LogFormatter(logging.Formatter):
    def format(self, record):
        """
        Formats console logs following this pattern:
        time="2024-06-09 12:00:00" level=info msg="This is an info log" file="example.py:10"
        """
        log_time = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        log_level = record.levelname.lower()
        log_msg = record.getMessage()
        log_file = f'{record.filename}:{record.lineno}'
        formatted_log = f'time="{log_time}" level={log_level} msg="{log_msg}" file="{log_file}"'
        return formatted_log

def init(enable_verbose: bool):
    """
    Configures the system's log level and format.
    :param enable_verbose: if true, set the log level to DEBUG, else INFO
    """
    logger = logging.getLogger()
    handler = logging.StreamHandler()

    if enable_verbose:
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        handler.setLevel(logging.INFO)

    handler.setFormatter(LogFormatter())
    logger.addHandler(handler)
