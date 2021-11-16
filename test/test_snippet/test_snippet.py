'''
Test cases for Snippet CRUD Services
'''
from datetime import datetime
import unittest
from unittest.mock import MagicMock
from botocore.stub import Stubber
from werkzeug.datastructures import FileStorage
from src.manager.snippet_manager import SnippetManager
from src.manager.user_manager import UserManager

class TestSnippetView(unittest.TestCase):
    """
    Test class for Snippet related CRUD Services
    """
    def setUp(self):
        self.snippet_manager = SnippetManager()
        self.stub_table = Stubber(self.snippet_manager.table.meta.client)
        self.stub_fs = Stubber(self.snippet_manager.fs)
        self.user = UserManager()
        self.user.stubber = Stubber(self.user.cognito_client)
        self.stub_creds = Stubber(self.snippet_manager._creds)

    # Get flow
    def test_get_snippet_success(self):
        '''
        Test fetching of the Snippet Metadata
        '''
        arg_id = 'user1-snippit-1'
        self.stub_table.add_response(
            'query',
            {"Items": [{"id": {"S": "user1-snippit-1"}}]}
        )
        self.stub_table.activate()
        resp = self.snippet_manager.get_snippet(arg_id)
        self.assertIsNotNone(resp.id)

    def test_get_snippet_fail(self):
        '''
        Test fetching of the Snippet Metadata when the id does not exist
        '''
        arg_id = 'user1-snippit-1sdfsc'
        self.stub_table.add_response(
            'query',
            {"Items": []}
        )
        self.stub_table.activate()
        resp = self.snippet_manager.get_snippet(arg_id)
        self.assertIsNone(resp)

    def test_create_snippet(self):
        '''
        Test creating of a new snippet
        '''
        data = open('./test/test_snippet/data.json', 'r')
        file = FileStorage(open('./test/test_snippet/binary_search_test.py', 'r'), 'abc.py')
        self.stub_table.add_response(
            'put_item',
            {"Attributes": {"id": {"S": "user1-snippit-1"}}}
        )
        self.stub_table.activate()
        self.snippet_manager.user.cognito_client = MagicMock()
        self.snippet_manager.fs.upload_fileobj = MagicMock()
        self.snippet_manager.es.index = MagicMock()
        snippet = self.snippet_manager.create_snippet(data, file)
        self.assertIsNotNone(snippet)

    def test_create_snippet_fail(self):
        '''
        Test creating of a new snippet in the event of fail
        '''
        data = open('./test/test_snippet/data.json', 'r')
        file = FileStorage(open('./test/test_snippet/binary_search_test.py', 'r'), 'abc.py')
        self.stub_table.add_client_error('put_item', 'ConnectionRefused')
        self.stub_table.activate()
        self.snippet_manager.user.cognito_client = MagicMock()
        self.snippet_manager.fs.upload_fileobj = MagicMock()
        self.snippet_manager.es.index = MagicMock()
        failed = False
        try :
            snippet = self.snippet_manager.create_snippet(data, file)
        except Exception as e:
            failed = True
        self.assertTrue(failed)

    def test_update_snippet_fail(self):
        '''
        Test creating of a new snippet in the event of fail
        '''
        data = open('./test/test_snippet/data.json', 'r')
        file = FileStorage(open('./test/test_snippet/binary_search_test.py', 'r'), 'abc.py')
        self.stub_table.add_client_error('put_item', 'ConnectionRefused')
        self.stub_table.activate()
        self.snippet_manager.user.cognito_client = MagicMock()
        self.snippet_manager.fs.upload_fileobj = MagicMock()
        self.snippet_manager.es.index = MagicMock()
        failed = False
        try :
            snippet = self.snippet_manager.update_snippet(data, file)
        except Exception as e:
            failed = True
        self.assertTrue(failed)


if __name__=="__main__":
    unittest.main()
