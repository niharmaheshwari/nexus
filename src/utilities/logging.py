'''
General purpose logging utility
'''
from functools import wraps
from flask import request
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
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'\
                                                                    ,level=log_level)

def get_logger(module_name, log_level = logging.INFO):
    '''
    Utility to get the global logger
    Arguments:
        module_name: str, the name of the module in which the logger
        object is created.
        log_level : Parameter that sets the global logging level
    '''
    # Set global root logging context
    root = logging.getLogger().getChild(module_name)
    init_log(root, log_level)
    return logging.getLogger()

def logger(func):
    """
    Decorator function for printing inital log statements
    about any REST call.
    """
    @wraps(func)
    def default_logger(*args, **kwargs):
        """
        Wrapper logger function for printing initial logging
        statements. Prints the method, url, headers and body
        of the request.
        """
        log = get_logger(module_name=__name__)
        log.info("http method: %s", request.method)
        log.info("request url: %s", request.url )
        log.info("request headers: %s", request.headers)
        log.info("request body: %s", request.get_json())
        return func(*args, **kwargs)
    return default_logger
