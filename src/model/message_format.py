"""
Model class for return message format
"""

class MessageFormat():
    """
    Describes the message format for API calls
    made during authentication and authorization
    """
    def __init__(self):
        self._status_code = None
        self._message = ""
        self._error = False
        self._success = False
        self._data = None

    def __to_json(self):
        """
        Converts the attributes to json
        """
        return {
            "status_code": self._status_code,
            "message": self._message,
            "error": self._error,
            "success": self._success,
            "data": self._data
        }

    def error_message(self, message, status_code=400):
        """
        Message format for error message
        :params:
            :message: str, error message
        :returns:
            :dict, message details
        """
        self._status_code = status_code
        self._message = message
        self._error = True
        return self.__to_json()

    def success_message(self, data, message="success"):
        """
        Message format for a success message
        :params:
            :data: dict, information to be returned
            :message: str, success message (default=success)
        :returns:
            :dict, message details
        """
        self._status_code = 200
        self._data = data
        self._message = message
        self._success = True
        return self.__to_json()
