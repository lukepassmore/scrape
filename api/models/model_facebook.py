"""
/usr/bin/python
"""

import requests
from api.utils.database import db
from marshmallow import fields
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

"""
Analytics URI
"""
#analytics_uri = 'https://graph.facebook.com/'

"""
Analytics Query stuff
"""
class FacebookInsights():
    def get():
        #return requests.get(analytics_uri, {}).text
        return [
            {
                'data': 'data'
            }
        ]
    def FbInsightsTest():
        my_app_id = '<APP_ID>'
        my_app_secret = '<APP_SECRET>'
        my_access_token_1 = '<ACCESS_TOKEN_1>'
        my_access_token_2 = '<ACCESS_TOKEN_2>'
        proxies = {'http': '<HTTP_PROXY>', 'https': '<HTTPS_PROXY>'} # add proxies if needed

        session1 = FacebookSession(
            my_app_id,
            my_app_secret,
            my_access_token_1,
            proxies,
        )

        session2 = FacebookSession(
            my_app_id,
            my_app_secret,
            my_access_token_2,
            proxies,
        )

        api1 = FacebookAdsApi(session1)
        api2 = FacebookAdsApi(session2)