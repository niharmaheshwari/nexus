''' Snippet View '''
from flask import (request, abort, Blueprint)

snippet = Blueprint('snippet', __name__, url_prefix='/snippet')

def fetch_snippet():
    '''Handler to fetch snippet from DB'''

def create_snippet():
    '''Handler to create snippet in DB'''

def update_snippet():
    '''Handler to update snippet from DB'''

def remove_snippet():
    '''Handler to remove Snippet from DB'''

@snippet.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def snippet_ops():
    '''Snippet Operations'''
    handler_map = {
        'GET': fetch_snippet,
        'POST': create_snippet,
        'PUT': update_snippet,
        'DELETE': remove_snippet
    }
    try:
        args = {}
        return handler_map[request.method](args)
    except KeyError:
        return abort(405, description='Method not defined')
