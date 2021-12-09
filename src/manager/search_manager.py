'''
Search Manager
'''
import json
from src.manager.snippet_snapshot_manager import SnippetSnapshotManager
from src.manager.snippet_manager import SnippetManager
from src.manager.user_manager import UserManager
from src.model.message_format import MessageFormat
from src.utils.utils import CustomJSONEncoder


class SearchManager():
    '''
    Class to manage searching
    '''

    def __init__(self):
        self.snippet_snapshot_manager = SnippetSnapshotManager()
        self.snippet_manager = SnippetManager()
        self.user_manager = UserManager()

    def search_general(self, search_string, email):
        '''
        This method returns a MessageFormat containing search results or an error
        '''

        # Get snippet snapshot information
        snippet_snapshots, err = self.snippet_snapshot_manager.search_by_string(
            search_string, email)
        if err is not None:
            return err
        if snippet_snapshots == []:
            return MessageFormat().success_message(data={"snippets":[]})

        ids = SearchManager.extract_ids_from_snapshots(snippet_snapshots)

        # Get snippets
        snippets_response = self.snippet_manager.get_snippets(ids)
        if snippets_response["error"] is True:
            return snippets_response
        snippets = snippets_response["data"]

        results = json.loads(json.dumps({"snippets":snippets},cls=CustomJSONEncoder))
        return MessageFormat().success_message(data=results)

    @staticmethod
    def extract_ids_from_snapshots(snippet_snapshots):
        '''Extract ids from snippetSnapshots into list of ids'''
        ids = []
        for snapshot in snippet_snapshots:
            ids.append(snapshot.id)
        return ids
