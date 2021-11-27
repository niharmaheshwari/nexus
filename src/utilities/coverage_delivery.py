'''
Helper routine for writing the coverage to S3
'''
import boto3
import os

fs = boto3.client('s3')
for root, dirs, files in os.walk('test/coverage', topdown=False):
    for name in files:
        fs.upload_file(
            root + '/' + name,
            'snippets-s',
            root + '/' + name
        )

