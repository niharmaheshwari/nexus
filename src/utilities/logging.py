'''
General purpose logging utility
'''
import logging

LOG_LEVELS = {
    'CRITICAL' : logging.CRITICAL,
    'FATAL'    : logging.FATAL,
    'ERROR'    : logging.ERROR,
    'WARNING'  : logging.WARNING,
    'INFO'     : logging.INFO,
    'DEBUG'    : logging.DEBUG,
    'NOTSET'   : logging.NOTSET
}

def get_level_name(level):
    '''
    Wrapper to execute the getLevelName for the logging module
    Arguments:
        level : logging level (integer)
    '''
    return logging.getLevelName(level)

def init_log(root, log_level = logging.INFO):
    '''
    Description
        Set the logging context.
    Note
        If deploying on a container / lambda, ensure that there are no handlers associated to the
        logging context (to prevent log messages from being supressed)
    Parameters
        default_level : Expects a log level. Default is INFO
    Returns
        -
    '''
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',level=log_level)

def get_logger(log_level = logging.INFO):
    '''
    Utility to get the global logger
    Arguments:
        log_level : Parameter that sets the global logging level
    '''
    # Set global root logging context
    root = logging.getLogger()
    init_log(root, log_level)
    return logging.getLogger()
