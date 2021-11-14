"""
util functions
"""

import hmac
import hashlib
import base64
import json
<<<<<<< HEAD
import time
from urllib import request
from jose.utils import base64url_decode
from src.constants.cognito_constants import CLIENT_ID, CLIENT_SECRET, KEYS_URL
from src.model.user import User

def get_hashcode(username):
    """
    Returns  a secret hashcode using hmac
    :params:
        username: str, email address of the user
    :returns:
        string, unique hashcode for the user
=======
import logging
import time
from urllib import request
from jose.utils import base64url_decode
from src.constants.cognito_constants import *

def get_hashcode(username):
    """
    returns hashcode generated from username
>>>>>>> 9f88c199bb488cc6e1c03c837400ecddc68b9943
    """
    msg = username + CLIENT_ID
    encoded_msg = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    decoded_msg = base64.b64encode(encoded_msg).decode()
    return decoded_msg

def get_keys():
    """
    Fetch keys from cognito url
    """
<<<<<<< HEAD
    with request.urlopen(KEYS_URL) as file_descriptor:
        data = file_descriptor.read()
    return json.loads(data.decode('utf-8'))['keys']

def find_public_key(key_id, key_list):
    """
    Find the key_id in the list of keys associated with
    cognito
    :params:
        key_id: string, key_id extracted from the id_token
        key_list: list, list of keys in cognito associated with users
    :returns:
        key_index: int, index of the key within key_list
    """
    key_index = -1
    for idx, _ in enumerate(key_list):
=======
    with request.urlopen(KEYS_URL) as fd:
        data = fd.read()
    return json.loads(data.decode('utf-8'))['keys']

def find_public_key(key_id, key_list):
    key_index = -1
    for idx in range(len(key_list)):
>>>>>>> 9f88c199bb488cc6e1c03c837400ecddc68b9943
        if key_id == key_list[idx]["kid"]:
            key_index = idx
            break
    return key_index

def verify_public_key(token, public_key):
<<<<<<< HEAD
    """
    Verifies whether the token and public key matches the ones stored
    in cognito
    :params:
        token: string, id_token associated with the user
        public_key: str, public key extracted from the token
    :returns:
        bool, whether the verification is successful or not
    """
=======
>>>>>>> 9f88c199bb488cc6e1c03c837400ecddc68b9943
    # fetch the payload and signature from the token
    payload, base64_signature = str(token).rsplit('.', 1)
    # decode signature
    decoded_signature = base64url_decode(base64_signature.encode("utf-8"))
    # verify the signature
    return public_key.verify(payload.encode("utf-8"), decoded_signature)

def is_token_expired(claims):
<<<<<<< HEAD
    """
    Checks whether the session id_token has expired
    :params:
        claims: dictionary, claims made bu the token
    :returns:
        bool, whether the token has expired or not
    """
    return time.time() > claims['exp']

def is_audience_valid(claims):
    """
    Checks whether the application is correct for the token
    :params:
        claims: dictionary, claims made bu the token
    :returns:
        bool, whether the application is correct or not
    """
    return claims['aud'] == CLIENT_ID

def serialize_user_object(user):
    """
    Serializes user object to return a dictionary
    :params:
        user: User() class object
    """
    serialized_response = []
    user_getter_handlers = {
        "sub": user.get_user_id(),
        "email": user.get_email(),
        "name": user.get_name(),
        "phone_number": user.get_phone_number(),
        "birthdate": user.get_birth_date()
    }
    for key, value in user_getter_handlers.items():
        serialized_response.append({"Name": key, "Value": value})
    return serialized_response

def deserialize_user_object(user_details):
    """
    Converts the json to User class object
    :params:
        user_details: list, containing attributes of the form
        {"Name": <attr_name>, "Value": <value>}
    """
    user = User()
    user_setter_handlers = {
        "sub": user.set_user_id,
        "email": user.set_email,
        "name": user.set_name,
        "phone_number": user.set_phone_number,
        "birthdate": user.set_birth_date
    }
    for field in user_details:
        if field["Name"] in user_setter_handlers:
            user_setter_handlers[field["Name"]](field["Value"])
    return user
=======
    return time.time() > claims['exp']

def is_audience_valid(claims):
    return claims['aud'] == CLIENT_ID
>>>>>>> 9f88c199bb488cc6e1c03c837400ecddc68b9943
