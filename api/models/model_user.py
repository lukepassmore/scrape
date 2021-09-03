"""
/usr/bin/python
"""

from api.utils.responses import response_with
from api.utils import responses as resp
from uuid import uuid1, uuid4
from api.utils.database import db, dynamodb
from api.utils.config import key, expiryTime, Encryption
from marshmallow import fields
import jwt

"""
User query stuff
"""
class User():
    def get(uid):
        user = dynamodb.Table('users').get_item(Key={'uid': uid})
        user['Item']['apiToken'] = ''
        return user['Item']
        
    def post(user):
        #user['active'] = 0
        view = dynamodb.Table('views').get_item(Key={'vid': user['view']})
        user['viewName'] = view['Item']['name']

        user['userId'] = uuid4().int
        user['viewId'] = user['view'] + '-' + uuid4().hex
        user['apiToken'] = jwt.encode({"userId": user['userId'], "exp": expiryTime}, key, algorithm="HS256")
        #encryptedPassword = Encryption.encryptPassword(user['password'])
        try:
            dynamodb.Table('users').put_item(Item= {
                'uid': user['userId'],
                'cid': user['cid'],
                'first_name': user['firstName'],
                'last_name': user['lastName'],
                'email': user['email'],
                #'password': encryptedPassword,
                user['viewName']: user['viewId'],
                'apiToken': user['apiToken'],
                'phone': user['phone'],
                'active': user['active']
            })
            return user
        except Exception:
            return response_with(resp.CONFLICT_409)
        
    def update(user):        
        #encryptedPassword = Encryption.encryptPassword(user['password'])
        try:
            dynamodb.Table('users').update_item(Key={'uid': user['userId']},
                UpdateExpression="SET cid = :cid, first_name = :first_name, last_name = :last_name, email = :email, phone = :phone, active = :active",
                ExpressionAttributeValues={
                    ':cid': user['cid'],
                    ':first_name': user['firstName'],
                    ':last_name': user['lastName'],
                    ':email': user['email'],
                    ':phone': user['phone'],
                    ':active': user['active']
                }
            )
            
            user['apiToken'] = ''
            return user
        except Exception:
            return response_with(resp.INVALID_INPUT_422)

    def delete(uid):
        return dynamodb.Table('users').delete_item(Key={'uid': uid})

"""
Company query stuff
"""
class Company():
    def get(cid):
        company = dynamodb.Table('companies').get_item(Key={'cid': cid})
        return company['Item']
        
    def post(company):        
        company['cid'] = uuid4().int
        # try exept here throws an error so temporarily removed
        dynamodb.Table('companies').put_item(Item= {
            'cid': company['cid'],
            'company_name': company['company_name'],
            'company_address': company['company_address'],
            'company_email': company['company_email'],
            'company_number': company['company_number']
        })
        return company

    def update(company):
        try:
            dynamodb.Table('companies').update_item(Key={'cid': company['cid']},
                UpdateExpression="SET company_name = :company_name, company_address = :company_address, company_email = :company_email, company_number = :company_number",
                ExpressionAttributeValues={
                    ':company_name': company['company_name'],
                    ':company_address': company['company_address'],
                    ':company_email': company['company_email'],
                    ':company_number': company['company_number']
                }
            )
            return company
        except Exception:
            return response_with(resp.INVALID_INPUT_422)

    def delete(cid):
         return dynamodb.Table('companies').delete_item(Key={'cid': cid})