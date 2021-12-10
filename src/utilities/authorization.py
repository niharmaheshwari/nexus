"""
User authorization decorator
"""

from flask import request
from jose import jwk, jwt
from src.utilities.authentication_utils import get_keys, find_public_key, is_audience_valid, \
    is_token_expired, verify_public_key
from src.model.message_format import MessageFormat
import src.utilities.logging as log

logger = log.get_logger(__name__)

def authorization(func):
    """
    Decorator for authorizing function with user email and token
    """
    def authorizer(*args, **kwargs):
        """
        Authorizer wrapper over the function. Checks whether the user is
        authorized or not.
        """
        id_token = request.headers.get("token", None)
        if id_token is None:
            return MessageFormat().error_message("Token not present/Invalid token.")
        json_web_keys = get_keys()
        headers = jwt.get_unverified_headers(id_token)
        # check if key id exists in cognito
        jwk_index = find_public_key(headers["kid"], json_web_keys)
        if jwk_index == -1:
            return MessageFormat().error_message("Invalid authorization token.")

        # generate public key
        public_key = jwk.construct(json_web_keys[jwk_index])
        # verify public key
        if not verify_public_key(id_token, public_key):
            return MessageFormat().error_message("Signature verification failed.")
        logger.debug("Signature verification was successful.")
        # verify claims -- token expiration and audience
        claims = jwt.get_unverified_claims(id_token)
        if is_token_expired(claims):
            return MessageFormat().error_message("Token has expired.")
        if not is_audience_valid(claims):
            return MessageFormat().error_message("Token was not issued for the app.")
        logger.info("Authorization successful.")
        return func(*args, **kwargs)
    return authorizer
