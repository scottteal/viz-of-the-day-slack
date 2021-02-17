# viz-of-the-day-slack
Get Tableau Public's Viz of the Day as a slack message on weekdays.

1. Create a Slack App with these requirements
  - Bot Token Scopes: chat:write
  - If you'd like to use the Tableau logo for your app icon, I've attached an image file that is compatible for this purpose.
2. Install your Slack App to get Bot User OAuth Access Token
3. Create a python script to post data from the VOTD API to Slack using the Slack API. (note: I wanted to make mine fully automated, so I chose to deploy the main.py file in this repo as a Cloud Function on Google Cloud. You could conceivably host the script however you'd like.)
4. Create a Cloud Function with:
  - Trigger: HTTP
  - Slack Bot User OAuth Access Token as a Runtime Environment Variable 'SLACK_TOKEN'
  - Runtime: Python 3.7
  - Entry point: post_votd_to_slack
5. Create a Cloud Scheduler job:
  - Frequency: 0 7 * * 1-5
  - Time zone: Whatever your preferred timezone is (note: depending on your timezone, you may receive VOTD that is one day old)
  - URL: The HTTP endpoint for the Cloud Function you just created
  - HTTP Method: POST
