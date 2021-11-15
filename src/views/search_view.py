'''Search View'''
import json
from flask import (Blueprint, request, jsonify)
from src.manager.search_manager import SearchManager
from src.manager.snippet_manager import SnippetManager
from src.manager.user_manager import UserManager
from src.utilities.authorization import authorization
from src.utils.utils import CustomJSONEncoder
from src.model.message_format import MessageFormat

search = Blueprint('search', __name__, url_prefix='/search')

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

    search_manager = SearchManager()
    snippet_manager = SnippetManager()
    user_manager = UserManager()

    #Get user details
    user_response = user_manager.get_user_details(email)
    if user_response["data"] is None:
        return jsonify(user_response)
    user = user_response["data"]["user"]

    # Search es for the SnippetSnapshots corresponding to search string
    snippet_snapshots = search_manager.search_by_string(search_string, user)
    if snippet_snapshots == []:
        return jsonify(MessageFormat().success_message(data={"snippets":[]}))

    # Extract IDs from SnippetSnapshots
    ids = []
    for snapshot in snippet_snapshots:
        ids.append(snapshot.id)

    # Search dynamo for list of Snippets
    snippets_response = snippet_manager.get_snippets(ids)
    if snippets_response["error"] is True:
        return jsonify(snippets_response)
    snippets = snippets_response["data"]

    # Serialize Snippets to JSON
    results = json.dumps({"snippets":snippets},cls=CustomJSONEncoder)

    return jsonify(MessageFormat().success_message(data=results))
    