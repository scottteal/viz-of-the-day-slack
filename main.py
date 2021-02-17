import requests
import json
import os

SLACK_TOKEN = os.environ['SLACK_TOKEN']

votd_url = "https://public.tableau.com/s/api/votd"
response = requests.get(votd_url).json()
description = response["nodes"][0]["node"]["description"]
title = response["nodes"][0]["node"]["title"]
image_src = response["nodes"][0]["node"]["field_image"]["src"]
url_path = response["nodes"][0]["node"]["path"]

blocks = [{
            "type": "section",
             "text": {
                 "type": "mrkdwn",
                 "text": '*' + title + '*\n ' + description
         }
        },
        {
            "type": "image",
             "image_url": image_src,
             "alt_text": "inspiration"
        },
        {
            "type": "divider"
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "See the viz",
                    },
                    "url": 'https://public.tableau.com' + url_path + '?referrer=slack'
                }
            ]
        }
    ]

def post_votd_to_slack(request):
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': SLACK_TOKEN,
        'channel': '#viz-of-the-day-test',
        'blocks': json.dumps(blocks) if blocks else None
    }).json()
