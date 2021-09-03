"""
/usr/bin/python
"""

import base64
import cryptography
from flask import Flask
from flask_dynamo import Dynamo
from datetime import datetime
from datetime import timedelta
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

"""
Define global apiKey
       token expiry 
       86400 = 24 hours
       1200 = 20 minutes
"""
key = "f4379a7f-3635-446c-bd25-6a0bc36f21b5"
expiryTime = datetime.utcnow() + timedelta(seconds=1200)

"""
Define global pwKey
        to store in keyfile
"""
pwKey = 'LXT0gQSNN7Amk4eApM10xPj-B-EW5qAYzvkRqHHVBHQ='
#pwKey = Fernet.generate_key()
#file = open('./utils/key.key', 'wb')
#file.write(pwKey)
#file.close()

class Encryption ():
    def encryptPassword(string):
        encoded = string.encode()
        f = Fernet(pwKey)
        return f.encrypt(encoded)

    def decryptPassword(string):
        f = Fernet(pwKey)
        decrypted = f.decrypt(string)
        return decrypted.decode()

class Config(object):
    DEBUG = False
    TESTING = False
    DYNAMO_ENABLE_LOCAL = False
    #DYNAMO_LOCAL_HOST = 'localhost'
    #DYNAMO_LOCAL_PORT = 8000

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True