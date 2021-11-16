'''
Snippet Snapshot Manager
'''
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from src.constants.secrets import ACCESS_KEY, SECRET_KEY
from src.constants.constants import AWS_REGION, ELASTIC_SEARCH, ES_SERVICE
from src.model.snippet_snapshot import SnippetSnapshot

class SnippetSnapshotManager():
    '''
    Builder class for SnippetSnapshot
    '''

    def __init__(self):
        creds = boto3.Session(ACCESS_KEY, SECRET_KEY,
        region_name=AWS_REGION).get_credentials()
        awsauth = AWS4Auth(creds.access_key, creds.secret_key, AWS_REGION,
        ES_SERVICE, session_token=creds.token)

        # connect to ES
        self._es = OpenSearch([ELASTIC_SEARCH],http_auth=awsauth, use_ssl = True,
        verify_certs=True, connection_class=RequestsHttpConnection)

    def search_by_string(self, search_string, email) -> list:
        '''
        General search: search through tags and description using a search string

        Inputs: search_string = "python code to do binary search"
                user = example "user2"
        Returns: list of snippetSnapshots that match the search_string in either tags,
         desc, or lang fields
        '''

        # compose query for ES
        query = {"query" : {
                "multi_match" : {
                    "query": search_string,
                    "fields": ["tags", "desc", "lang"]
                }
            }
        }

        # search using query
        response = self._es.search(
            body = query,
            index = email
        )

       # deserialized response to list of snippetSnapshots
        return SnippetSnapshotManager.es_result_to_snippet_snapshots(response)

    def match_all(self):
        '''
        Returns all information in es database, for testing purposes
        '''
        query = {"query" : {
                "match_all" : {}
            }
        }

        response = self._es.search(
            body = query,
        )

        return response

    @staticmethod
    def es_result_to_snippet_snapshots(response):
        '''deserialize es response to list of snippetSnapshots'''

        result = response['hits']['hits']
        snippet_list = []
        for item in result:
            snippet_id = item['_source']['id']
            desc = item['_source']['desc']
            tags = item['_source']['tags']
            lang = item['_source']['lang']
            snapshot= SnippetSnapshot(snippet_id, tags, desc, lang)
            snippet_list.append(snapshot)
        return snippet_list

