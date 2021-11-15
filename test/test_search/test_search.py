"""
Test cases for searching 
"""
import unittest
from unittest import mock, TestCase
from src.manager.search_manager import SearchManager
from src.model.message_format import MessageFormat

from src.model.snippet_snapshot import SnippetSnapshot

class TestSearch(TestCase):
    """
    Test class for searching
    """
    # pylint: disable=unused-argument
    def setUp(self):
       self.search_manager = SearchManager()

    @mock.patch('src.manager.search_manager.UserManager.get_user_details', return_value=MessageFormat().error_message("error"))
    def test_search_general_bad_user(self, mock_user_manger):
        rsp = self.search_manager.search_general("string", "bademail")
        self.assertEqual(MessageFormat().error_message("error"), rsp)

    @mock.patch('src.manager.search_manager.UserManager.get_user_details', 
    return_value=MessageFormat().success_message(data={"user":'user1'}))
    @mock.patch('src.manager.search_manager.SnippetSnapshotManager.search_by_string', return_value=[])
    def test_search_general_happy_path_no_snippets(self, mock1, mock2):
        rsp = self.search_manager.search_general("string", "email")
        self.assertEqual(MessageFormat().success_message(data={"snippets":[]}), rsp)
    
    @mock.patch('src.manager.search_manager.UserManager.get_user_details', 
    return_value=MessageFormat().success_message(data={"user":'user1'}))
    @mock.patch('src.manager.search_manager.SnippetSnapshotManager.search_by_string', 
    return_value=[SnippetSnapshot('id1',['binary'], 'bs', 'python'),SnippetSnapshot('id2',['tags'], 'desc', 'c++')])
    @mock.patch('src.manager.search_manager.SnippetManager.get_snippets', return_value=['id1', 'id2'])





if __name__=="__main__":
    unittest.main()
