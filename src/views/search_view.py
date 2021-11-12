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

    tags = json.loads(request.json)['tags']
    search_manager = SearchManager()
    snippet_manager = SnippetManager()


    # TODO : figure out how you know what user is using the service and update this
    user = 'fake_user'
    snippet_snapshots = search_manager.search_by_tags(tags, user)

    rsp = []

    # TODO: maybe have a method in snippet manager that allows you to get many snippets by a list of IDs?
    for snapshot in snippet_snapshots: 
        id = snapshot.snippet_id()
        snippet = snippet_manager.get_sinppet(id)
        rsp.append(snippet)
    
    # TODO: serialize array of snippets to json, return it? Figure out format we want for response
    # TODO: error handling

@search.route('/', methods=['POST'])
def search_general():
    '''The body will be a json object {"search_string": "looking for a python string"}'''
    '''fuzzy matching on the search string will be applied to both tags and description'''

    search_string = json.loads(request.json)['search_string']
    search_manager = SearchManager()
    snippet_manager = SnippetManager()

    # TODO : figure out how you know what user is using the service and update this
    user = 'fake_user'
    snippet_snapshots = search_manager.search_by_string(search_string, user)

    rsp = []

    for snapshot in snippet_snapshots: 
        id = snapshot.snippet_id()
        snippet = snippet_manager.get_sinppet(id)
        rsp.append(snippet)
    
    # TODO: serialize array of snippets to json, return it? Figure out format we want for response
    # TODO: error handling









