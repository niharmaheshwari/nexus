'''lint View'''
from src.manager.linting import linting_manager
from flask import (Blueprint, Response, jsonify)
from src.manager.snippet_manager import SnippetManager
from src.utilities.authorization import authorization
from src.utilities.logging import logger

lint = Blueprint('lint', __name__, url_prefix='/api/lint')
manager = SnippetManager()

@lint.route('/<snippet_id>', methods=['GET'])
@authorization
@logger
def get_lint_output(snippet_id):
    '''
    Given a snippet ID, run a linter, return the output
    '''
    rsp, err = linting_manager.get_lint_output(snippet_id)
    if err is not None:
        return jsonify(err)
    return Response(rsp,status=200, content_type='text/plain')
