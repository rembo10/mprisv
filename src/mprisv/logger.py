import logging

logging.basicConfig(level=logging.INFO)

def get_log(name):
    log = logging.getLogger(name)
    return log
