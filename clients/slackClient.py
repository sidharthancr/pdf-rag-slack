import requests
import json
import os
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)

"""
    Sends a message to a specified Slack channel using the Slack API.

    :param channel_id: The ID of the Slack channel to send the message to.
    :param message: The message text to send.
"""
def post_message_to_slack(channel_id, message):
   
    if not channel_id or not message:
        logging.error("Channel ID and message must be provided.")
        return

    slack_token = os.getenv('SLACK_TOKEN')
    if not slack_token:
        logging.error("SLACK_TOKEN environment variable is not set.")
        return

    url = "https://slack.com/api/chat.postMessage"
    payload = json.dumps({"channel": channel_id, "text": message})
    headers = {'Authorization': f'Bearer {slack_token}', 'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Check for HTTP errors.
        response_data = response.json()
        if not response_data.get('ok'):
            logging.error(f"Slack API error: {response_data.get('error', 'Unknown error')}")
            return
        return response_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Slack request failed: {e}")