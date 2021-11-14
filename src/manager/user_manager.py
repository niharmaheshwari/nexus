"""
User manager class
"""

import logging
import boto3
from src.constants.cognito_constants import ACCESS_KEY, SECRET_ACCESS_KEY, \
            REGION, USER_POOL_ID, CLIENT_ID
from src.utilities.authentication_utils import get_hashcode, deserialize_user_object
from src.utilities.authorization import authorization
from src.model.message_format import MessageFormat

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# pylint: disable=broad-except
class UserManager():
    """
    Builder class for user authentication and authorization
    """
    def __init__(self):
        """
        Init class for initializing the cognito client
        """
        self._cognito_client = boto3.client(
            "cognito-idp",
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_ACCESS_KEY,
            region_name=REGION
        )

    def signup(self, user_details):
        """
        Signs up user for creating an account and sends otp to the user's email
        :params:
            :user_details: dict, containing required attributes of the user
        :returns:
            :dict, with email confirmation message
        """
        # check whether all values are present
        for attribute in ["email", "password", "name", "birthdate", "phone_number"]:
            if not user_details.get(attribute):
                return MessageFormat().error_message(f"{attribute} is not present")
        # fetch user information
        email = user_details["email"]
        password = user_details["password"]

        # create a dictionary for user attributes
        user_attributes = [{"Name": key, "Value": value} for key, value in user_details.items() \
                                    if key != "password"]

        # use cognito sdk for signing up
        try:
            self._cognito_client.sign_up(
                ClientId=CLIENT_ID,
                SecretHash=get_hashcode(email),
                Username=email,
                Password=password,
                UserAttributes=user_attributes,
                ValidationData=[{"Name": "email", "Value": email}]
            )
        except self._cognito_client.exceptions.UsernameExistsException:
            return MessageFormat().error_message("This username already exists")
        except self._cognito_client.exceptions.InvalidPasswordException:
            return MessageFormat().error_message("Password should have Caps, \
                                                    Special chars, Numbers")
        except self._cognito_client.exceptions.UserLambdaValidationException:
            return MessageFormat().error_message("Email already exists")
        except Exception as err:
            return MessageFormat().error_message(str(err))

        return MessageFormat().success_message(data=None,
                        message="Please confirm your signup, check Email for validation code")

    def confirm_signup(self, email, otp):
        """
        Confirm the user signup by verifying the otp
        :params:
            email: str, email of the user
            otp: str, unique verification code sent to the user's email
        :returns:
            None
        """
        try:
            self._cognito_client.confirm_sign_up(
                ClientId=CLIENT_ID,
                SecretHash=get_hashcode(email),
                Username=email,
                ConfirmationCode=otp,
                ForceAliasCreation=False
            )
        except self._cognito_client.exceptions.UserNotFoundException:
            return MessageFormat().error_message("Username doesnt exists")
        except self._cognito_client.exceptions.CodeMismatchException:
            return MessageFormat().error_message("Invalid Verification code")
        except self._cognito_client.exceptions.NotAuthorizedException:
            return MessageFormat().error_message("User is already confirmed", status_code=401)
        except Exception as err:
            return MessageFormat().error_message(f"Unknown error: {str(err)}")
        return MessageFormat().success_message(data=None)

    def initiate_auth(self, username, password):
        """
        initiates authentication for the user
        :params:
            username: str, email of the user
            password: str, password given by the user
        :returns:
            dictionary, with unique session details
        """
        secret_hash = get_hashcode(username)
        try:
            response = self._cognito_client.admin_initiate_auth(
                        UserPoolId=USER_POOL_ID,
                        ClientId=CLIENT_ID,
                        AuthFlow='ADMIN_NO_SRP_AUTH',
                        AuthParameters={
                            'USERNAME': username,
                            'SECRET_HASH': secret_hash,
                            'PASSWORD': password,
                        },
                        ClientMetadata={
                        'username': username,
                        'password': password,
                    })
        except self._cognito_client.exceptions.NotAuthorizedException:
            return None, "The username or password is incorrect"
        except self._cognito_client.exceptions.UserNotConfirmedException:
            return None, "User is not confirmed"
        except Exception as err:
            return None, err.__str__()

        return response, None

    def login(self, user_credentials):
        """
        Logs in user and returns session details
        :params:
           user_credentials: dictionary, consisting of
        email and password
        :returns:
            dictionary, session details
        """
        # check whether credentials are present
        for attribute in ["email", "password"]:
            if not user_credentials.get(attribute):
                return  MessageFormat().error_message(f"{attribute} is required")
        email = user_credentials["email"]
        password = user_credentials["password"]
        # initiate authentication flow
        response, message = self.initiate_auth(email, password)
        if message is not None:
            return MessageFormat().error_message(message)
        if response.get("AuthenticationResult"):
            data = {"id_token": response["AuthenticationResult"]["IdToken"],
                    "refresh_token": response["AuthenticationResult"]["RefreshToken"],
                    "access_token": response["AuthenticationResult"]["AccessToken"],
                    "expires_in": response["AuthenticationResult"]["ExpiresIn"],
                    "token_type": response["AuthenticationResult"]["TokenType"]}
            return MessageFormat().success_message(data=data)
        return MessageFormat().error_message("Unknown error occured")

    # def authorize_user(self, id_token):
    #     """
    #     authorizes user based on id_token
    #     :params:
    #         id_token: str, unique session id token for the logged in user
    #     :returns:
    #         dictionary, with the user claims object
    #     """
    #     json_web_keys = get_keys()
    #     headers = jwt.get_unverified_headers(id_token)
    #     jwk_index = find_public_key(headers["kid"], json_web_keys)
    #     if jwk_index == -1:
    #         return MessageFormat().error_message("Invalid authorization token.")

    #     # generate public key
    #     public_key = jwk.construct(json_web_keys[jwk_index])
    #     # verify public key
    #     if not verify_public_key(id_token, public_key):
    #         return MessageFormat().error_message("Signature verification failed.")
    #     logger.debug("Signature verification was successful.")
    #     # verify claims -- token expiration and audience
    #     claims = jwt.get_unverified_claims(id_token)
    #     if is_token_expired(claims):
    #         return MessageFormat().error_message("Token has expired.")
    #     if not is_audience_valid(claims):
    #         return MessageFormat().error_message("Token was not issued for the app.")
    #     logger.info("Authorization successful.")
    #     return MessageFormat().success_message(data={"claims": claims})

    def generate_new_token(self, refresh_token_details):
        """
        Generates new id_token and access_token from refresh token
        :params:
            refresh_token_credentials: dictionary, consisting of email and 
            refresh token
        :returns:
            dictionary, new id token and access token for the user
        """
        for attribute in ["email", "refresh_token"]:
            if not refresh_token_details.get(attribute):
                return MessageFormat().error_message(f"{attribute} is not present")
        email = refresh_token_details["email"]
        refresh_token = refresh_token_details["refresh_token"]
        try:
            response = self._cognito_client.initiate_auth(
                AuthParameters={
                    'USERNAME': email,
                    'SECRET_HASH': get_hashcode(email),
                    'REFRESH_TOKEN': refresh_token
                },
                ClientId=CLIENT_ID,
                AuthFlow='REFRESH_TOKEN_AUTH'
            )
            result = response['AuthenticationResult']
            if result:
                data = {
                    "id_token": result["IdToken"],
                    "access_token": result["AccessToken"], 
                    "expires_in": result["ExpiresIn"],
                    "token_type": result["TokenType"]
                }
                return MessageFormat().success_message(data=data)
        except self._cognito_client.exceptions.NotAuthorizedException:
            return MessageFormat().error_message("Invalid email/token", status_code=401)
        except self._cognito_client.exceptions.UserNotConfirmedException:
            return MessageFormat().error_message("User is not confirmed")
        except Exception as err:
            return MessageFormat().error_message(str(err))

    @authorization
    def get_user_details(self, token, email):
        """
        Fetches all cognito stored attributes
        for the user
        :params:
            email: str, unique email address for the user
            token: str, id token for the user
        :returns:
            dictionary, user details
        """
        if email is None or token is None:
            return MessageFormat().error_message("Email and Token are required.")
        try:
            response = self._cognito_client.admin_get_user(
                UserPoolId=USER_POOL_ID,
                Username=email
            )
            user = deserialize_user_object(response["UserAttributes"])
            return MessageFormat().success_message(data={"user": user})
        except self._cognito_client.exceptions.UserNotFoundException:
            return MessageFormat().error_message("Invalid username")
