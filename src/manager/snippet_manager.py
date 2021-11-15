'''
Snippet Manager
'''
import boto3

from src.model.snippet import Snippet
from src.model.audit import Audit
from src.model.message_format import MessageFormat
from src.views.snippet_view import snippet_ops
from src.constants.secrets import ACCESS_KEY, SECRET_KEY
from src.constants.constants import AWS_REGION, SNIPPET_TABLE

# pylint: disable=broad-except
class SnippetManager():
    '''
    Builder class for Snippets
    '''

    def __init__(self):
        '''
        Restrict s3 client and table. These should be initialized once and not modified
        '''
        self._db_client = boto3.resource('dynamodb', aws_access_key_id= ACCESS_KEY, aws_secret_access_key=SECRET_KEY,region_name=AWS_REGION)
        self._table = self._db_client.Table(SNIPPET_TABLE)

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
            Message with data =list of Snippets
        
        ''' 

        # Search snippets table for multiple ids
        try:
            batch_keys = {
            self._table.name: {
            'Keys': [{'id': id} for id in snippet_ids]
            }}
            response = self._db_client.batch_get_item(RequestItems=batch_keys)
        except Exception as err:
            return MessageFormat().error_message(str(err))

        # return a list of snippets
        return MessageFormat().success_message(data=SnippetManager.dynamo_response_to_snippets(response))

    @staticmethod
    def dynamo_response_to_snippets(response):
        '''
        deserialize the dynamo response to a list of Snippets
        '''
        snippets_list = []
        for item in response['Responses']['snippets']:

            last_upd_user = item['audit']['last_upd_user']
            creation_date = item['audit']['creation_date']
            last_upd_date = item['audit']['last_upd_date']
            creation_user = item['audit']['creation_user']
            uri = item['uri']
            snippet_id = item['id']
            tags = item['tags']
            shares = item['shares']
            author = item['author']
            lang = item['lang']
            desc = item['desc']

            audit = Audit(last_upd_date, last_upd_user, creation_date, creation_user)
            snippets_list.append(Snippet(uri, desc, snippet_id, tags, author, shares, audit, lang))
        
        return snippets_list

