'''
Snippet Manager
'''
import logging
import json
import boto3
import datetime
import uuid
from boto3.dynamodb.conditions import Key
import flask
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import src.constants.constants as const
from src.model.snippet import Snippet
from src.model.snippet_snapshot import SnippetSnapshot
from src.manager.user_manager import UserManager
from src.utilities.snippet_utils import merge_snippet
from src.model.snippet import Snippet
from src.model.audit import Audit
from src.model.message_format import MessageFormat
from src.constants.constants import AWS_REGION, SNIPPET_TABLE

LANG_EXTENTION = {
    'py': 'Python',
    'java': 'Java',
    'cpp': 'C++',
    'sh': 'Shell'
}

# pylint: disable=broad-except
class SnippetManager():
    '''
    Builder class for Snippets
    '''

    def __init__(self):
        '''
        Restrict s3 client and table. These should be initialized once and not modified
        '''
        self._db_client = boto3.resource(const.DB, region_name=const.AWS_REGION)
        self._table = self._db_client.Table(const.SNIPPET_TABLE)
        self._fs = boto3.client(const.FILE_SYSTEM)
        self._user = UserManager()
        self._creds = boto3.Session().get_credentials()
        self._awsauth = AWS4Auth(
            self._creds.access_key,
            self._creds.secret_key,
            const.AWS_REGION,
            'es',
            session_token=self._creds.token
        )
        self._es = OpenSearch(
            hosts = [const.ELASTIC_SEARCH],
            http_auth = self._awsauth,
            use_ssl = True,
            verify_certs = True,
            connection_class = RequestsHttpConnection
        )

    @property
    def table(self):
        '''Getter for Table'''
        return self._table

    @property
    def fs(self):
        '''Getter for File System'''
        return self._fs

    @property
    def user(self):
        '''Getter for the user manager'''
        return self._user

    @property
    def es(self):
        '''Getter for elastic client'''
        return self._es

    def get_snippet(self, id):
        '''
        Get a snippet from DB given a snippet ID
        Arguments
            snipped_id: ID for the snipped to be fetched
        '''
        snippet = Snippet()
        try:
            snippet = Snippet.to_snippet(self.table.query(
                KeyConditionExpression = Key('id').eq(id)
            )['Items'][0])
            logging.info('Snippet Obtained : %s', snippet)
        except Exception as key_error:
            logging.error('Key: %s does not exist in the database. Full Error : %s', id, key_error)
            snippet = None
        return snippet

    def create_snippet(self, snippet_raw, file_data):
        '''
        Create a new snippet and return it along with an ID
        Arguments:
            snippet     : Metadata of the new snippet to be created. This is a Snippet() partial
            file_data   : Code content which the user uploads
        '''
        snippet = Snippet()
        try:
            # Construct Snippet() from the parital
            snippet_raw = json.loads(snippet_raw)
            # 1. Get User
            user_details = self.user.get_user_details(snippet_raw['email'])
            logging.info('User is : %s', user_details )
            snippet.author = user_details['data']['user'].name

            # 2. Infer Language
            snippet.lang = LANG_EXTENTION[file_data.filename.split('.')[-1]]

            # 3. Set the audit
            snippet.audit = {
                'last_upd_date': datetime.datetime.utcnow().isoformat(),
                'last_upd_user': snippet.author,
                'creation_date': datetime.datetime.utcnow().isoformat(),
                'creation_user': snippet.author
            }

            # 4. Pick the description if it exists
            snippet.desc = snippet_raw['desc'] if 'desc' in snippet_raw else ''

            # 5. Generate a UUID
            snippet.id = str(uuid.uuid1())

            # 6. Pick tags if they exist
            snippet.tags = snippet_raw['tags'] if 'tags' in snippet_raw else ''

            # 7. Generate S3 URI
            snippet.uri = const.S3 + file_data.filename

            # 8. Attempt to add Snippet to S3
            logging.info('Adding snippet to the S3 location')
            f = self._fs.upload_fileobj(file_data,const.BUCKET,file_data.filename, ExtraArgs = {
                'ContentType': 'text/plain'
            })

            # 9. Add metadata to Dynamo
            self.table.put_item(Item= snippet.to_dict(), ReturnValues='ALL_OLD')

            # 10. Index in Elastic
            snapshot = SnippetSnapshot(
                snippit_id=snippet.id,
                tags=snippet.tags,
                desc=snippet.desc,
                lang=snippet.lang
            )

            self.es.index(index = snippet_raw['email'], doc_type = 'snippet', body = snapshot.to_dict())

        except Exception as e:
            logging.error('There was an exception during upload.')

            if 'email' not in snippet_raw:
                logging.error('Email id field missing from the data sent in the request')

            if (
                file_data is None or
                '.' not in file_data.filename or
                file_data.filename.split('.')[-1] not in LANG_EXTENTION
            ):
                logging.error('The file is either corrupt or the extension is not supported')

            if snippet is None:
                logging.error('There was an issue persisting to Dynamo / S3 / Elastic')

            raise e

        return snippet

    def update_snippet(self, snippet_raw, file_data):
        '''
        Create a new snippet and return it along with an ID
        Arguments:
            snippet_raw : Raw data for the new snippet
            file_data   : Optionally the new code file
        '''
        snippet_raw = json.load(snippet_raw)
        snippet = Snippet()
        snippet.id = snippet_raw['id']
        try:
            # Construct Snippet() from the parital
            # 1. Get User
            user_details = self.user.get_user_details(snippet_raw['email'])
            logging.info('User is : %s', user_details )
            snippet.author = user_details['data']['user'].name

            # 2. Infer Language
            snippet.lang = LANG_EXTENTION[file_data.filename.split('.')[-1]] if file_data else None

            # 3. Set the audit
            snippet.audit = {
                'last_upd_date': datetime.datetime.utcnow().isoformat(),
                'last_upd_user': snippet.author
            }

            # 4. Pick the description if it exists
            snippet.desc = snippet_raw['desc'] if 'desc' in snippet_raw else None

            # 6. Pick tags if they exist
            snippet.tags = snippet_raw['tags'] if 'tags' in snippet_raw else None

            # 7. Generate S3 URI
            snippet.uri = (const.S3 + file_data.filename) if file_data else None

            # 8. Attempt to add Snippet to S3
            logging.info('Adding snippet to the S3 location')
            if file_data:
                f = self._fs.upload_fileobj(file_data,const.BUCKET,file_data.filename, ExtraArgs = {
                'ContentType': 'text/plain'
            })

            # 9. Add metadata to Dynamo
            snippet = merge_snippet(self.get_snippet(snippet.id), snippet)
            self.table.put_item(Item=snippet.to_dict(), ReturnValues='ALL_OLD')

            # 10. Index in Elastic
            snapshot = SnippetSnapshot(
                snippit_id=snippet.id,
                tags=snippet.tags,
                desc=snippet.desc,
                lang=snippet.lang
            )
            # TODO : Put the real user here. I dont have permission
            self.es.index(index = snippet_raw['email'], doc_type = 'snippet', id = snapshot.id, body = snapshot.to_dict())

        except Exception as e:
            logging.error('There was an exception during upload.')

            if 'email' not in snippet_raw:
                logging.error('Email id field missing from the data sent in the request')

            if (
                file_data is None or
                '.' not in file_data.filename or
                file_data.filename.split('.')[-1] not in LANG_EXTENTION
            ):
                logging.error('The file is either corrupt or the extension is not supported')

            if snippet is None:
                logging.error('There was an issue persisting to Dynamo / S3 / Elastic')

            raise e

        return snippet

    def delete_snippet(self, id):
        '''
        Delete Snippet from DynamoDB
        Arguments
            id : ID for the snippet to be deleted
        '''
        # TODO : Test this after getting access to elastic
        res = self.table.delete_item(Key={'id': id})
        #self.es.delete(index = 'user', id = id)
        return

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
            snippet = Snippet()
            snippet.id = snippet_id
            snippet.uri = uri
            snippet.desc = desc
            snippet.tags = tags
            snippet.author = author
            snippet.shares = shares
            snippet.audit = audit
            snippet.lang = lang
            snippets_list.append(snippet)

        return snippets_list

