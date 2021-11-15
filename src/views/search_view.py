'''Search View'''
from flask import (Blueprint, request, jsonify)
from src.manager.search_manager import SearchManager
from src.utilities.authorization import authorization
from src.model.message_format import MessageFormat

search = Blueprint('search', __name__, url_prefix='/search')

search_manager = SearchManager()

@search.route('/', methods=['POST'])
@authorization
def search_general():
    '''
    The body will be a json object:
    {"search_string": "looking for a python string", "email":"tom@gmail.com"}
    Matching will be applied to tags, description, and lang fields
    '''
    # Extract POST body parameters
    try:
        search_string = request.json['search_string']
        email = request.json['email']
    except KeyError:
        msg = "key error: body should contain search_string, email"
        return jsonify(MessageFormat().error_message(msg))
    rsp = search_manager.search_general(search_string, email)
    return jsonify(rsp)


    