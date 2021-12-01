''' Snippet View '''
from copy import Error
import logging
from flask import (Blueprint, Response, request)
from src.manager.snippet_manager import SnippetManager
from src.model.message_format import MessageFormat
from src.utilities.authorization import authorization

snippet_blueprint = Blueprint('snippet', __name__, url_prefix='/api/snippet')
mgr = SnippetManager()


def fetch_snippet(inflight_request):
    '''
    Fetch a snippet given it's ID. Throw a 404 if snippet does not exist
    Arguments:
        request : Attributes from the session request
    '''
    snippet_id = inflight_request.args.get('id')
    snippet = mgr.get_snippet(snippet_id)
    if snippet is not None:
        return MessageFormat().success_message(data=snippet.to_dict())
    return Response(MessageFormat().error_message('Snippet not found in database', 404), 404)

def create_snippet(inflight_request):
    '''
    Create a new request signed by the uploader. Note that the body and the file both are
    required in this call.
    Arguments:
        request : Attributes from the session request
    '''
    snippet = None
    try:    
        body = inflight_request.form['data']
        file = inflight_request.files['file']
        snippet = mgr.create_snippet(body, file)
    except KeyError as e:
        logging.error('The metadata or file was missing. Full error : %s', e)

    if snippet is not None:
        return MessageFormat().success_message(data = snippet.to_dict())
    return Response(MessageFormat().error_message('Bad Request', 400),400)

def update_snippet(inflight_request):
    '''
    Update an existing request signed by the uploader. Note that only the body is mandatory here
    Arguments:
        request : Attributes from the session request
    '''
    snippet = None
    try:
        body = inflight_request.form['data']
        file = inflight_request.files['file'] if 'file' in inflight_request.files else None
        snippet = mgr.update_snippet(body, file)
    except KeyError as e:
        logging.error('The metadata was missing for updating the snippet. Full error %s' , e)

    if snippet is not None:
        return MessageFormat().success_message(data = snippet.to_dict())
    return Response(MessageFormat().error_message('Bad Request', 400), 400)

def remove_snippet(inflight_request):
    '''
    Delete a snippet from the user store. Note that although the snippet metadata is removed,
    the snippet is still maintained in S3 as a history.
    Arguments:
        request : Attributes from the session request
    '''
    snippet_id = inflight_request.args.get('id')
    try:
        mgr.delete_snippet(snippet_id)
        return MessageFormat().success_message(data = {})
    except Error:
        return Response(MessageFormat().error_message('Bad Request. Key does not exist', 400),400)

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
        return Response(MessageFormat().error_message('Method not defined', 405), 405)
