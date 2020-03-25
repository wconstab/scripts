# pip3 install browser-cookie3 
import browser_cookie3 
import json
import numpy
import requests 
import time
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from pushover import PushoverNotifier


def fetch_delivery_url(amazon_request_headers):
    """
    TODO: remove manually entered cookie/session info as much as possible
        - removing 'cookie' from headers seems to work as long as cookie jar is used
        - probably referer is going to be harder to fix?
    """
    delivery_url = "https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1"
    cj = browser_cookie3.chrome() 
    resp = requests.get(delivery_url, cookies=cj, headers=amazon_request_headers)
    return resp

def interpret_resp(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    slotselect_div_id = 20200325
    slotselect_div = soup.find(id=slotselect_div_id)
    if 'ufss-unavailable' in slotselect_div.attrs['class']:
        message = "No Slots available."
        retry = True
    elif 'ufss-available' in slotselect_div.attrs['class']:
        message = "Hurry, Slots available!"
        retry = False
    else:
        fname = 'response.html'
        message = "Unknown error, check response content manually"
        retry = False
        with open(fname, 'wb') as f:
            f.write(response.content)
    return retry, message

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--pushover_api_key", required=True)
    parser.add_argument("--pushover_user_key", required=True)
    parser.add_argument("--min_delay_minutes", type=int, default=5)
    parser.add_argument("--max_delay_minutes", type=int, default=35)
    parser.add_argument("--amazon_request_headers_file", required=True)
    args = parser.parse_args()

    pushover = PushoverNotifier(user_key=args.pushover_user_key, api_key=args.pushover_api_key)

    with open(args.amazon_request_headers_file, 'r') as f:
        amazon_request_headers = json.load(f)

    retry = True
    while retry:
        resp = fetch_delivery_url(amazon_request_headers)
        retry, message = interpret_resp(resp)
        
        if retry:
            delay_minutes = numpy.random.randint(low=args.min_delay_minutes, high=args.max_delay_minutes)
            message += " waiting {} minutes to try again".format(delay_minutes)
        else:
            message += " exiting."

        print(message)
        pushover.notify(message)

        if retry:
            noise_seconds = numpy.random.randint(low=0, high=60)
            time.sleep(60 * delay_minutes + noise_seconds)



