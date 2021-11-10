'''
Snippet Definition
'''
class Snippet():
    '''
    Class definition to represent a Snippet.
    Attributes:
        uri         : S3 uri indicating the file location
        desc        : A user description for a code snippet
        snippet_id  : A hex string representing a unique snippet_id for a snippet
        tags        : A list of instances of the Tag class
        creator     : A string representing the user_snippet_id of the uploader
        shares      : A list of user_snippet_ids representing the share list
        audit       : An instance of the audit class giving the latest audit
    '''

    def __init__(self):
        '''
        This should always initialize an empty snippet
        '''
        self._uri = None
        self._desc = None
        self._snippet_id = None
        self._tags = None
        self._creator = None
        self._shares = None
        self._audit = None

    @property
    def uri(self):
        '''Getter for uri'''
        return self._uri

    @uri.setter
    def uri(self, value):
        self._uri = value

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
        '''Getter for Tags'''
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

    @property
    def audit(self):
        '''Getter for audit'''
        return self._audit

    @audit.setter
    def audit(self, value):
        self._audit = value
