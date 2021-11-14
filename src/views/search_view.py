'''Search View'''
import json
from flask import (jsonify, Blueprint, request)
from flask.wrappers import Response
from manager.search_manager import SearchManager
from manager.snippet_manager import SnippetManager

search = Blueprint('search', __name__, url_prefix='/search')

@search.route('/tags', methods=['POST'])
def search_tag():
    '''The body will be a json object {tags: ["python", "binary_search"]}'''
    '''Exact matches for the tags will be searched for'''

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

    results = json.dumps({"snippets":snippets},cls=MyEncoder)

    return Response(results, status=200, content_type="application/json")

    # TODO: error handling

@search.route('/', methods=['POST'])
def search_general():
    '''
    The body will be a json object {"search_string": "looking for a python string"}
    Matching will be applied to tags, description, and lang fields

    '''
    search_string = request.json['search_string']
    search_manager = SearchManager()
    snippet_manager = SnippetManager()

    # TODO : update getting the user with real function call 
    user = 'user2'

    '''Search es for the SnippetSnapshots corresponding to search string'''
    snippet_snapshots = search_manager.search_by_string(search_string, user)

    '''Extract IDs from SnippetSnapshots'''
    ids = []
    for snapshot in snippet_snapshots: 
        ids.append(snapshot.id)
    
    '''Search dynamo for list of Snippets'''
    snippets = snippet_manager.get_snippets(ids)

    '''Serialize Snippets to JSON'''
    results = json.dumps({"snippets":snippets},cls=MyEncoder)

    return Response(results, status=200, content_type="application/json")
    
    # TODO: error handling

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return {k.lstrip('_'): v for k, v in vars(o).items()}






