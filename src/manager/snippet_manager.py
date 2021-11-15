'''
Snippet Manager
'''
import boto3
from boto3.dynamodb.conditions import Key
import logging
import flask
import json
import constants.constants as const
from model.snippet import Snippet
from model.snippet_snapshot import SnippetSnapshot
from manager.user_manager import UserManager
import datetime
import uuid
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from utilities.snippet_utils import merge_snippet

LANG_EXTENTION = {
    'py': 'Python',
    'java': 'Java',
    'cpp': 'C++',
    'sh': 'Shell'
}


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
            logging.info(f'Snippet Obtained : {snippet}')
        except Exception as key_error:
            logging.error(f'Key: {id} does not exist in the database. Full Error : {key_error}')
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
            snippet_raw = json.load(snippet_raw)
            # 1. Get User
            # TODO : Try using the real auth module after getting the new master auth
            #user_details = self.user.get_user_details(snippet_raw['email'])
            snippet.author = 'nihar-maheshwari'#user_details.name

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
            f = self._fs.upload_fileobj(file_data,const.BUCKET,file_data.filename)

            # 9. Add metadata to Dynamo
            self.table.put_item(Item= snippet.to_dict(), ReturnValues='ALL_OLD')

            # 10. Index in Elastic
            snapshot = SnippetSnapshot(
                snippit_id=snippet.id,
                tags=snippet.tags,
                desc=snippet.desc,
                lang=snippet.lang
            )
            # TODO : Put the real user here. I dont have permission
            # self.es.index(index = 'nihar-maheshwari', doc_type = '_doc', id = snapshot.id, body = snapshot.to_dict())

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
            # TODO : Try using the real auth module after getting the new master auth
            #user_details = self.user.get_user_details(snippet_raw['email'])
            snippet.author = 'nihar-maheshwari'#user_details.name

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
                f = self._fs.upload_fileobj(file_data,const.BUCKET,file_data.filename)

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
            # self.es.delete(index = 'user', id = snapshot.id)
            # self.es.index(index = 'user', doc_type = '_doc', id = snapshot.id, body = snapshot.to_dict())

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

