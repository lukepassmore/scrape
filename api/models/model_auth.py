"""
/usr/bin/python
"""

import requests
from flask import jsonify
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.database import db, dynamodb
from api.utils.config import key, expiryTime, Encryption
import jwt

"""
Encoding and decoding things
"""
class Auth():
    def create(apiKey,userId,viewId):
        view = dynamodb.Table('views').get_item(Key={'vid': viewId[0:4]})
        viewName = view['Item']['name']
        user = dynamodb.Table('users').get_item(Key={'uid': userId})

        #databasePassword = Encryption.decryptPassword(user['Item']['password'].value)
        if (viewId == user['Item'][viewName]):
            token = jwt.encode({"userId": userId, "exp": expiryTime}, key, algorithm="HS256")
            
            dynamodb.Table('users').update_item(Key={'uid': userId},
                UpdateExpression="SET apiToken = :updated",
                ExpressionAttributeValues={':updated': token}
            )

            return token
        else:
            return response_with(resp.UNauthorIZED_401)

    def check(apiKey,apiToken):
        decoded = jwt.decode(apiToken, key, algorithms="HS256")
        uid = decoded['userId']
        user = dynamodb.Table('users').get_item(Key={'uid': uid})
        uid = user['Item']['uid']
        if (uid):
            return uid
        

    def login(apiKey,userId,viewId):
        view = dynamodb.Table('views').get_item(Key={'vid': viewId[0:4]})
        viewName = view['Item']['name']
        user = dynamodb.Table('users').get_item(Key={'uid': userId})

        #databasePassword = Encryption.decryptPassword(user['Item']['password'].value)
        if (viewId == user['Item'][viewName]):
            token = jwt.encode({"userId": userId, "exp": expiryTime}, key, algorithm="HS256")

            dynamodb.Table('users').update_item(Key={'uid': userId},
                UpdateExpression="SET apiToken = :updated",
                ExpressionAttributeValues={':updated': token}
            )

            user['Item']['apiToken'] = token
            return user['Item']
        else:
            return response_with(resp.UNauthorIZED_401)