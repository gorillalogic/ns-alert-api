import requests
import os


def post_slack(msg):
    channel = os.environ.get('SLACK_CHANNEL')
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    data = {
        "channel": channel,
        "text": msg
    }
    json = requests.post(url=webhook_url, json=data).json()

    return json['ok'] == 'true', json
