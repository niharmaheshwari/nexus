'''Main Module'''
import argparse
from flask import Flask
import logging
from src.views.snippet_view import snippet_blueprint
from src.views.test_view import test
from src.views.authentication import auth
from src.views.dummy_view import dummy
from src.views.search_view import search
import src.constants.constants as const

logger = logging.getLogger()

levels = {
    'CRITICAL': logging.CRITICAL,
    'FATAL': logging.FATAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET
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
    app = Flask(const.NAME)
    app.register_blueprint(snippet_blueprint)
    app.register_blueprint(test)
    app.register_blueprint(search)
    app.register_blueprint(auth)
    app.register_blueprint(dummy)
    return app

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
    arguments.log = levels[arguments.log]
    return arguments


if __name__ == '__main__':
    args = parse_args()
    logger.info('Starting the flask server with the following arguments:')
    logger.info('Flask Debugging: %s', format(args.debug))
    logger.info('Log Level: %s', logging.getLevelName(args.log))
    register().run(debug=args.debug, host=args.server, port=args.port)
