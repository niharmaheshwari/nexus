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
        self._db_client = boto3.resource('dynamodb', aws_access_key_id="AKIAVYPI7GZ6X3S4WW6Y", aws_secret_access_key="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",region_name='us-east-2')
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
        batch_keys = {
        self._table.name: {
        'Keys': [{'id': id} for id in snippet_ids]
        }}

        response = self._db_client.batch_get_item(RequestItems=batch_keys)['Responses']['snippets']
        #TODO: change this to a list of snippets and return the response?
        '''
        [{'file': 's3-url', 'user_shared': [], 'audit': {'created_at': '2021-11-09 21:36:31.497460', 'last_update': '2021-11-09 21:36:31.497443'}, 
        'id': 'user2-snippit-1', 'tags': ['python', 'binary search'], 'author': 'user2', 'desc': ['find upper bound using binary search']}, 
        {'file': 's3-url', 'user_shared': [], 'audit': {'created_at': '2021-11-12 13:49:57.204840', 'last_update': '2021-11-12 13:49:57.204829'}, 
        'id': 'user1-snippit-4', 'tags': ['python', 'binary search'], 'author': 'user1', 'desc': ['perform binary search']}]
        '''


       
    
s = SnippetManager()
print(s.get_snippets(['user1-snippit-4','user2-snippit-1']))
