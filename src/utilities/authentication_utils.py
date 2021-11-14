"""
util functions
"""

import hmac
import hashlib
import base64
import json
import logging
import time
from urllib import request
from jose.utils import base64url_decode
from src.constants.cognito_constants import *

def get_hashcode(username):
    """
    returns hashcode generated from username
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
    with request.urlopen(KEYS_URL) as fd:
        data = fd.read()
    return json.loads(data.decode('utf-8'))['keys']

def find_public_key(key_id, key_list):
    key_index = -1
    for idx in range(len(key_list)):
        if key_id == key_list[idx]["kid"]:
            key_index = idx
            break
    return key_index

def verify_public_key(token, public_key):
    # fetch the payload and signature from the token
    payload, base64_signature = str(token).rsplit('.', 1)
    # decode signature
    decoded_signature = base64url_decode(base64_signature.encode("utf-8"))
    # verify the signature
    return public_key.verify(payload.encode("utf-8"), decoded_signature)

def is_token_expired(claims):
    return time.time() > claims['exp']

def is_audience_valid(claims):
    return claims['aud'] == CLIENT_ID
