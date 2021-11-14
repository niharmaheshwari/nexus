'''
Snippet Manager
'''
import boto3
from pprint import pprint

from model.snippet import Snippet
from model.audit import Audit
from views.snippet_view import snippet_ops
import manager.constants as constants

class SnippetManager():
    '''
    Builder class for Snippets
    '''

    def __init__(self):
        '''
        Restrict s3 client and table. These should be initialized once and not modified
        '''
        self._db_client = boto3.resource('dynamodb', aws_access_key_id= constants.ACCESS_KEY, aws_secret_access_key=constants.SECRET_KEY,region_name=constants.REGION)
        self._table = self._db_client.Table('snippets')

    @property
    def table(self):
        '''Getter for Table'''
        return self._table

    def get_sinppet(self, snippet_id):
        '''
        Get a snippet from DB given a snippet ID
        Arguments
            snipped_id: ID for the snipped to be fetched
        '''

    def update_snipped(self, modified_snippet):
        '''
        Update an existing Snippet
        Arguments
            modified_snippet : The modified snippet
        '''

    def create_snippet(self, snippet):
        '''
        Create a new snippet and return it along with an ID
        Arguments:
            snippet : New snippet to be created
        '''

    def delete_snippet(self, snippet_id):
        '''
        Delete Snippet from DynamoDB
        Arguments
            id : ID for the snippet to be deleted
        '''

    def get_snippets(self, snippet_ids):
        '''
        Get multiple snippets from DynamoDB
        Arguments
            snippet__ids: array of ids to fetch
        Returns
            list of Snippets
        
        '''
        # TODO : error handling 

        '''Search snippets table for multiple ids'''
        batch_keys = {
        self._table.name: {
        'Keys': [{'id': id} for id in snippet_ids]
        }}

        response = self._db_client.batch_get_item(RequestItems=batch_keys)

        '''return a list of Snippets'''
        return self.dynamo_response_to_snippets(response)

    def dynamo_response_to_snippets(self, response):
        '''
        deserialize the dynamo response to a list of Snippets
        '''
        json_snippets_list = response['Responses']['snippets']
        snippets_list = []
        for item in json_snippets_list: 
            a = Audit()
            s = Snippet()
            audit = item['audit']

            a.last_upd_user = audit['last_upd_user']
            a.creation_date = audit['creation_date']
            a.last_upd_date = audit['last_upd_date']
            a.creation_user = audit['creation_user']

            s.audit = audit
            s.uri = item['uri']
            s.id = item['id']
            s.tags = item['tags']
            s.shares = item['shares']
            s.author = item['author']
            s.lang = item['lang']
            s.desc = item['desc']

            snippets_list.append(s)
        
        return snippets_list

