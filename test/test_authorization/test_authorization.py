"""
Test module for authorization decorator
"""
import unittest
from unittest.mock import Mock, patch
from flask import Flask, request
from jose import jwt, jwk
from src.utilities.authorization import authorization

class TestAuthorization(unittest.TestCase):
    """
    Class for unit testing of authorization decorators
    """
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True


    def test_invalid_missing_token(self):
        """
        Tests whether the token has been provided or not
        """
        with self.app.test_request_context():
            func = Mock()
            decorated_function = authorization(func)
            service_response = decorated_function(request)
            self.assertEqual(service_response["message"], "Token not present/Invalid token.")


    def test_invalid_token(self):
        """
        Tests whether the token is invalid
        """
        with self.app.test_request_context(
            headers={"token": "sample-token"}
        ):
            id_token = request.headers.get("token", None)
            self.assertEqual(id_token, "sample-token")
            get_keys = Mock(name="src.utilities.authorization.get_keys")
            get_keys.return_value = list()
            jwt.get_unverified_headers = Mock(name="get_unverified_headers")
            jwt.get_unverified_headers.return_value = {"kid": "sample-kid"}
            find_public_key = Mock(name="find_public_key")
            find_public_key.return_value = -1
            func = Mock()
            decorated_function = authorization(func)
            service_response = decorated_function(request)
            self.assertEqual(service_response["message"], "Invalid authorization token.")
            self.assertTrue(service_response["error"])

    @patch("src.utilities.authorization.find_public_key")
    @patch("src.utilities.authorization.verify_public_key")
    @patch("src.utilities.authorization.get_keys")
    def test_invalid_signature(self, get_keys_mock, verify_public_key_mock, \
                                        find_public_key_mock):
        """
        Tests whether the token verification is successful or not
        :params:
            get_keys_mock: mock object for get_keys
            verify_public_key_mock: mock object for verify_public_key_mock
            find_public_key_mock: mock object for find_public_key_mock
        """
        with self.app.test_request_context(
            headers={"token": "sample-token"}
        ):
            id_token = request.headers.get("token", None)
            self.assertEqual(id_token, "sample-token")

            # mock objects
            get_keys_mock.return_value = [{"kid": "sample-kid"}]
            jwt.get_unverified_headers = Mock(name="get_unverified_headers")
            jwt.get_unverified_headers.return_value = {"kid": "sample-kid"}
            find_public_key_mock.return_value = 0
            jwk.construct = Mock(name="construct")
            verify_public_key_mock.return_value = False

            # assertions
            func = Mock()
            decorated_function = authorization(func)
            service_response = decorated_function(request)
            self.assertEqual(service_response["message"], "Signature verification failed.")
            self.assertTrue(service_response["error"])

    @patch("src.utilities.authorization.is_token_expired")
    @patch("src.utilities.authorization.find_public_key")
    @patch("src.utilities.authorization.verify_public_key")
    @patch("src.utilities.authorization.get_keys")
    def test_token_expired(self, get_keys_mock, verify_public_key_mock, \
                                 find_public_key_mock, token_expired_mock):
        """
        Tests whether the token verification is successful or not
        :params:
            get_keys_mock: mock object for get_keys
            verify_public_key_mock: mock object for verify_public_key_mock
            find_public_key_mock: mock object for find_public_key_mock
            token_expired_mock: mock object for token_expired_mock
        """
        with self.app.test_request_context(
            headers={"token": "sample-token"}
        ):
            id_token = request.headers.get("token", None)
            self.assertEqual(id_token, "sample-token")

            # mock objects
            get_keys_mock.return_value = [{"kid": "sample-kid"}]
            jwt.get_unverified_headers = Mock(name="get_unverified_headers")
            jwt.get_unverified_headers.return_value = {"kid": "sample-kid"}
            find_public_key_mock.return_value = 0
            jwk.construct = Mock(name="construct")
            verify_public_key_mock.return_value = True
            jwt.get_unverified_claims = Mock(name="get_unverified_headers")
            token_expired_mock.return_value = True

            # assertions
            func = Mock()
            decorated_function = authorization(func)
            service_response = decorated_function(request)
            self.assertEqual(service_response["message"], "Token has expired.")
            self.assertTrue(service_response["error"])

    @patch("src.utilities.authorization.is_audience_valid")
    @patch("src.utilities.authorization.is_token_expired")
    @patch("src.utilities.authorization.find_public_key")
    @patch("src.utilities.authorization.verify_public_key")
    @patch("src.utilities.authorization.get_keys")
    def test_invalid_audience(self, get_keys_mock, verify_public_key_mock, \
                                 find_public_key_mock, token_expired_mock, \
                                 audience_valid_mock):
        """
        Tests whether the token verification is successful or not
        :params:
            get_keys_mock: mock object for get_keys
            verify_public_key_mock: mock object for verify_public_key_mock
            find_public_key_mock: mock object for find_public_key_mock
            token_expired_mock: mock object for token_expired_mock
            audience_valid_mock: mock object for audience_valid_mock
        """
        with self.app.test_request_context(
            headers={"token": "sample-token"}
        ):
            id_token = request.headers.get("token", None)
            self.assertEqual(id_token, "sample-token")

            # mock objects
            get_keys_mock.return_value = [{"kid": "sample-kid"}]
            jwt.get_unverified_headers = Mock(name="get_unverified_headers")
            jwt.get_unverified_headers.return_value = {"kid": "sample-kid"}
            find_public_key_mock.return_value = 0
            jwk.construct = Mock(name="construct")
            verify_public_key_mock.return_value = True
            jwt.get_unverified_claims = Mock(name="get_unverified_headers")
            token_expired_mock.return_value = False
            audience_valid_mock.return_value = False

            # assertions
            func = Mock()
            decorated_function = authorization(func)
            service_response = decorated_function(request)
            self.assertEqual(service_response["message"], "Token was not issued for the app.")
            self.assertTrue(service_response["error"])

    def tearDown(self) -> None:
        del self.app
