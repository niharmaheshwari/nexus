'''
Testing snippet snapshot and search functionality
'''
import unittest
from unittest import mock, TestCase
from src.manager.snippet_snapshot_manager import SnippetSnapshotManager
from src.manager.search_manager import SearchManager
from src.manager.snippet_manager import SnippetManager
from src.model.message_format import MessageFormat
from src.model.snippet_snapshot import SnippetSnapshot

# pylint: disable=unused-argument
class TestSnippetSnapshot(TestCase):
    '''
    Test class for snippet snapshot and search functionality
    '''
    snippet_snapshot_manager = SnippetSnapshotManager()
    search_manager = SearchManager()
    snippet_manager = SnippetManager()

    def test_get_snippet_snapshots_success(self):
        '''testing getting a snippet snapshot from es'''

        es_response =  {'_shards': {'failed': 0, 'skipped': 0, 'successful': 5, 'total': 5},
                        'hits': {'hits': [{'_id': 'hzp9h30BEkalmidZuH96',
                        '_index': 'nm3223@columbia.edu',
                        '_score': 1.8923234,
                        '_source': {'desc': 'x265',
                                'id': 'b26686a6-554e-11ec-9fc1-fd30d1dbf375',
                                'lang': 'Python',
                                'tags': ['binary search']},
                        '_type': 'snippet'}],
                        'max_score': 1.8923234,
                        'total': {'relation': 'eq', 'value': 1}},
                        'timed_out': False,
                        'took': 11}

        with mock.patch('src.manager.snippet_snapshot_manager.OpenSearch.search',
         return_value=es_response):
            rsp, err = self.snippet_snapshot_manager.search_by_string(
                'bs','nm3223@columbia.edu')
        self.assertIsInstance(rsp[0],SnippetSnapshot)
        self.assertIsNone(err)

    @mock.patch('src.manager.snippet_snapshot_manager.OpenSearch.search', return_value=None)
    def test_get_snippet_snapshots_fail(self, mock1):
        '''tests searching when invalid id is inputted'''
        mock1.side_effect = Exception()
        rsp, err = self.snippet_snapshot_manager.search_by_string('searching for bs', 'invalidID')
        self.assertIsNone(rsp)
        self.assertTrue(err['error'])

    @mock.patch('src.manager.search_manager.SnippetSnapshotManager.search_by_string',
     return_value=(None,MessageFormat().error_message("error")))
    def test_search_failure(self, mock1):
        '''tests search when there is a ES failure'''
        rsp = self.search_manager.search_general("search string", "tk2892@columbia.edu")
        self.assertTrue(rsp['error'])

    @mock.patch('src.manager.search_manager.SnippetSnapshotManager.search_by_string',
     return_value=([], None))
    def test_search_general_happy_path_no_snippets(self, mock1):
        '''tests search when no snippets match'''
        rsp = self.search_manager.search_general("string", "email")
        self.assertEqual(MessageFormat().success_message(data={"snippets":[]}), rsp)

    @mock.patch('src.manager.search_manager.SnippetSnapshotManager.search_by_string',
    return_value=([SnippetSnapshot('id1',['binary'], 'bs', 'python')
    ,SnippetSnapshot('id2',['tags'], 'desc', 'c++')], None))
    @mock.patch('src.manager.search_manager.SnippetManager.get_snippets',
     return_value=MessageFormat().error_message("error"))
    def test_search_get_snippets_fail(self, mock1, mock2):
        '''tests for when get_snippets fails from dynamoDB'''
        rsp = self.search_manager.search_general("string", "email")
        self.assertTrue(rsp['error'])

    @mock.patch('src.manager.search_manager.SnippetSnapshotManager.search_by_string',
    return_value=([SnippetSnapshot('id1',['binary'], 'bs', 'python'),
    SnippetSnapshot('id2',['tags'], 'desc', 'c++')], None))
    def test_search_happy_path(self, mock1):
        '''tests for when search works correctly'''
        snippets_response = {
            'Responses': {
                'snippets': [ {
                    'id': '1',
                    'uri': 'www.binarysearch.com',
                    'desc': 'desc',
                    'tags': '[binary search]',
                    'author': 'tk2892@columbia.edu',
                    'shares': '',
                    'lang': 'Python',
                    'audit': {
                        'last_upd_user': '',
                        'creation_date':'',
                        'last_upd_date': '',
                        'creation_user':'',
                    }
                }
                ]
            }
        }
        data= self.snippet_manager.dynamo_response_to_snippets(snippets_response)
        with mock.patch('src.manager.search_manager.SnippetManager.get_snippets',
         return_value=MessageFormat().success_message(data=data)):
            rsp = self.search_manager.search_general("string", "email")
        self.assertFalse(rsp['error'])

if __name__=="__main__":
    unittest.main()
