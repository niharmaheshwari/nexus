from opensearchpy import OpenSearch, RequestsHttpConnection
import json
# import boto3
from src.constants.secrets import ACCESS_KEY
from requests_aws4auth import AWS4Auth


print("HELLO WORLD")
print(ACCESS_KEY)


REGION = "us-east-2"
SERVICE = "es"
# creds = boto3.Session(ACCESS_KEY, SECRET_KEY, region_name=REGION).get_credentials()
#
# awsauth = AWS4Auth(creds.access_key, creds.secret_key, REGION, SERVICE, session_token=creds.token)