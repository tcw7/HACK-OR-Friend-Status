
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / 'env' / '.env'

load_dotenv(dotenv_path=env_path)

client = WebClient(token=os.environ['SLACK_USER_TOKEN'])


def get_user_id(user_email):
    try:
        response = client.users_lookupByEmail(email=user_email)
        response = response['user']['id']
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}")
    return response


def get_user_status(user_id):
    try:
        response = client.users_getPresence(user=user_id)
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}")
    return response


