# viz-of-the-day-slack
Get Tableau Public's Viz of the Day as a slack message on weekdays.

# How to creat a Viz of the Day Slack App
## Creating a Slack App
1. Create a Slack App with these requirements
  - Bot Token Scopes: chat:write
  - If you'd like to use the Tableau logo for your app icon, I've attached an image file that is compatible for this purpose.
2. Install your Slack App to get Bot User OAuth Access Token
3. Create a python script to post data from the VOTD API to Slack using the Slack API.

## Using a Cloud Function on GCP
I wanted to make mine fully automated, so I chose to deploy the main.py file in this repo as a Cloud Function on Google Cloud.
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

## Using a Lambda Function on AWS
If you prefer using AWS over GCP, I also included AWS-Lambda-Function_votd-slack.py file in this repo to use as a Lambda Function on AWS. (note: instead of using Botocore, you will need to bundle dependencies with your Lambda function. I found this tutorial quite helpful: https://www.youtube.com/watch?v=rDbxCeTzw_k)
4. Create a Lambda Function with:
  - Author from scratch
  - Runtime: Python 3.7
  - Execution role: Create a new role with basic Lambda permissions
5. Add trigger to Lambda created above:
  - EventBridge
  - Rule: Create a new rule
  - Rule name: votd_scheduler
  - Rule type: Schedule expression
  - Schedule expression: (Any cron schedule you want, but VOTD is only posted on weekdays. I'd suggest 0 7 ? * MON-FRI *)
  - Check box for "Enable trigger"
