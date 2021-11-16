"""
Test cases for user authentication and authorization
"""
from datetime import datetime
import unittest
from botocore.stub import Stubber
from src.manager.user_manager import UserManager

class TestAuthentication(unittest.TestCase):
    """
    Test class for user authentication and authorization
    """
    def setUp(self):
        self.user_manager = UserManager()
        self.stubber = Stubber(self.user_manager.cognito_client)

    # signup flow
    def test_signup_missing_attribute(self):
        """
        Tests missing attributes in signup
        """
        user_details = {"name": "Shantanu Jain"}
        response = self.user_manager.signup(user_details)
        self.assertEqual("email is not present", response["message"])
        self.assertTrue(response["error"])

    def test_signup_duplicate_username(self):
        """
        Tests duplicate email for the user during signup
        """
        user_details = {
            "email": "shantanujainrko@gmail.com",
            "name": "Shantanu Jain",
            "birthdate": "05/03/1997",
            "phone_number": "+16467644875",
            "password": "sample@123"
        }
        self.stubber.add_client_error("sign_up", service_error_code="UsernameExistsException")
        self.stubber.activate()
        response = self.user_manager.signup(user_details)
        self.assertEqual("This username already exists", response["message"], f"{response}")
        self.assertTrue(response["error"])


    def test_signup_invalid_password(self):
        """
        Tests invalid password type for the user during signup
        """
        user_details = {
            "email": "shantanujainrko@gmail.com",
            "name": "Shantanu Jain",
            "birthdate": "05/03/1997",
            "phone_number": "+16467644875",
            "password": "sample"
        }
        self.stubber.add_client_error("sign_up", service_error_code="InvalidPasswordException")
        self.stubber.activate()
        response = self.user_manager.signup(user_details)
        self.assertEqual("Password should have Caps, \
                Special chars, Numbers", response["message"], f"{response}")
        self.assertTrue(response["error"])

    def test_signup_success(self):
        """
        Happy path for the user signup flow
        """
        user_details = {
            "email": "shantanujainrko@gmail.com",
            "name": "Shantanu Jain",
            "birthdate": "05/03/1997",
            "phone_number": "+16467644875",
            "password": "sample@123"
        }
        service_response = {
            'UserConfirmed': False,
            'CodeDeliveryDetails': {
                'Destination': 'string',
                'DeliveryMedium': 'EMAIL',
                'AttributeName': 'string'
            },
            'UserSub': 'string'
        }
        self.stubber.add_response("sign_up", service_response)
        self.stubber.activate()
        response = self.user_manager.signup(user_details)
        self.assertEqual(
            "Please confirm your signup, check Email for validation code", \
                response["message"], f"{response}")
        self.assertFalse(response["error"])
        self.assertTrue(response["success"])

    # confirm sign up flow
    def test_confirm_signup_missing_attribute(self):
        """
        Tests missing attributes for confirm-signup
        """
        response = self.user_manager.confirm_signup(email=None, otp=None)
        self.assertEqual("Email/OTP is a required attribute.", response["message"])
        self.assertTrue(response["error"])

    def test_confirm_signup_invalid_otp(self):
        """
        Tests invalid otp entered by the user for confirm-signup
        """
        self.stubber.add_client_error("confirm_sign_up", "CodeMismatchException")
        self.stubber.activate()
        response = self.user_manager.confirm_signup(email="shantanujainrko@gmail.com", otp="xxxxx")
        self.assertEqual("Invalid Verification code", response["message"])
        self.assertTrue(response["error"])

    def test_confirm_signup_email_does_not_exist(self):
        """
        Tests whether email is passed or not for confirm-signup
        """
        self.stubber.add_client_error("confirm_sign_up", "UserNotFoundException")
        self.stubber.activate()
        response = self.user_manager.confirm_signup(email="sample@gmail.com", otp="xxxxx")
        self.assertEqual("Username doesnt exists", response["message"])
        self.assertTrue(response["error"])

    def test_confirm_signup_user_confirmed_already(self):
        """
        Tests whether user is already confirmed or not for confirm-signup
        """
        self.stubber.add_client_error("confirm_sign_up", "NotAuthorizedException")
        self.stubber.activate()
        response = self.user_manager.confirm_signup(email="sample@gmail.com", otp="xxxxx")
        self.assertEqual("User is already confirmed", response["message"])
        self.assertTrue(response["error"])

    def test_confirm_signup_success(self):
        """
        Happy path for confirm-signup flow
        """
        service_response = {}
        self.stubber.add_response("confirm_sign_up", service_response)
        self.stubber.activate()
        response = self.user_manager.confirm_signup(email="xxxx@gmail.com", otp="xxxxx")
        self.assertEqual("success", response["message"], f"{response}")
        self.assertFalse(response["error"])
        self.assertTrue(response["success"])

    # login flow
    def test_login_missing_credentials(self):
        """
        Tests missing attributes for login
        """
        credentials = {}
        response = self.user_manager.login(credentials)
        self.assertEqual("email is required", response["message"])
        self.assertTrue(response["error"])

    def test_login_invalid_credentials(self):
        """
        Tests invalid username/password for login
        """
        credentials = {"email": "sample@gmail.com", "password": "sample"}
        self.stubber.add_client_error("admin_initiate_auth", "NotAuthorizedException")
        self.stubber.activate()
        response = self.user_manager.login(credentials)
        self.assertEqual("The username or password is incorrect", response["message"])
        self.assertTrue(response["error"])

    def test_login_user_not_confirmed(self):
        """
        Tests whether the user is confirmed for login
        """
        credentials = {"email": "sample@gmail.com", "password": "sample"}
        self.stubber.add_client_error("admin_initiate_auth", "UserNotConfirmedException")
        self.stubber.activate()
        response = self.user_manager.login(credentials)
        self.assertEqual("User is not confirmed", response["message"])
        self.assertTrue(response["error"])

    def test_login_success(self):
        """
        Happy path for login flow
        """
        credentials = {"email": "sample@gmail.com", "password": "sample"}
        service_response = {
            'ChallengeName': 'string',
            'Session': 'xxxxxxxxxxxxxxxxxxxx',
            'ChallengeParameters': {
                'string': 'string'
            },
            'AuthenticationResult': {
                'AccessToken': 'string',
                'ExpiresIn': 123,
                'TokenType': 'string',
                'RefreshToken': 'string',
                'IdToken': 'string',
                'NewDeviceMetadata': {
                    'DeviceKey': 'string',
                    'DeviceGroupKey': 'string'
                }
            }
        }
        self.stubber.add_response("admin_initiate_auth", service_response)
        self.stubber.activate()
        response = self.user_manager.login(credentials)
        self.assertEqual("success", response["message"])
        self.assertFalse(response["error"])
        self.assertTrue(response["success"])

    # fetch user details flow
    def test_get_user_details_missing_attribute(self):
        """
        Tests missing attributes for get user details
        """
        response = self.user_manager.get_user_details(email=None)
        self.assertEqual("Email is required.", response["message"])
        self.assertTrue(response["error"])

    def test_get_user_details_invalid_user(self):
        """
        Tests invalid email for get user details
        """
        self.stubber.add_client_error("admin_get_user", "UserNotFoundException")
        self.stubber.activate()
        response = self.user_manager.get_user_details(email="sample@gmail.com")
        self.assertEqual("Invalid username", response["message"])
        self.assertTrue(response["error"])

    def test_get_user_details_success(self):
        """
        Happy path for get user details
        """
        service_response = {
            'Username': 'string',
            'UserAttributes': [
                {
                    'Name': 'string',
                    'Value': 'string'
                },
            ],
            'UserCreateDate': datetime(2015, 1, 1),
            'UserLastModifiedDate': datetime(2015, 1, 1),
            'Enabled': True,
            'UserStatus': 'CONFIRMED',
            'MFAOptions': [
                {
                    'DeliveryMedium': 'EMAIL',
                    'AttributeName': 'string'
                },
            ],
            'PreferredMfaSetting': 'string',
            'UserMFASettingList': [
                'string',
            ]
        }
        self.stubber.add_response("admin_get_user", service_response)
        self.stubber.activate()
        response = self.user_manager.get_user_details(email="sample@gmail.com")
        self.assertEqual("success", response["message"])
        self.assertFalse(response["error"])
        self.assertTrue(response["success"])

    def tearDown(self):
        del self.user_manager
        self.stubber.deactivate()

if __name__=="__main__":
    unittest.main()
