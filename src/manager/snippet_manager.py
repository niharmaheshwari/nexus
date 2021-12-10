'''
Snippet Manager
'''
import json
import boto3
import datetime
import uuid
from boto3.dynamodb.conditions import Key
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import src.constants.constants as const
import src.utilities.logging as log
from src.model.snippet import Snippet
from src.model.snippet_snapshot import SnippetSnapshot
from src.manager.user_manager import UserManager
from src.utilities.snippet_utils import merge_snippet
from src.model.snippet import Snippet
from src.model.audit import Audit
from src.model.message_format import MessageFormat
from src.constants.constants import AWS_REGION, SNIPPET_TABLE
from src.constants.secrets import ACCESS_KEY, SECRET_ACCESS_KEY

logging = log.get_logger(__name__)

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

    def __init__(self, *args, **kwargs):
        '''
        Restrict s3 client and table. These should be initialized once and not modified
        '''

        self._session = kwargs.get('session',boto3.Session(
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_ACCESS_KEY,
        ))
        self._db_client = kwargs.get('db_client', self._session.resource(const.DB, region_name=const.AWS_REGION))
        self._table = kwargs.get('table', self._db_client.Table(const.SNIPPET_TABLE))
        self._fs = kwargs.get('fs', self._session.client(const.FILE_SYSTEM))
        self._user = kwargs.get('user', UserManager())
        self._creds = kwargs.get('creds', self._session.get_credentials())
        self._awsauth = kwargs.get('awsauth', AWS4Auth(
            self._creds.access_key,
            self._creds.secret_key,
            const.AWS_REGION,
            'es',
            session_token=self._creds.token
        ))
        self._es = kwargs.get('es', OpenSearch(
            hosts = [const.ELASTIC_SEARCH],
            http_auth = self._awsauth,
            use_ssl = True,
            verify_certs = True,
            connection_class = RequestsHttpConnection
        ))

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

    def get_snippet(self, id, token):
        '''
        Get a snippet from DB given a snippet ID.
        If a snippet ID is not passed, fetch all snippets for a specific user. Note that this
        fetches even those sinppets which are shared with the user.
        :params:
            snippet_id: ID for the snipped to be fetched (Optional)
            token: Token for the user
        :returns:
            result: A single Snippet OR a list of Snippets
            validation: The list of validation errors in input. None if input is correct
        '''
        # Return Values
        result = []
        validation = []

        try:
            user_details = self.user.get_user_details(token=token)
        except Exception as user_undef:
            logging.error('Unable to obtain user details from token. Error: %s', user_undef)
            validation.append('Unable to obtain user details from token')
            # If there are no user details found, there is no point in moving forward. Return here.
            return result, validation


        if id is None or len(id) == 0:
            try:
                table_res = []
                # Hack - Since the current Dynamo Table version does not support non-index queries,
                # Use SCAN to fetch the entire table in memory and then filter in code.
                logging.info('Table Result : %s', str(table_res))
                table_res.extend(self.table.scan()['Items'])
                logging.info('Table Result : %s', str(table_res))
                for res in table_res:
                    snippet = Snippet.to_snippet(res)
                    if snippet.author == user_details['data']['user'].email:
                        result.append(snippet)
                    elif (
                        snippet.shares is not None and
                        len(snippet.shares) > 0 and
                        user_details['data']['user'].email in snippet.shares
                    ):
                        result.append(snippet)

            except Exception as query_error:
                logging.error('There was an error while fetching multiple snippets from the DB')
                logging.error('Error: %s', query_error)
                validation.append('Error fetching snippets from the database')
            return result, validation
        else:
            try:
                result.append(Snippet.to_snippet(self.table.query(
                    KeyConditionExpression = Key('id').eq(id)
                )['Items'][0]))
                logging.info('Snippet Obtained : %s', result)
            except Exception as query_error:
                logging.error('There was an error while fetching a snippet. Error: %s', query_error)
                validation.append('Error fetching the snippet from the database')
            return result, validation

    def create_snippet(self, snippet_raw, file_data, token):
        '''
        Create a new snippet and return it along with an ID
        :params:
            snippet     : Metadata of the new snippet to be created. This is a Snippet() partial
            file_data   : Code content which the user uploads
            token       : Token for the user
        :returns:
            snippet     : The newly created snippet
            validation  : Validation errors on the input, if any.
        '''
        snippet = Snippet()
        validation = []
        try:
            snippet_raw = json.loads(snippet_raw)
        except Exception as parse_error:
            logging.error('There was an error parsing the request body. Error: %s', parse_error)
            validation.append('There was an error parsing the request body')
            # There is no point moving forward from here. Return here
            return snippet, validation

        try:
            user_details = self.user.get_user_details(token)
            logging.info('User is : %s', user_details )
            snippet.author = user_details['data']['user'].email
        except Exception as user_fail:
            logging.error('There was an error while getting the user details. Error: %s', user_fail)
            validation.append('There was an error fetching user information')

        try:
            snippet.lang = LANG_EXTENTION[file_data.filename.split('.')[-1]]
        except Exception as lang_miss:
            logging.error('Uploaded file is missing the language extension. Error: %s', lang_miss)
            validation.append('Uploaded file is missing the language extension')

        try:
            snippet.audit = {
                'last_upd_date': datetime.datetime.utcnow().isoformat(),
                'last_upd_user': snippet.author,
                'creation_date': datetime.datetime.utcnow().isoformat(),
                'creation_user': snippet.author
            }
        except Exception as audit_fail:
            logging.error('An error occured while setting the audit. Error: %s', audit_fail)
            validation.append('An error occured while setting the audit on the snippet')

        try:
            snippet.desc = snippet_raw['desc'] if 'desc' in snippet_raw else ''
        except Exception as desc_fail:
            logging.error('An error occured while setting the description. Error: %s', desc_fail)
            validation.append('An error occured while setting the description')

        try:
            snippet.id = str(uuid.uuid1())
        except Exception as id_fail:
            logging.error('Exception occured while setting the id. Error: %s', id_fail)
            validation.append('Exception while assigning a UUID to a snippet')

        try:
            snippet.tags = snippet_raw['tags'] if 'tags' in snippet_raw else ''
        except Exception as tag_fail:
            logging.error('Exception occured while setting tags. Error: %s', tag_fail)
            validation.append('Exception while setting tags')

        try:
            snippet.uri = const.S3 + snippet.id
        except Exception as uri_fail:
            logging.error('Exception occured while setting the file name and location on S3')
            logging.error('Full Error: %s', uri_fail)
            validation.append('Exception while setting the S3 URI')

        try:
            logging.info('Adding snippet to the S3 location')
            # Storing files with the id of the snippet in S3. This is to prevent write clashes for
            # multiple files with the same name.
            f = self._fs.upload_fileobj(file_data,const.BUCKET,snippet.id, ExtraArgs = {
                'ContentType': 'text/plain'
            })
        except Exception as upload_fail:
            logging.error('S3 Upload Failed. Error: %s', upload_fail)
            validation.append('S3 Upload Failed')
            # There is no benefit to continue from here. Return here
            return snippet, validation

        try:
            self.table.put_item(Item=snippet.to_dict(), ReturnValues='ALL_OLD')
        except Exception as table_exception:
            logging.error('Could not add Snippet to Dynamo. Error: %s', table_exception)
            validation.append('Could not add snippet to DynamoDB')

        try:
            snapshot = SnippetSnapshot(
                snippit_id=snippet.id,
                tags=snippet.tags,
                desc=snippet.desc,
                lang=snippet.lang
            )
            self.es.index(
                index = snippet.author, 
                doc_type = 'snippet', 
                body = snapshot.to_dict(),
                id=snippet.id
            )
        except Exception as elastic_fail:
            logging.error('There was an exception while adding the snippet to elastic')
            logging.error('Full Error: %s', elastic_fail)
            logging.error('Performing an emergency rollback on DynamoDB')
            self.table.delete_item(Key={'id': snippet.id})
            validation.append('Failed to add Snippet to Elastic. Did an emergency rollback on DynamoDB')

        return snippet, validation

    def update_snippet(self, snippet_raw, file_data, token):
        '''
        Updates an existing snippet and returns the new metadata pertaining to the snippet.
        :params:
            snippet     : Metadata of the new snippet to be created. This is a Snippet() partial
            file_data   : Code content which the user uploads
            token       : Token for the user
        :returns:
            snippet     : The newly created snippet
            validation  : Validation errors on the input, if any.
        '''
        snippet = Snippet()
        validation = []
        try:
            snippet_raw = json.loads(snippet_raw)
            snippet.id = snippet_raw['id']
        except Exception as parse_error:
            logging.error('There was an error parsing the request body. Error: %s', parse_error)
            validation.append('There was an error parsing the request body')
            # There is no point moving forward from here. Return here
            return snippet, validation

        try:
            # Unlike the CREATE method, do NOT assign the token holder as the author. The update
            # might be from a share list member.
            user_details = self.user.get_user_details(token)
            logging.info('User is : %s', user_details )
            snippet.author = user_details['data']['user'].email
        except Exception as user_fail:
            logging.error('There was an error while getting the user details. Error: %s', user_fail)
            validation.append('There was an error fetching user information')

        try:
            if file_data is not None:
                snippet.lang = LANG_EXTENTION[file_data.filename.split('.')[-1]]
        except Exception as lang_miss:
            logging.error('Uploaded file is missing the language extension. Error: %s', lang_miss)
            validation.append('Uploaded file is missing the language extension')

        try:
            snippet.audit = {
                'last_upd_date': datetime.datetime.utcnow().isoformat(),
                'last_upd_user': user_details['data']['user'].email,
                'creation_date': datetime.datetime.utcnow().isoformat(),
                'creation_user': snippet.author
            }
        except Exception as audit_fail:
            logging.error('An error occured while setting the audit. Error: %s', audit_fail)
            validation.append('An error occured while setting the audit on the snippet')

        try:
            snippet.desc = snippet_raw['desc'] if 'desc' in snippet_raw else ''
        except Exception as desc_fail:
            logging.error('An error occured while setting the description. Error: %s', desc_fail)
            validation.append('An error occured while setting the description')

        try:
            snippet.tags = snippet_raw['tags'] if 'tags' in snippet_raw else ''
        except Exception as tag_fail:
            logging.error('Exception occured while setting tags. Error: %s', tag_fail)
            validation.append('Exception while setting tags')

        try:
            snippet.uri = const.S3 + snippet.id
        except Exception as uri_fail:
            logging.error('Exception occured while setting the file name and location on S3')
            logging.error('Full Error: %s', uri_fail)
            validation.append('Exception while setting the S3 URI')

        try:
            logging.info('Adding snippet to the S3 location')
            # Storing files with the id of the snippet in S3. This is to prevent write clashes for
            # multiple files with the same name.
            if file_data is not None:
                f = self._fs.upload_fileobj(file_data,const.BUCKET,snippet.id, ExtraArgs = {
                    'ContentType': 'text/plain'
                })
        except Exception as upload_fail:
            logging.error('S3 Upload Failed. Error: %s', upload_fail)
            validation.append('S3 Upload Failed')
            # There is no benefit to continue from here. Return here
            return snippet, validation

        try:
            self.table.put_item(Item=snippet.to_dict(), ReturnValues='ALL_OLD')
        except Exception as table_exception:
            logging.error('Could not add Snippet to Dynamo. Error: %s', table_exception)
            validation.append('Could not add snippet to DynamoDB')

        try:
            snapshot = SnippetSnapshot(
                snippit_id=snippet.id,
                tags=snippet.tags,
                desc=snippet.desc,
                lang=snippet.lang
            )
            self.es.delete(
                index= snippet_raw['email'],
                id= snippet_raw['id']
            )
            self.es.index(
                index = snippet_raw['email'], 
                doc_type = 'snippet',
                id=snippet.id,
                body = snapshot.to_dict()
            )
        except Exception as elastic_fail:
            logging.error('There was an exception while adding the snippet to elastic')
            logging.error('Full Error: %s', elastic_fail)
            logging.warn('There are inconsitencies between S3 / Dynamo / Elastic. Please check')

        return snippet, validation

    def delete_snippet(self, id, token):
        '''
        Delete the snippet if it exists.
        :params:
            id          : The identifier for the snippet to be deleted
            token       : Token for the user
        :returns:
            result      : Boolean result of the delete operation.
            validation  : Validation errors on the input, if any.
        '''
        result, validation = False, []

        try:
            result, validation = self.get_snippet(id=id, token=token)
        except Exception as fetch_fail:
            logging.error('Failed to fetch the existing Snippet from the DB. Error: %s', fetch_fail)
            logging.error('This snippet does not exist or is corrupt to delete')
            validation.append('This snippet does not exist or is corrupt to delete')
            return result, validation

        try:
            user_details = self.user.get_user_details(token)
            logging.info('User is : %s', user_details )
        except Exception as user_fail:
            logging.error('There was an error while getting the user details. Error: %s', user_fail)
            validation.append('There was an error fetching user information')

        try:
            result[0].uri = const.S3 + result[0].id
            self.fs.delete_object(Bucket=const.BUCKET, Key=result[0].uri)
        except Exception as uri_fail:
            logging.error('Exception occured while removing the file from S3')
            logging.error('Full Error: %s', uri_fail)
            validation.append('Exception while setting the S3 URI')

        try:
            self.table.delete_item(Key={'id': id})
        except Exception as table_exception:
            logging.error('Could not remove Snippet from Dynamo. Error: %s', table_exception)
            validation.append('Could not remove snippet from DynamoDB')

        try:
            snapshot = SnippetSnapshot(
                snippit_id=result[0].id,
                tags=result[0].tags,
                desc=result[0].desc,
                lang=result[0].lang
            )
            self.es.delete(
                index= result[0].author,
                id= result[0].id
            )
        except Exception as elastic_fail:
            logging.error('There was an exception while adding deleting the snippet from elastic')
            logging.error('Full Error: %s', elastic_fail)
            logging.warn('There are inconsitencies between S3 / Dynamo / Elastic. Please check')

        return result[0], validation
    
    def get_snippet_headless(self, snippet_id):
        '''
        Get a snippet from DB given a snippet ID
        Arguments
            snipped_id: ID for the snipped to be fetched
        '''
        snippet = Snippet()
        try:
            snippet = Snippet.to_snippet(self.table.query(
                KeyConditionExpression = Key('id').eq(snippet_id)
            )['Items'][0])
            logging.info(f'Snippet Obtained : {snippet}')
        except Exception as key_error:
            logging.error(f'Key: {snippet_id} does not exist in the database. Full Error : {key_error}')
            snippet = None
        return snippet

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

            audit = Audit(last_upd_date, last_upd_user, creation_date, creation_user)
            snippet = Snippet()
            snippet.id = item['id']
            snippet.uri = item['uri']
            snippet.desc = item['desc']
            snippet.tags = item['tags']
            snippet.author = item['author']
            snippet.shares = item['shares']
            snippet.audit = audit
            snippet.lang = item['lang']
            snippets_list.append(snippet)

        return snippets_list


