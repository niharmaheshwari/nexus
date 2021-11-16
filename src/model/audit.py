'''
Snippet Audit
'''
class Audit():
    '''
    Class definition to represent the latest Audit.
    Attributes:
        last_upd_date   : Last Updated Date for a Snippet
        last_upd_user   : Username of the user who performed the last touch on the Snippet
        creation_date   : Creation Date for a Snippet
        creation_user   : Username of the user who created the Snippet
    '''

    def __init__(self, last_upd_date, last_upd_user, creation_date, creation_user):
        """
        Args:
            last_upd_date   : Last Updated Date for a Snippet
            last_upd_user   : Username of the user who performed the last touch on the Snippet
            creation_date   : Creation Date for a Snippet
            creation_user   : Username of the user who created the Snippet
        """
        self._last_upd_date = last_upd_date
        self._last_upd_user = last_upd_user
        self._creation_date = creation_date
        self._creation_user = creation_user

    @property
    def last_upd_date(self):
        '''Getter for last_upd_date'''
        return self._last_upd_date

    @last_upd_date.setter
    def last_upd_date(self, value):
        self._last_upd_date = value

    @property
    def last_upd_user(self):
        '''Getter for last_upd_user'''
        return self._last_upd_user

    @last_upd_user.setter
    def last_upd_user(self, value):
        self._last_upd_user = value

    @property
    def creation_date(self):
        '''Getter for creation_date'''
        return self._creation_date

    @creation_date.setter
    def creation_date(self, value):
        self._creation_date = value

    @property
    def creation_user(self):
        '''Getter for creation_user'''
        return self._creation_user

    @creation_user.setter
    def creation_user(self, value):
        self._creation_user = value
