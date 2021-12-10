import json
import unittest
from unittest.mock import patch
from src.manager.user_manager import UserManager
from src.manager.snippet_manager import SnippetManager
from src.model.user import User
from src.model.snippet import Snippet
from botocore.stub import Stubber
from werkzeug.datastructures import FileStorage
from unittest.mock import MagicMock

class TestSnippetView(unittest.TestCase):
    """
    Test class for Snippet related CRUD Services
    """

    def setUp(self):
        pass

    @patch('src.manager.user_manager.UserManager.get_user_details')
    def test_get_snippet_success_single(self, mock_user):
        user = User()
        user.email = 'abc@xyz.com'
        user.name = 'ABC'
        user.phone_number = '123'
        mock_user.return_value = {
            'data': {
                'user': user
            }
        }
        manager = SnippetManager()
        dynamo_stub = Stubber(manager.table.meta.client)
        dynamo_stub.add_response(
            'query',
            {"Items": [{"id": {"S": "user1-snippit-1"}, "author": {"S": "abc@xyz.com"}}]}
        )
        dynamo_stub.activate()
        resp = manager.get_snippet('user-snippit-1','asdasdasdasdasd')
        self.assertEqual(len(resp[1]), 0)
        self.assertEqual(len(resp[0]), 1)

    @patch('src.manager.user_manager.UserManager.get_user_details')
    def test_get_snippet_success_multiple(self, mock_user):
        user = User()
        user.email = 'abc@xyz.com'
        user.name = 'ABC'
        user.phone_number = '123'
        mock_user.return_value = {
            'data': {
                'user': user
            }
        }
        manager = SnippetManager()
        dynamo_stub = Stubber(manager.table.meta.client)
        dynamo_stub.add_response(
            'scan',
            {"Items": [{"id": {"S": "user1-snippit-1"}, "author": {"S": "abc@xyz.com"}}, {"id": {"S": "user1-snippit-2"}, "author": {"S": "abc@xyz.com"}}]}
        )
        dynamo_stub.activate()
        resp = manager.get_snippet('','asdasdasdasdasd')
        self.assertEqual(len(resp[1]), 0)
        self.assertEqual(len(resp[0]), 2)
        
    @patch('src.manager.user_manager.UserManager.get_user_details')
    def test_get_snippet_fail_single(self, mock_user):
        user = User()
        user.email = 'abc@xyz.com'
        user.name = 'ABC'
        user.phone_number = '123'
        mock_user.return_value = {
            'data': {
                'user': user
            }
        }
        manager = SnippetManager()
        dynamo_stub = Stubber(manager.table.meta.client)
        dynamo_stub.add_response(
            'query',
            {"Items": []}
        )
        dynamo_stub.activate()
        resp = manager.get_snippet('user-snippit-1','asdasdasdasdasd')
        self.assertEqual(len(resp[1]), 1)
        self.assertEqual(len(resp[0]), 0)

    @patch('src.manager.user_manager.UserManager.get_user_details')
    def test_get_snippet_fail_multiple(self, mock_user):
        user = User()
        user.email = 'abc@xyz.com'
        user.name = 'ABC'
        user.phone_number = '123'
        mock_user.return_value = {
            'data': {
                'user': user
            }
        }
        manager = SnippetManager()
        dynamo_stub = Stubber(manager.table.meta.client)
        dynamo_stub.add_response(
            'scan',
            {"Items": []}
        )
        dynamo_stub.activate()
        resp = manager.get_snippet('',None)
        self.assertEqual(len(resp[0]), 0)

    @patch('src.manager.user_manager.UserManager.get_user_details')
    def test_create_snippet_success(self, mock_user):
        '''
        Test creating of a new snippet
        '''
        user = User()
        user.email = 'abc@xyz.com'
        user.name = 'ABC'
        user.phone_number = '123'
        mock_user.return_value = {
            'data': {
                'user': user
            }
        }
        # data = open('./test/test_snippet/data.json', 'r')
        data = {
            "email": "nmw@nmw.com",
            "id": "dfsjdf",
            "desc": "A generic binary search for sorted datasets",
            "tags": ["binary_search", "algorithms", "prep"],
            "shares": ["user@gmail.com"]
        }
        data = json.dumps(data)
        file = FileStorage(open('./test/test_snippet/binary_search_test.py', 'r'), 'abc.py')
        manager = SnippetManager()
        dynamo_stub = Stubber(manager.table.meta.client)
        dynamo_stub.add_response(
            'query',
            {"Items": [{"id": {"S": "user1-snippit-1"}, "author": {"S": "abc@xyz.com"}}]}
        )
        dynamo_stub.activate()
        manager.user.cognito_client = MagicMock()
        manager.fs.upload_fileobj = MagicMock()
        manager.es.index = MagicMock()
        snippet, validation = manager.create_snippet(data, file, 'sdfsdfsdfsdf')
        self.assertIsNotNone(snippet)


    @patch('src.manager.user_manager.UserManager.get_user_details')
    def test_create_snippet_fail(self, mock_user):
        '''
        Test creating of a new snippet
        '''
        user = User()
        user.email = 'abc@xyz.com'
        user.name = 'ABC'
        user.phone_number = '123'
        mock_user.return_value = {
            'data': {
                'user': user
            }
        }
        data = open('./test/test_snippet/data_error.json', 'r')
        file = FileStorage(open('./test/test_snippet/binary_search_test.py', 'r'), 'abc.py')
        manager = SnippetManager()
        dynamo_stub = Stubber(manager.table.meta.client)
        dynamo_stub.add_response(
            'query',
            {"Items": [{"id": {"S": "user1-snippit-1"}, "author": {"S": "abc@xyz.com"}}]}
        )
        dynamo_stub.activate()
        manager.user.cognito_client = MagicMock()
        manager.fs.upload_fileobj = MagicMock()
        manager.es.index = MagicMock()
        snippet, validation = manager.create_snippet(data, file, 'sdfsdfsdfsdf')
        self.assertIsNotNone(snippet)
        self.assertEqual(len(validation), 1)

    @patch('src.manager.user_manager.UserManager.get_user_details')
    def test_update_snippet_success(self, mock_user):
        '''
        Test creating of a new snippet
        '''
        user = User()
        user.email = 'abc@xyz.com'
        user.name = 'ABC'
        user.phone_number = '123'
        mock_user.return_value = {
            'data': {
                'user': user
            }
        }
        data = open('./test/test_snippet/data.json', 'r')
        file = FileStorage(open('./test/test_snippet/binary_search_test.py', 'r'), 'abc.py')
        manager = SnippetManager()
        dynamo_stub = Stubber(manager.table.meta.client)
        dynamo_stub.add_response(
            'query',
            {"Items": [{"id": {"S": "user1-snippit-1"}, "author": {"S": "abc@xyz.com"}}]}
        )
        dynamo_stub.activate()
        manager.user.cognito_client = MagicMock()
        manager.fs.upload_fileobj = MagicMock()
        manager.es.index = MagicMock()
        snippet, validation = manager.update_snippet(data, file, 'sdfsdfsdfsdf')
        self.assertIsNotNone(snippet)

    @patch('src.manager.user_manager.UserManager.get_user_details')
    def test_update_snippet_share_list(self, mock_user):
        '''
        Test creating of a new snippet
        '''
        user = User()
        user.email = 'abc@xyz.com'
        user.name = 'ABC'
        user.phone_number = '123'
        mock_user.return_value = {
            'data': {
                'user': user
            }
        }
        # mock_fs.return_value = None
        # data = open('./test/test_snippet/data.json', 'r')
        data = {
            "email": "nmw@nmw.com",
            "id": "dfsjdf",
            "desc": "A generic binary search for sorted datasets",
            "tags": ["binary_search", "algorithms", "prep"],
            "shares": ["user@gmail.com"]
        }
        data = json.dumps(data)
        file = FileStorage(open('./test/test_snippet/binary_search_test.py', 'r'), 'abc.py')
        manager = SnippetManager()
        dynamo_stub = Stubber(manager.table.meta.client)
        dynamo_stub.add_response(
            'query',
            {"Items": [{"id": {"S": "user1-snippit-1"}, "author": {"S": "abc@xyz.com"}}]}
        )
        dynamo_stub.activate()
        manager.user.cognito_client = MagicMock()
        manager.fs.upload_fileobj = MagicMock(return_value=None)
        manager.es.index = MagicMock()
        manager.es.delete = MagicMock()
        snippet = Snippet()
        snippet.id = "dfsjdf"
        snippet.shares = ["user3@gmail.com"]
        manager.get_snippet = MagicMock(return_value=([snippet],None))
        snippet, validation = manager.update_snippet(data, file, 'sdfsdfsdfsdf')
        self.assertIsNotNone(snippet)

    @patch('src.manager.user_manager.UserManager.get_user_details')
    def test_create_snippet_fail(self, mock_user):
        '''
        Test creating of a new snippet
        '''
        user = User()
        user.email = 'abc@xyz.com'
        user.name = 'ABC'
        user.phone_number = '123'
        mock_user.return_value = {
            'data': {
                'user': user
            }
        }
        data = open('./test/test_snippet/data_error.json', 'r')
        file = FileStorage(open('./test/test_snippet/binary_search_test.py', 'r'), 'abc.py')
        manager = SnippetManager()
        dynamo_stub = Stubber(manager.table.meta.client)
        dynamo_stub.add_response(
            'query',
            {"Items": [{"id": {"S": "user1-snippit-1"}, "author": {"S": "abc@xyz.com"}}]}
        )
        dynamo_stub.activate()
        manager.user.cognito_client = MagicMock()
        manager.fs.upload_fileobj = MagicMock()
        manager.es.index = MagicMock()
        snippet, validation = manager.update_snippet(data, file, 'sdfsdfsdfsdf')
        self.assertIsNotNone(snippet)
        self.assertEqual(len(validation), 1)

    @patch('src.manager.user_manager.UserManager.get_user_details')
    def test_delete_snippet_fail(self, mock_user):
        '''
        Test creating of a new snippet
        '''
        user = User()
        user.email = 'abc@xyz.com'
        user.name = 'ABC'
        user.phone_number = '123'
        mock_user.return_value = {
            'data': {
                'user': user
            }
        }
        manager = SnippetManager()
        dynamo_stub = Stubber(manager.table.meta.client)
        dynamo_stub.add_response(
            'query',
            {"Items": [{"id": {"S": "user1-snippit-1"}, "author": {"S": "abc@xyz.com"}}]}
        )
        dynamo_stub.activate()
        manager.user.cognito_client = MagicMock()
        manager.fs.upload_fileobj = MagicMock()
        manager.es.index = MagicMock()
        snippet, validation = manager.delete_snippet('user1-snippit-1', 'sdfsdfsdfsdf')
        self.assertIsNotNone(snippet)
        self.assertEqual(len(validation), 2)