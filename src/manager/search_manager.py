import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import constants
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
        '''Search es for exact tag matches.  All returned snippets will have 
            at least one matching tag from tags

            Inputs: tags = Array of strings . example ['python', 'binary search']
                    user = example 'user1' 
            Returns: list of snippetSnapshots

        '''
        query = {"query" : {
                "terms" : {
                    "tags.keyword" : tags
                }
            }
        }

        response = self._es.search(
            body = query,
            index = user
        )

        # TODO: deserialize the response into an array of snippetSnapshots
        return response['hits']['hits'] 

        
    
    def search_by_string(self, search_string, user) -> list[SnippetSnapshot]: 
        '''General search: search through tags and description using 
            a search string

            Inputs: search_string = "python code that searches a list quickly"
                    user = example 'user2' 
            Returns: list of snippetSnapshots that match the search_string 
        '''

        #TODO: do we want this to be fuzzy? 
        query = {"query" : {
                "multi_match" : {
                    "query": search_string,
                    "fields": ["tags", "desc"]
                }
            }
        }

        response = self._es.search(
            body = query,
            index = user
        )

        # TODO: deserialize the response into an array of snippetSnapshots
        return response['hits']['hits']

    

                
