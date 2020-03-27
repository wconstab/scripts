import browser_cookie3 
import json
import numpy
import requests 
import time
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from util.pushover import PushoverNotifier

def load_html_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    return content

def fetch_delivery_url(amazon_request_headers):
    """
    Rely fully on chrome cookies- removing cookie and referer URL from headers doens't seem to break it.
    """
    delivery_url = "https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1"
    cj = browser_cookie3.chrome() 
    resp = requests.get(delivery_url, cookies=cj, headers=amazon_request_headers)
    resp.raise_for_status()
    return resp.content

"""
Probably try pressing this button
<input class="a-button-text" formaction="/gp/buy/itemselect/handlers/continue.html/ref=chk_multi_addr_continue?ie=UTF8&amp;action=continue-no-js&amp;useCase=singleAddress" name="continue-bottom" type="submit" value="Continue"/>

"""
def interpret_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    retry = False
    if soup.find('div', {'class':'ufss-unavailable'}) is not None:
        message = "No slots available."
        retry = True
    elif soup.find('div', {'class':'ufss-available'}) is not None:
        message = "Hurry, slots available!"
    elif soup.find(text="We're sorry we are unable to fulfill your entire order."):
        change_q_form = soup.find('form', {'id': 'changeQuantityFormId'})
        item_rows = change_q_form.find_all('div', {'class': ['item-row']})
        items = []
        for row in item_rows:
            text_col = row.find('div', {'class': 'itemselect-right-col'})
            item_name = text_col.find('p').contents[0]
            items.append(item_name)
        message = "{} items out of stock: {}".format(len(items), items)
    else:
        message = "Unknown response"
    return retry, message

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--pushover_config", help="optionally provide json config with user_key and api_key fields for using pushover service.")
    parser.add_argument("--min_delay_minutes", type=int, default=1)
    parser.add_argument("--max_delay_minutes", type=int, default=5)
    parser.add_argument("--amazon_headers", default="config/amazon_request_headers.json", help="json formatted request headers for amazon get request.")
    args = parser.parse_args()

    if args.pushover_config:
        pushover = PushoverNotifier(config=args.pushover_config)

    with open(args.amazon_headers, 'r') as f:
        amazon_request_headers = json.load(f)

    try:
        retry = True
        while retry:
            content = fetch_delivery_url(amazon_request_headers)
            retry, message = interpret_content(content)
            
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
    except Exception as e:
        fname = time.strftime("response-%Y%m%d-%H%M%S.html")
        with open(fname, 'wb') as f:
            f.write(content)
        message = "{}, check response content manually, {}".format(e, fname)
        print(message)
        if pushover:
            pushover.notify(message)


