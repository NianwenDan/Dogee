import logging
import src.config as config

def setup_logger():
    '''
    Setup logger configuration
    '''
    LOG_LEVEL = logging.ERROR

    if config.LOG_LEVEL == 'INFO':
        LOG_LEVEL = logging.INFO
    elif config.LOG_LEVEL == 'DEBUG':
        LOG_LEVEL = logging.DEBUG

    # Create a logger
    logger = logging.getLogger('Dogee')
    logger.setLevel(LOG_LEVEL)  # Set the logging level based on global variable

    # Create a file handler which logs even debug messages
    fh = logging.FileHandler(config.LOG_SAVEPATH, mode='a')
    fh.setLevel(LOG_LEVEL)  # Set the logging level for the file handler

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(LOG_LEVEL)  # Set the logging level for the console handler

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s %(name)s:%(levelname)s:%(message)s', datefmt='%m-%d-%Y %H:%M:%S')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger

def new(level: str, *msg: list) -> None:
    '''
    Write new log to console and file

    :param level: debug, info, warning, error, critical
    :param msg: log message
    '''
    # Turn off logs
    if config.LOG_LEVEL == 'OFF':
        return

    logger = setup_logger()

    full_msg = ''
    for i in msg:
        full_msg += str(i) + ' '

    if level == 'debug':
        logger.debug(full_msg)
    elif level == 'info':
        logger.info(full_msg)
    elif level == 'warning':
        logger.warning(full_msg)
    elif level == 'error':
        logger.error(full_msg)
    elif level == 'critical':
        logger.critical(full_msg)
    else:
        print('Incorrect Log Level')