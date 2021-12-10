'''
Helper routine for writing the coverage to S3
'''
import os
import boto3
import src.utilities.logging as log

logger = log.get_logger(__name__)

session = boto3.Session(
    aws_access_key_id=os.environ['ACCESS_KEY'],
    aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
)
fs = session.client('s3')

for root, dirs, files in os.walk('test/coverage', topdown=False):
    for name in files:
        fs.upload_file(
            root + '/' + name,
            'snippets-s',
            root + '/' + name
        )
