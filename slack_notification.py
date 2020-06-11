import requests
import os


def post_slack(msg):
    api_token = os.environ.get('SLACK_API_TOKEN')
    api_url_base = 'https://slack.com/api/chat.postMessage'
    data = {
        "channel": '#noise-alert-tests',
        "text": msg
    }
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': f'Bearer {api_token}'
    }
    json = requests.post(url=api_url_base,headers=headers, json=data).json()

    return json['ok'] == 'true', json
