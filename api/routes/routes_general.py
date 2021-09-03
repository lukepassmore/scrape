"""
/usr/bin/python
"""

from flask import Flask, g
from flask_dynamo import Dynamo
from api.utils.database import db, dynamodb
from flask import Blueprint
from flask import request
import simplejson as json
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.model_auth import Auth
from api.models.model_user import User, Company
from api.models.model_properties import Properties
from api.models.model_google_analytics import GoogleAnalytics
from api.models.model_google_search_console import GoogleSearchConsole
from api.models.model_facebook import FacebookInsights

route_path_general = Blueprint("route_path_general", __name__)

@route_path_general.before_request
def before_request():
    """
    Request Token
    """
    if request.method != 'OPTIONS':

        #replace this with a more elegant solution
        if request.endpoint == 'route_path_general.create_user' or request.endpoint == 'route_path_general.create_company' or request.endpoint == 'route_path_general.database' or request.endpoint == 'route_path_general.request_token' or request.endpoint == 'route_path_general.login_user' or request.endpoint == 'route_path_general.check_token':
            return

        #elif request.endpoint == 'route_path_general.create_user' or request.endpoint == 'route_path_general.create_company' or request.endpoint == 'route_path_general.database':
        #    return

        else:
            try:
                apiKey = request.headers['apiKey']
                apiToken = request.headers['apiToken']
                Auth.check(apiKey,apiToken)
                return
            except Exception:
                return response_with(resp.UNauthorIZED_401)

"""
Build Database
Remember to disable this before prod...
"""
@route_path_general.route('config/database', methods=['GET'])
def database():
    try:
        response = dynamodb.Table('users').get_item(Key={'uid': 57})
        return response_with(resp.SUCCESS_200, value={"database": response})
    except Exception:
       return response_with(resp.INVALID_INPUT_422, value={"users": "Could not fetch users!"})

"""
Request Token
"""
@route_path_general.route('auth/request', methods=['POST'])
def request_token():
    try:
        apiKey = request.headers['apiKey']
        viewId = request.headers['viewId']
        body = request.get_json()
        userId = body['userId']

        token = Auth.create(apiKey,userId,viewId)
        return response_with(resp.SUCCESS_200, value={"apiToken": token})
    except Exception:
        return response_with(resp.UNauthorIZED_401)

"""
Check Token
"""
@route_path_general.route('auth/check', methods=['POST'])
def check_token():
    try:
        apiKey = request.headers['apiKey']
        apiToken = request.headers['apiToken']

        response = Auth.check(apiKey,apiToken)
        return response_with(resp.SUCCESS_200, value={"data": response})
    except Exception:
        return response_with(resp.UNauthorIZED_401)

"""
Login
"""
@route_path_general.route('auth/login', methods=['POST'])
def login_user():
    try:
        apiKey = request.headers['apiKey']
        viewId = request.headers['viewId']
        body = request.get_json()
        userId = body['userId']

        result = Auth.login(apiKey,userId,viewId)
        return response_with(resp.SUCCESS_200, value={"user": result})
    except Exception:
        return response_with(resp.UNauthorIZED_401)

"""
Get user
"""
@route_path_general.route('users/<int:uid>', methods=['GET'])
def get_user_detail(uid):
    try:
        response = User.get(uid)
        return response_with(resp.SUCCESS_200, value={"data": response})
    except Exception:
        return response_with(resp.DATASTORE_ERROR_404)

"""
Create user
"""
@route_path_general.route('users', methods=['POST'])
def create_user():
    try:
        body = request.get_json()
        apiFunctionParams = body['apiFunctionParams']
        result = User.post(apiFunctionParams)
        return response_with(resp.SUCCESS_200, value={"user": result})
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

"""
Update user
"""
@route_path_general.route('users', methods=['PATCH'])
def update_user():
    try:
        body = request.get_json()
        apiFunctionParams = body['apiFunctionParams']
        result = User.update(apiFunctionParams)
        return response_with(resp.SUCCESS_200, value={"data": result})
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

"""
Delete user
"""
@route_path_general.route('users/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    try:
        response = User.delete(uid)
        return response_with(resp.SUCCESS_200)
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

"""
Get Company
"""
@route_path_general.route('companies/<int:cid>', methods=['GET'])
def get_company_detail(cid):
    try:
        response = Company.get(cid)
        return response_with(resp.SUCCESS_200, value={"data": response})
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

"""
Create Company
"""
@route_path_general.route('companies', methods=['POST'])
def create_company():
    try:
        body = request.get_json()
        apiFunctionParams = body['apiFunctionParams']
        result = Company.post(apiFunctionParams)
        return response_with(resp.SUCCESS_200, value={"data": result})
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

"""
Update Company
"""
@route_path_general.route('companies', methods=['PATCH'])
def update_company():
    try:
        body = request.get_json()
        apiFunctionParams = body['apiFunctionParams']
        result = Company.update(apiFunctionParams)
        return response_with(resp.SUCCESS_200, value={"data": result})
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

"""
Delete Company
"""
@route_path_general.route('companies/<int:cid>', methods=['DELETE'])
def delete_company(cid):
    try:
        response = Company.delete(cid)
        return response_with(resp.SUCCESS_200)
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

"""
Google Analytics Properties
"""
@route_path_general.route('connector/google/analytics', methods=['GET'])
def get_google_analytics():
    try:
        body = request.get_json()
        apiFunctionParams = body['apiFunctionParams']
        headers = request.headers
        response = GoogleAnalytics.get(headers,apiFunctionParams)
        if response[0] == 1:
            r = response_with(resp.SUCCESS_200, value={"data": response[1]})
        elif response[0] == 0:
            r = response_with(resp.EXTERNAL_403, value={"error": response[1]})
        return r
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

"""
Google Analytics Request
"""
@route_path_general.route('connector/google/analytics', methods=['POST'])
def gpost_google_analytics():
    try:
        body = request.get_json()
        apiFunctionParams = body['apiFunctionParams']
        headers = request.headers
        response = GoogleAnalytics.post(headers,apiFunctionParams)
        if response[0] == 1:
            r = response_with(resp.SUCCESS_200, value={"data": response[1]})
        elif response[0] == 0:
            r = response_with(resp.EXTERNAL_403, value={"error": response[1]})
        return r
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

"""
Google search console
"""
@route_path_general.route('connector/google/search', methods=['POST'])
def get_google_search_console():
    try:
        response = GoogleSearchConsole.get()
        return response_with(resp.SUCCESS_200, value={"data": response})
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

"""
Facebook insights
"""
@route_path_general.route('connector/facebook/insights', methods=['POST'])
def get_facebook_insights():
    try:
        response = FacebookInsights.get()
        return response_with(resp.SUCCESS_200, value={"data": response})
    except Exception:
        return response_with(resp.INVALID_INPUT_422)