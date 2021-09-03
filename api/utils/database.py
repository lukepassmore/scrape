"""
/usr/bin/python
"""

from flask import Flask
from flask_dynamo import Dynamo
import boto3

db = ''
dynamodb = boto3.resource(
                            'dynamodb',
                            aws_access_key_id='AKIA6DCE6TBEYQJUQBUM',
                            aws_secret_access_key='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',
                            region_name='eu-west-1'
                        )