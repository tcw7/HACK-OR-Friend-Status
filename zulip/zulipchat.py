# Module to return user presence in Zulip (zulip.com)

import zulip

client = zulip.Client(config_file="./.zuliprc")

def get_user_status(user_email):
    result = client.get_user_presence(user_email)
    return result["presence"]["aggregated"]["status"]

