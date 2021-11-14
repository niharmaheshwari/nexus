'''Main Module'''
import  logging
import  argparse
from    flask              import Flask
from    views.snippet_view import snippet
from    views.test_view    import test
from    views.search_view  import search

# Global APP Name
NAME = 'NEXUS'

# Set global root logging context
ROOT = logging.getLogger()

# Support the following logging levels
LOG_LEVELS = {
    'CRITICAL' : logging.CRITICAL,
    'FATAL'    : logging.FATAL,
    'ERROR'    : logging.ERROR,
    'WARNING'  : logging.WARNING,
    'INFO'     : logging.INFO,
    'DEBUG'    : logging.DEBUG,
    'NOTSET'   : logging.NOTSET
}

def register():
    '''
    Description:
        Register the flask application
    Parameters:
        -
    Returns:
        the flask application context
    '''
    app = Flask(NAME)
    app.register_blueprint(snippet)
    app.register_blueprint(test)
    app.register_blueprint(search)
    return app

def init_log(log_level = logging.INFO):
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
    if ROOT.handlers:
        for handler in ROOT.handlers:
            ROOT.removeHandler(handler)
    logging.basicConfig(format='%(asctime)s %(message)s',level=log_level)

def parse_args():
    '''
    Description
        Parse arguments sent in the startup script
    Paramteres
        Arguments sent from the startup initialization context
    Returns
        Default or user defined parameter values
    '''
    parser = argparse.ArgumentParser(description='Spin up the nexus flask server')
    parser.add_argument(
        '-d', '--debug',choices=['True','False'],default='False',
        help='Specify the debug mode for flask.'
    )
    parser.add_argument(
        '-l','--log',
        choices=['CRITICAL','FATAL','ERROR','WARNING','INFO','DEBUG','NOTSET'],
        default='INFO',help='Specify the logging level for the application'
    )
    parser.add_argument(
        '-s','--server',default='127.0.0.1',
        help='Specify the host address on which the Flask app is deployed'
    )
    parser.add_argument(
        '-p','--port',default= 5000,
        help='Specify the port on which should serve the flask application'
    )
    arguments = parser.parse_args()
    arguments.debug = arguments.debug == 'True'
    arguments.log = LOG_LEVELS[arguments.log]
    return arguments


if __name__ == '__main__':
    args = parse_args()
    init_log(args.log)
    logging.info('Starting the flask server with the following arguments:')
    logging.info('Flask Debugging: %s', format(args.debug))
    logging.info('Log Level: %s', logging.getLevelName(args.log))
    register().run(debug=args.debug, host=args.server, port=args.port)
