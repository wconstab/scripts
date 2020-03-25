### Requirements
bs4
browser_cookie3
numpy
json
requests

### Usage
Log into amazon in Chrome, prepare a Wholefoods order, get to the point in checkout where there are 'no delivery slots available'.
Use Chrome developer tools to find the request headers that were used to load that delivery schedule page.  Save the headers to a json file.

python3 wf_bot.py --amazon_request_headers_file <path_to_json> --pushover_api_key <key> --pushover_user_key <key>

Currently assumes pushover account for notifications, but could make this optional
