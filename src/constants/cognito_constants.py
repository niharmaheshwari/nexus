"""
Constants for cognito
"""
USER_POOL_ID = 'us-east-2_iV4OqMaB3'
CLIENT_ID = '89c4peguvnl94r51sgekgqiag'
CLIENT_SECRET = 'kg7rdng88t07piqsdt1a3utjsoidcs6il6vs0ldadb6qrlfk0sq'
<<<<<<< HEAD
ACCESS_KEY = '<access-key>'
SECRET_ACCESS_KEY = '<secret-access-key>'
REGION = 'us-east-2'
KEYS_URL = f"https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"
=======
ACCESS_KEY = 'AKIAVYPI7GZ66577MKNF'
SECRET_ACCESS_KEY = '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'
REGION = 'us-east-2'
KEYS_URL="https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json".format(REGION, USER_POOL_ID)
>>>>>>> 9f88c199bb488cc6e1c03c837400ecddc68b9943
