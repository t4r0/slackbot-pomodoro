import requests
import sys
import os
import json

USER_TOKEN_STRING = os.environ['SLACK_USER_TOKEN_STRING']
URL_TOKEN_STRING = os.environ['SLACK_URL_TOKEN_STRING']

HASH  = "%88"

channel_name = sys.argv[1]

params = {'token': USER_TOKEN_STRING}

response = requests.get('https://slack.com/api/channel.list', params=params)
channels = json.loads(response.text, encoding='utf-8')['channels']

for channel in channels:
    if channel['name'] == channel_name:
        print channel['id']
        break
        
