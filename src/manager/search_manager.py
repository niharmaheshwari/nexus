import boto3
from pprint import pprint
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import manager.constants as constants
from model.snippet_snapshot import SnippetSnapshot

class SearchManager():

    def __init__(self):
        creds = boto3.Session(constants.ACCESS_KEY, constants.SECRET_KEY, 
        region_name=constants.REGION).get_credentials()

        awsauth = AWS4Auth(creds.access_key, creds.secret_key, constants.REGION, 
        constants.SERVICE, session_token=creds.token)
        
        '''Connect to es'''
        self._es = OpenSearch(['https://search-code-snippets-x7pez2uta5ofjf4sch7o63dd2y.us-east-2.es.amazonaws.com/'],
                http_auth=awsauth, use_ssl = True, verify_certs=True, connection_class=RequestsHttpConnection)
        
 
    def search_by_tags(self, tags, user) -> list[SnippetSnapshot]:
        '''
        Search es for exact tag matches.  All returned snippets will have 
        at least one matching tag from tags

        Inputs: tags = Array of strings . example ['python', 'binary search']
                user = example 'user1' 
        Returns: list of snippetSnapshots

        '''
        # TODO: should also search lang? 
        '''build search query for es'''
        query = {"query" : {
                "terms" : {
                    "tags.keyword" : tags
                }
            }
        }

        '''search es using query in index user'''
        response = self._es.search(
            body = query,
            index = user
        )

        '''deserialize es response to list of SnippetSnapshots'''
        return self.es_result_to_snippet_snapshots(response) 

        
    
    def search_by_string(self, search_string, user) -> list[SnippetSnapshot]: 
        '''
        General search: search through tags and description using a search string

        Inputs: search_string = "python code that searches a list quickly"
                user = example 'user2' 
        Returns: list of snippetSnapshots that match the search_string in either tags, desc, or lang fields
        '''

        #TODO: do we want this to be fuzzy? 
        query = {"query" : {
                "multi_match" : {
                    "query": search_string,
                    "fields": ["tags", "desc", "lang"]
                }
            }
        }

        response = self._es.search(
            body = query,
            index = user
        )
       
        return self.es_result_to_snippet_snapshots(response)
    
    def es_result_to_snippet_snapshots(self, response) -> list[SnippetSnapshot]: 
        '''deserialize es response to list of SnippetSnapshots'''
        result = response['hits']['hits']
        snippet_list = []
        for item in result:
            s = SnippetSnapshot()
            s.id = item['_source']['id']
            s.desc = item['_source']['desc']
            s.tags = item['_source']['tags']
            s.lang = item['_source']['lang']
            snippet_list.append(s)   
        return snippet_list

