'''Search View'''
import json
from flask import (Blueprint, request)
from flask.wrappers import Response
from src.manager.search_manager import SearchManager
from src.manager.snippet_manager import SnippetManager
from src.manager.user_manager import UserManager
from src.utilities.authorization import authorization
from src.utils.utils import CustomJSONEncoder

search = Blueprint('search', __name__, url_prefix='/search')

@search.route('/tags', methods=['POST'])
def search_tag():
    '''
    The body will be a json object {tags: ["python", "binary_search"]}
    Exact matches for the tags will be searched for
    '''

    tags = request.json['tags']
    search_manager = SearchManager()
    snippet_manager = SnippetManager()

    # TODO : update getting the user to a real function call
    user = 'user2'
    snippet_snapshots = search_manager.search_by_tags(tags, user)

    ids = []
    for snapshot in snippet_snapshots:
        ids.append(snapshot.snippet_id())

    snippets = snippet_manager.get_snippets(ids)

    results = json.dumps({"snippets":snippets},cls=CustomJSONEncoder)

    return Response(results, status=200, content_type="application/json")

    # TODO: error handling

@search.route('/', methods=['POST'])
@authorization
def search_general():
    '''
    The body will be a json object {"search_string": "looking for a python string", "email":"talyakosch@gmail.com"}
    Matching will be applied to tags, description, and lang fields

    '''
    search_string = request.json['search_string']
    email = request.json['email']
    search_manager = SearchManager()
    snippet_manager = SnippetManager()
    user_manager = UserManager()

    token = request.headers.get("token", None)
    user = user_manager.get_user_details(token, email)

    # Search es for the SnippetSnapshots corresponding to search string
    snippet_snapshots = search_manager.search_by_string(search_string, user)

    # Extract IDs from SnippetSnapshots
    ids = []
    for snapshot in snippet_snapshots:
        ids.append(snapshot.id)

    # Search dynamo for list of Snippets
    snippets = snippet_manager.get_snippets(ids)

    # Serialize Snippets to JSON
    results = json.dumps({"snippets":snippets},cls=CustomJSONEncoder)

    return Response(results, status=200, content_type="application/json")

    # TODO: error handling
