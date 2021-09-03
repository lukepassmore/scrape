"""
/usr/bin/python
"""

import requests
from api.utils.database import db
from marshmallow import fields

"""
Use query stuff
"""
class Properties():
    def get(userId,connector):
        return [
            {
                'data': 'data'
            }
        ]