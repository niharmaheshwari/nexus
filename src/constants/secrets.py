import os

def safe_get(env_var):
    '''
    Attempt to safely get the value of the environment variable passed
    :params:
        env_var : The envrionment variable requested
    '''
    val = None # Default Value
    try:
        val = os.environ[env_var]
    except KeyError:
        pass
    return val

USER_POOL_ID = safe_get('USER_POOL_ID')
CLIENT_ID = safe_get('CLIENT_ID')
CLIENT_SECRET = safe_get('CLIENT_SECRET')
ACCESS_KEY = safe_get('ACCESS_KEY')
SECRET_ACCESS_KEY = safe_get('SECRET_ACCESS_KEY')
REGION = safe_get('REGION')
KEYS_URL = safe_get('KEYS_URL')