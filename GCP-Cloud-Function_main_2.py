import requests
import json
import os
import re

SLACK_TOKEN = os.environ['SLACK_TOKEN']
SLACK_CHANNEL = '#viz-of-the-day'

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

votd_url = "https://public.tableau.com/api/gallery?page=0&count=1&galleryType=viz-of-the-day"
response = requests.get(votd_url).json()
title = response["items"][0]["title"]
author = response["items"][0]["authorName"]
image_src = response["items"][0]["screenshot"]
url_path = response["items"][0]["gallerySlug"]
view_count = response["items"][0]["workbook"]["viewCount"]
num_favorites = response["items"][0]["workbook"]["numberOfFavorites"]

#need to clean the html out of the description field
description = response["items"][0]["description"]
description = cleanhtml(description)
description = description.replace("\n","")

blocks = [{
            "type": "section",
             "text": {
                 "type": "mrkdwn",
                 "text": '*' + title + '*\n by ' + author + '\n :eyes: ' + str(f'{view_count:,}') + ' views\n :star: ' + str(f'{num_favorites:,}') + ' favorites\n ' + description
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
                        "text": "See the viz"
                    },
                    "url": 'https://public.tableau.com/gallery/' + url_path + '?referrer=slack'
                }
            ]
        }
    ]

def post_votd_to_slack(request):
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': SLACK_TOKEN,
        'channel': SLACK_CHANNEL,
        'blocks': json.dumps(blocks) if blocks else None,
        'text': title
    }).json()
