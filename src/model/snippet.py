'''
Snippet Definition
'''
class Snippet():
    '''
    Class definition to represent a Snippet.
    Attributes:
        uri         : S3 uri indicating the file location
        desc        : A user description for a code snippet
        id          : A hex string representing a unique id for a snippet
        tags        : A list of Strings representing the Snippet tags
        author      : A string representing the user_id of the uploader
        shares      : A list of user_ids representing the share list
        audit       : An instance of the audit class giving the latest audit
        lang        : The language tag of the snippet
    '''

    def __init__(self):
        '''
        This should always initialize an empty snippet
        '''
        self._uri = None
        self._desc = None
        self._id = None
        self._tags = None
        self._author = None
        self._shares = None
        self._audit = None
        self._lang = None

    def __init__(self, uri, desc, id, tags, author, shares, audit, lang):
        """
        Initialize an object of Snippet
        Args:
            uri         : S3 uri indicating the file location
            desc        : A user description for a code snippet
            id          : A hex string representing a unique id for a snippet
            tags        : A list of Strings representing the Snippet tags
            author      : A string representing the user_id of the uploader
            shares      : A list of user_ids representing the share list
            audit       : An instance of the audit class giving the latest audit
            lang        : The language tag of the snippet
        """
        self._uri = uri
        self._desc = desc
        self._id = id
        self._tags = tags
        self._author = author
        self._shares = shares
        self._audit = audit
        self._lang = lang

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
    def id(self):
        '''Getter for id'''
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def tags(self):
        '''Getter for Tags'''
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value

    @property
    def author(self):
        '''Getter for author'''
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def audit(self):
        '''Getter for audit'''
        return self._audit

    @audit.setter
    def audit(self, value):
        self._audit = value

    @property
    def lang(self):
        '''Getter for lang'''
        return self._lang

    @lang.setter
    def lang(self, value):
        self._lang = value
    
    @property
    def shares(self):
        '''Getter for shares'''
        return self._shares

    @shares.setter
    def shares(self, value):
        self._shares = value