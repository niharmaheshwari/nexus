"""
Test cases for user authentication and authorization
"""
from datetime import datetime, timedelta
import time
import unittest
from unittest.mock import Mock
from botocore.stub import Stubber
from jose import jwt
from src.constants.secrets import CLIENT_ID, KEYS_URL
from src.manager.user_manager import UserManager
from src.utilities.authentication_utils import find_public_key, \
            get_keys, is_audience_valid, is_token_expired, serialize_user_object
from src.model.user import User


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

    # refresh token flow
    def test_refresh_token_missing_params(self):
        """
        Tests missing parameters for generating new tokens
        """
        parameters = {}
        response = self.user_manager.generate_new_token(parameters)
        self.assertEqual("email is not present", response["message"])
        self.assertTrue(response["error"])

    def test_refresh_token_invalid_token(self):
        """
        Tests invalid token/email for generating new tokens
        """
        parameters = {"email": "sample@gmail.com", "refresh_token": "xxxx"}
        self.stubber.add_client_error("initiate_auth", "NotAuthorizedException")
        self.stubber.activate()
        response = self.user_manager.generate_new_token(parameters)
        self.assertEqual("Invalid email/token", response["message"])
        self.assertTrue(response["error"])

    def test_refresh_token_user_not_confirmed(self):
        """
        Tests whether the user is confirmed or not for generating new tokens
        """
        parameters = {"email": "sample@gmail.com", "refresh_token": "xxxx"}
        self.stubber.add_client_error("initiate_auth", "UserNotConfirmedException")
        self.stubber.activate()
        response = self.user_manager.generate_new_token(parameters)
        self.assertEqual("User is not confirmed", response["message"])
        self.assertTrue(response["error"])

    def test_refresh_token_success(self):
        """
        Happy path flow for generate_refresh_tokens
        """
        parameters = {"email": "sample@gmail.com", "refresh_token": "xxxx"}
        service_response = {
            'ChallengeName': 'SMS_MFA',
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
        self.stubber.add_response("initiate_auth", service_response)
        self.stubber.activate()
        response = self.user_manager.generate_new_token(parameters)
        self.assertEqual("success", response["message"])
        self.assertFalse(response["error"])
        self.assertTrue(response["success"])

    # fetch user details flow

    def test_get_user_details_invalid_user(self):
        """
        Tests invalid email for get user details
        """
        self.stubber.add_client_error("admin_get_user", "UserNotFoundException")
        jwt.get_unverified_claims = \
            Mock(name="get_unverified_claims")
        jwt.get_unverified_claims.return_value = {"email": "sample-email@gmail.com"}
        self.stubber.activate()
        response = self.user_manager.get_user_details(token="sample-token")
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
        jwt.get_unverified_claims = \
            Mock(name="get_unverified_claims")
        jwt.get_unverified_claims.return_value = {"email": "sample-email@gmail.com"}
        self.stubber.activate()
        response = self.user_manager.get_user_details(token="sample-token")
        self.assertEqual("success", response["message"])
        self.assertFalse(response["error"])
        self.assertTrue(response["success"])
    
    # authentication utils error
    def test_invalid_public_key_not_found(self):
        key_id = "sample"
        key_list = get_keys()
        response = find_public_key(key_id, key_list)
        self.assertEqual(response, -1)
    
    def test_valid_public_key_found(self):
        key_id = "n59PyjVWe1jjiJ0mAJQPP5eUjH4jPNbDwltff0144U4="
        key_list = get_keys()
        response = find_public_key(key_id, key_list)
        self.assertEqual(response, 0)
    
    def test_token_expired(self):
        claims = {'exp': 13}
        response = is_token_expired(claims)
        self.assertTrue(response)
    
    def test_token_not_expired(self):
        datetime_time = datetime.now() + timedelta(days=1)
        timestamp = datetime.timestamp(datetime_time)
        claims = {'exp': timestamp}
        response = is_token_expired(claims)
        self.assertFalse(response)
    
    def test_invalid_claims(self):
        claims = {'aud': "sample"}
        response = is_audience_valid(claims)
        self.assertFalse(response)

    def test_valid_claims(self):
        claims = {'aud': CLIENT_ID}
        response = is_audience_valid(claims)
        self.assertTrue(response)

    def test_user_serialization(self):
        user = User()
        user.set_user_id("uid")
        user.set_name("sample")
        user.set_phone_number("123")
        user.set_email("sample@gmail.com")
        user.set_birth_date("05/03/1997")

        serialized_user = [
            {"Name": "sub", "Value": "uid"},
            {"Name": "email", "Value": "sample@gmail.com"},
            {"Name": "name", "Value": "sample"},
            {"Name": "phone_number", "Value": "123"},
            {"Name": "birthdate", "Value": "05/03/1997"}
        ]

        serialized_response = serialize_user_object(user)
        self.assertListEqual(serialized_response, serialized_user)

    def tearDown(self):
        del self.user_manager
        self.stubber.deactivate()

if __name__=="__main__":
    unittest.main()
