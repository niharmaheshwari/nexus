''' Snippet View '''
from copy import Error
import logging
from flask import (Blueprint, request)
from src.manager.snippet_manager import SnippetManager
from src.model.message_format import MessageFormat
from src.utilities.authorization import authorization

snippet_blueprint = Blueprint('snippet', __name__, url_prefix='/api/snippet')
mgr = SnippetManager()

INTERNAL_SERVER_ERROR = 'Internal Server Error!'

def fetch_snippet(inflight_request):
    '''
    Fetch a snippet given it's ID. This endpoint tries to fetch all the snippets under a specific
    user if the ID argument is missing. 
    :params:
        inflight_request : Inflight request object containing all parameters.
    :returns:
        JSONified view of the Snippet(s)
    '''
    snippet_id = inflight_request.args.get('id')
    id_token = inflight_request.headers.get("token", None)
    snippets, validation = mgr.get_snippet(snippet_id, id_token)

    if validation is not None and len(validation) > 0:
        return MessageFormat().error_message(str(validation), 400)
    if snippets is not None:
        if len(snippets) == 1:
            return MessageFormat().success_message(data=snippets[0].to_dict())
        else:
            return MessageFormat().success_message(data=list(map(lambda x: x.to_dict(), snippets)))
    return MessageFormat().error_message(INTERNAL_SERVER_ERROR, 500)

def create_snippet(inflight_request):
    '''
    Create a new snippet from the input file and the metadata. Note both metadata and the file are
    mandatory in this call.
    :params:
        inflight_request : Inflight request object containing metadata and file
    '''
    snippet, validation = None, None
    try:    
        body = inflight_request.form['data']
        file = inflight_request.files['file']
        id_token = inflight_request.headers.get("token", None)
        snippet, validation = mgr.create_snippet(body, file, id_token)
    except KeyError as e:
        logging.error('The metadata or file was missing. Full error : %s', e)
    if validation is not None and len(validation) > 0:
        return MessageFormat().error_message(str(validation), 400)
    if snippet is not None:
        logging.error('Snippet : %s', str(snippet))
        return MessageFormat().success_message(data=snippet.to_dict())
    return MessageFormat().error_message(INTERNAL_SERVER_ERROR, 500)

def update_snippet(inflight_request):
    '''
    Update an existing request signed by the uploader. Note that only the body is mandatory here
    :params:
        inflight_request : Attributes from the session request
    '''
    snippet, validation = None, None
    try:
        body = inflight_request.form['data']
        file = inflight_request.files['file'] if 'file' in inflight_request.files else None
        id_token = request.headers.get("token", None)
        snippet, validation = mgr.update_snippet(body, file, id_token)
    except KeyError as e:
        logging.error('The metadata was missing for updating the snippet. Full error %s' , e)
    if validation is not None and len(validation) > 0:
        return MessageFormat().error_message(validation, 400)
    if snippet is not None:
        return MessageFormat().success_message(data = snippet.to_dict())
    return MessageFormat().error_message(INTERNAL_SERVER_ERROR, 500)

def remove_snippet(inflight_request):
    '''
    Delete a snippet from the user store. This removes the snippet from 3 locations: S3, Dynamo and
    elastic.
    :params:
        inflight_request : Attributes from the session request
    '''
    snippet_id = inflight_request.args.get('id')
    id_token = inflight_request.headers.get("token", None)
    result, validation = None, None
    try:
        result, validation = mgr.delete_snippet(snippet_id, id_token)
    except Error as e:
        logging.error('There was an error while executing a delete. Error: %s', e)
    if validation is not None and len(validation) > 0:
        return MessageFormat().error_message(validation, 400)
    if result is not None:
        # If everything is fine, return the dict view of the Snippet for the last time
        return MessageFormat().success_message(data=result.to_dict())
    return MessageFormat.error_message(INTERNAL_SERVER_ERROR, 500)

@snippet_blueprint.route('', methods=['GET', 'POST', 'PUT', 'DELETE'])
@authorization
def snippet_ops():
    '''Snippet Operations'''
    handler_map = {
        'GET': fetch_snippet,
        'POST': create_snippet,
        'PUT': update_snippet,
        'DELETE': remove_snippet
    }
    try:
        logging.info('Incoming %s Request with arguments : %s', request.method, request.args)
        resp = handler_map[request.method](request)
        logging.info('Completed execution of %s with arguments : %s', request.method, request.args)
        return resp
    except KeyError:
        return MessageFormat().error_message('Method not defined', 405)
