"""
User class
"""

class User:
    """
    User model class describing the structure of the class
    """
    def __init__(self):
        self.uid = None
        self.name = None
        self.birthdate = None
        self.phone_number = None
        self.email = None

    # getter and setter methods for the model
    def set_user_id(self, uid):
        """
        Setter for uid
        """
        self.uid = uid

    def get_user_id(self):
        """
        Getter for uid
        """
        return self.uid


    def set_name(self, name):
        """
        Setter for name
        """
        self.name = name

    def get_name(self):
        """
        Getter for name
        """
        return self.name

    def set_birth_date(self, date):
        """
        Setter for birth date
        """
        self.birthdate = date

    def get_birth_date(self):
        """
        Getter for name
        """
        return self.birthdate

    def set_phone_number(self, phone_number):
        """
        Setter for phone_number
        """
        self.phone_number = phone_number

    def get_phone_number(self):
        """
        Getter for name
        """
        return self.phone_number

    def set_email(self, email):
        """
        Setter for email
        """
        self.email = email

    def get_email(self):
        """
        Getter for name
        """
        return self.email
