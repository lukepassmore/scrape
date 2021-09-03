"""
/usr/bin/python
"""

import requests
from api.utils.database import db
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.database import db, dynamodb
from api.utils.config import key
import jwt
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
import httplib2

"""
Analytics Query stuff
"""
class GoogleAnalytics():
    def get(headers,params):
        decoded = jwt.decode(headers['apiToken'], key, algorithms="HS256")
        userId = decoded['userId']
        view = dynamodb.Table('views').get_item(Key={'vid': headers['viewId'][0:4]})
        user = dynamodb.Table('users').get_item(Key={'uid': userId})

        if (headers['viewId'] == user['Item'][view['Item']['name']]):
            credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secrets.json', ['https://www.googleapis.com/auth/analytics.readonly'])
            
            #Create a service object
            http = credentials.authorize(httplib2.Http())
            service = build('analytics', 'v4', http=http, discoveryServiceUrl=('https://analyticsreporting.googleapis.com/$discovery/rest'))

            try:
                response = service.reports().batchGet(
                    body={
                        'reportRequests': [
                            {
                                'viewId': '278055805',
                                'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
                                'metrics': [{'expression': 'ga:sessions'}], 
                                'dimensions': [{"name": "ga:pagePath"}],
                                "filtersExpression":"ga:pagePath=~products;ga:pagePath!@/translate",
                                'orderBys': [{"fieldName": "ga:sessions", "sortOrder": "DESCENDING"}], 
                                'pageSize': 100
                            }]
                    }
                ).execute()
                return [1, response]
            except Exception as e:
                return [0, str(e), credentials]
                
                '''return {
                    "columnHeaders": [
                        {
                        "columnType": "DIMENSION",
                        "dataType": "STRING",
                        "name": "rt:pagePath"
                        },
                        {
                        "columnType": "METRIC",
                        "dataType": "INTEGER",
                        "name": "rt:pageviews"
                        }
                    ],
                    "id": "https://www.googleapis.com/analytics/v3/data/realtime?ids=ga:XXXXX",
                    "kind": "analytics#realtimeData",
                    "profileInfo": {
                        "accountId": "XXXX",
                        "internalWebPropertyId": "61947021XXXX",
                        "profileId": "XXXX",
                        "profileName": "home: Sites only",
                        "tableId": "realtime:XXXX",
                        "webPropertyId": "UA-XXXXX-X"
                    },
                    "query": {
                        "dimensions": "rt:pagePath",
                        "filters": "rt:pagePath=@404.html",
                        "ids": "ga:XXXXX",
                        "max-results": 1000,
                        "metrics": [
                        "rt:pageviews"
                        ],
                        "sort": [
                        "-rt:pageviews"
                        ]
                    },
                    "rows": [
                        [
                        "/404.html?page=/eyeblaster/addineyeV2-secure.html&from=http://www.google.com/",
                        "2"
                        ],
                        [
                        "/404.html?page=/amobee/a3d-ad-loader.html?",
                        "1"
                        ],
                        [
                        "/404.html?page=/amobee/a3d-ad-loader.html",
                        "1"
                        ],
                        [
                        "/404.html?page=/amobee/a3d-ad-loader.html?a3dWebglBanner=https",
                        "1"
                        ]
                    ],
                    "selfLink": "https://www.googleapis.com/analytics/v3/data/realtime?ids=",
                    "totalResults": 4,
                    "totalsForAllResults": {
                        "rt:pageviews": "5"
                    }
                }'''
        else:
            return response_with(resp.UNauthorIZED_401)

    def post(headers,params):
        decoded = jwt.decode(headers['apiToken'], key, algorithms="HS256")
        userId = decoded['userId']
        view = dynamodb.Table('views').get_item(Key={'vid': headers['viewId'][0:4]})
        user = dynamodb.Table('users').get_item(Key={'uid': userId})

        if (headers['viewId'] == user['Item'][view['Item']['name']]):
            credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secrets.json', ['https://www.googleapis.com/auth/analytics.readonly'])
            
            #Create a service object
            http = credentials.authorize(httplib2.Http())
            service = build('analytics', 'v4', http=http, discoveryServiceUrl=('https://analyticsreporting.googleapis.com/$discovery/rest'))

            try:
                response = service.reports().batchGet(
                    body={
                        'reportRequests': [
                            {
                                'viewId': '278055805',
                                'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
                                'metrics': [{'expression': 'ga:sessions'}], 
                                'dimensions': [{"name": "ga:pagePath"}],
                                "filtersExpression":"ga:pagePath=~products;ga:pagePath!@/translate",
                                'orderBys': [{"fieldName": "ga:sessions", "sortOrder": "DESCENDING"}], 
                                'pageSize': 100
                            }]
                    }
                ).execute()
                return [1, response]
            except Exception as e:
                return [0, str(e), credentials]

        else:
            return response_with(resp.UNauthorIZED_401)

    def AnalyticsApiTest():

        # property_id = "GA4-PROPERTY-ID"    
        client = BetaAnalyticsDataClient()

        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="city")],
            metrics=[Metric(name="activeUsers")],
            date_ranges=[DateRange(start_date="2020-03-31", end_date="today")],
        )

        response = client.run_report(request)
        return response.rows