"""
/usr/bin/python
"""

from flask import make_response, jsonify

SUCCESS_200 = {
    'http_code': 200,
    'code': 'Success'
}

BAD_REQUEST_400 = {
    "http_code": 400,
    "code": "badRequest",
    "message": "Bad request"
}

UNauthorIZED_401 = {
    "http_code": 401,
    "code": "notauthorized",
    "message": "You are not allowed to do that."
}

UNuserIZED_403 = {
    "http_code": 403,
    "code": "notuserized",
    "message": "You are not allowed to do that."
}

EXTERNAL_403 = {
    "http_code": 403,
    "code": "externalForbidden",
    "message": "External connector disallowed the request."
}

NOT_FOUND_HANDLER_404 = {
    "http_code": 404,
    "code": "notFound",
    "message": "There is no such handler."
}

DATASTORE_ERROR_404 = {
    "http_code": 404,
    "code": "notFound",
    "message": "Record not found in datastore."
}

CONFLICT_409 = {
    "http_code": 409,
    "code": "recordConflict",
    "message": "Record already exists."
}

INVALID_FIELD_NAME_SENT_422 = {
    "http_code": 422,
    "code": "invalidField",
    "message": "Not all field names are valid."
}

INVALID_INPUT_422 = {
    "http_code": 422,
    "code": "invalidInput",
    "message": "Invalid input."
}

MISSING_PARAMETERS_422 = {
    "http_code": 422,
    "code": "missingParameter",
    "message": "Missing parameters."
}

SERVER_ERROR_500 = {
    "http_code": 500,
    "code": "serverError",
    "message": "Server error"
}


def response_with(response, value=None, message=None, error=None, headers={}, pagination=None):
    result = {}
    if value is not None:
        result.update(value)

    if response.get('message', None) is not None:
        result.update({'message': response['message']})

    result.update({'code': response['code']})

    if error is not None:
        result.update({'errors': error})

    if pagination is not None:
        result.update({'pagination': pagination})

    headers.update({'Access-Control-Allow-Origin': '*'})
    headers.update({'server': 'Yellow Box Software API'})

    return make_response(jsonify(result), response['http_code'], headers)
