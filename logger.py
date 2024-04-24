import logging
from logging import Handler
from logging.handlers import RotatingFileHandler

class SpaceHandler(Handler):
    def emit(self, record):
        print()  # Print a newline to insert space between log messages

def setup_logger(log_file):
    # Create a logger
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    # Create a formatter for regular log messages
    ### Print as Time (YYYY-MM-DD h:m:s, millisecond) - Severity Level - Log Message
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create a console handler for logging
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Create a custom console handler for adding space between logs
    space_handler = SpaceHandler()
    logger.addHandler(space_handler)

    # Create a file handler and set level to DEBUG
    fh = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2)  # 5MB file size, 2 backup files
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger