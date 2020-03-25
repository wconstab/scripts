### Requirements
bs4
browser_cookie3
numpy
json
requests

### Usage
Log into amazon in Chrome, prepare a Wholefoods order, get to the point in checkout where there are 'no delivery slots available'.

Edit pushover_config.json.template with your own keys, or skip it.

python3 wf_bot.py --pushover_config <pushover_config.json> 
Currently assumes pushover account for notifications, but could make this optional
