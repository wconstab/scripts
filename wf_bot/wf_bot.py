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
    Rely fully on chrome cookies- removing cookie and referer URL from headers doens't seem to break it.
    """
    delivery_url = "https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1"
    cj = browser_cookie3.chrome() 
    resp = requests.get(delivery_url, cookies=cj, headers=amazon_request_headers)
    return resp


def interpret_resp(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    slotselect_div_id = 20200325
    slotselect_div = soup.find(id=slotselect_div_id)
    try:
        if 'ufss-unavailable' in slotselect_div.attrs['class']:
            message = "No Slots available."
            retry = True
        elif 'ufss-available' in slotselect_div.attrs['class']:
            message = "Hurry, Slots available!"
            retry = False
    except Exception:
        fname = time.strftime("response-%Y%m%d-%H%M%S.html")
        message = "Unknown error, check response content manually, {}".format(fname)
        retry = False
        with open(fname, 'wb') as f:
            f.write(response.content)
    return retry, message

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--pushover_config", help="optionally provide json config with user_key and api_key fields for using pushover service.")
    parser.add_argument("--min_delay_minutes", type=int, default=5)
    parser.add_argument("--max_delay_minutes", type=int, default=35)
    parser.add_argument("--amazon_headers", default="amazon_request_headers.json", help="json formatted request headers for amazon get request.")
    args = parser.parse_args()

    if args.pushover_config:
        pushover = PushoverNotifier(config=args.pushover_config)

    with open(args.amazon_headers, 'r') as f:
        amazon_request_headers = json.load(f)

    retry = True
    while retry:
        resp = fetch_delivery_url(amazon_request_headers)
        retry, message = interpret_resp(resp)
        
        if retry:
            delay_minutes = numpy.random.randint(low=args.min_delay_minutes, high=args.max_delay_minutes)
            noise_seconds = numpy.random.randint(low=0, high=60)
            message += " waiting {} minutes to try again".format(delay_minutes)
            print(message)
            time.sleep(60 * delay_minutes + noise_seconds)

        else:
            message += " exiting."
            print(message)
            if pushover:
                pushover.notify(message)




