import requests
import json
"""
Sign up for a free trial and generate an API key at pushover.net
Would have to pay for continued use.
"""

class PushoverNotifier(object):
    def __init__(self, config):
        with open(config, 'r') as f:
            config_data = json.load(f)

        self.user_key = config_data['user_key']
        self.api_key = config_data['api_key']
        self.api_url = config_data['api_url']
    
    def notify(self, message):
        """ POST an HTTPS request to https://api.pushover.net/1/messages.json with the following parameters:
            
                token (required) - your application's API token
                user (required) - the user/group key (not e-mail address) of your user (or you), viewable when logged into our dashboard (often referred to as USER_KEY in our documentation and code examples)
                message (required) - your message
            
            Some optional parameters may be included:

                attachment - an image attachment to send with the message; see attachments for more information on how to upload files
                device - your user's device name to send the message directly to that device, rather than all of the user's devices (multiple devices may be separated by a comma)
                title - your message's title, otherwise your app's name is used
                url - a supplementary URL to show with your message
                url_title - a title for your supplementary URL, otherwise just the URL is shown
                priority - send as -2 to generate no notification/alert, -1 to always send as a quiet notification, 1 to display as high-priority and bypass the user's quiet hours, or 2 to also require confirmation from the user
                sound - the name of one of the sounds supported by device clients to override the user's default sound choice
                timestamp - a Unix timestamp of your message's date and time to display to the user, rather than the time your message is received by our API
        """
        data = dict(token=self.api_key, 
                    user=self.user_key, 
                    message=message)
        resp = requests.post(self.api_url, data=data)
        resp.raise_for_status()