'''
Tag Definition
'''
class Tag():
    '''
    Class definition to represent a Tag
    Attributes:
        category    : a value from ['user', 'language] to indicate the tag category
        value       : indicates the value of the tag. e.g. 'python', 'binary_search'
    '''

    def __init__(self):
        '''
        This should always initialize an empty tag
        '''
        self._category = None
        self._value = None

    @property
    def category(self):
        '''Category Getter'''
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def value(self):
        '''Value Getter'''
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
