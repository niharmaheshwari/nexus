'''
Snippet Snapshot for Elastic
'''
class SnippetSnapshot():
    '''
    Class definition to represent the minified view of the Snippet
    Attributes
        id  : A hex string representing a unique id for a snippet
        tags        : A list of Strings representing the Snippet tags
        desc        : A user description for a code snippet
        lang        : The language tag of the snippet
    '''

    def __init__(self):
        self._id = None
        self._tags = None
        self._desc = None
        self._lang = None

    def __init__(self, snippit_id, tags, desc, lang):
        """
        Initialize an object of SnippetSnapshot
        Args:
            snippit_id: A hex string representing a unique id for a snippet
            tags: A list of Strings representing the Snippet tags
            desc: A user description for a code snippet
            lang: The language tag of the snippet
        """
        self._id = snippit_id
        self._tags = tags
        self._desc = desc
        self._lang = lang

    @property
    def desc(self):
        '''Getter for desc'''
        return self._desc

    @desc.setter
    def desc(self, value):
        self._desc = value

    @property
    def id(self):
        '''Getter for id'''
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def tags(self):
        '''Getter for tags'''
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value

    @property
    def lang(self):
        '''Getter for lang'''
        return self._lang

    @lang.setter
    def lang(self, value):
        self._lang = value