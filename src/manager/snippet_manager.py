'''
Snippet Manager
'''
import boto3

class SnippetManager():
    '''
    Builder class for Snippets
    '''

    def __init__(self):
        '''
        Restrict s3 client and table. These should be initialized once and not modified
        '''
        self._db_client = boto3.resource('dynamodb', region_name='us-east-1')
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
