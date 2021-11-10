'''
Snippet Snapshot for Elastic
'''
class SnippetSnapshot():
    '''
    Class definition to represent the minified view of the Snippet
    Attributes
        snippet_id  : A hex string representing a unique snippet_id for a snippet
        creator     : A string representing the user_snippet_id of the uploader
        tags        : A list of instances of the Tag class
        desc        : A user description for a code snippet
    '''

    def __init__(self):
        self._snippet_id = None
        self._creator = None
        self._tags = None
        self._desc = None

    @property
    def desc(self):
        '''Getter for desc'''
        return self._desc

    @desc.setter
    def desc(self, value):
        self._desc = value

    @property
    def snippet_id(self):
        '''Getter for snippet_id'''
        return self._snippet_id

    @snippet_id.setter
    def snippet_id(self, value):
        self._snippet_id = value

    @property
    def tags(self):
        '''Getter for tags'''
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value

    @property
    def creator(self):
        '''Getter for creator'''
        return self._creator

    @creator.setter
    def creator(self, value):
        self._creator = value
