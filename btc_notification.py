import requests
import time
import argparse


class Bitcoin:
    def __init__(self, btc_url, ifttt_webhooks_url, btc_threshold_price):
        self.btc_url = btc_url    # for BTC API url
        self.ifttt_webhooks_url = ifttt_webhooks_url    # for webhooks url
        self.btc_threshold_price = btc_threshold_price  # price threshold

    def get_latest_btc_price(self, coinIndex):
        url = self.btc_url   # BTC API url.
        r = requests.get(url)    # get retuest to obtain btc data.
        res = r.json()    # BTC data received (json data)
        # Got actual BTC price below from response json object.
        bitPrice = res[coinIndex]['price']
        bitPrice = float(bitPrice)
        threshold = int(bitPrice)  # convert threshold to int.
        return (bitPrice, threshold)

    def post_ifttt_webhook(self, event, coinName, value):
        # Value is sent to IFTTT as json object.
        data = {
            'value1': coinName, 'value2': value}
        # Formatting event as per action for Telegram
        ifttt_event_url = self.ifttt_webhooks_url.format(event)
        # Sending post request to IFTTT url.
        requests.post(ifttt_event_url, json=data)

    def post_ifttt_webhook_mail(self, event, coinName, value_a, value_b):
        # Value is sent to IFTTT as json object
        data = {
            'value1': coinName, 'value2': value_a, 'value3': value_b}
        # Formatting required destination action for gmail.
        ifttt_event_url = self.ifttt_webhooks_url.format(event)
        # Sending post request to IFTTT url.
        requests.post(ifttt_event_url, json=data)

    def making_btc_log(self, btc_log, btc_price, date):
        rows = []
        for each_price in btc_log:
            price = each_price['price']
            # Format date and to bold the BTC price.
            row = '{}: $<b>{}</b>'.format(date, price)
            rows.append(row)
        # Using <br> tag to seperate rows and returning them.
        return '<br>'.join(rows)


if __name__ == '__main__':
    coinIndex = 0
    # Help code to parse the positional arguments while running code
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'c', help="Cryptocurrency Price to Know:", choices=['BTC', 'ETH'])
    parser.add_argument('t', help="Threshold for cryptocurrency \
        (For BTC Type 10000 (means $ 10000) and ETH Type 300 (means $ 300))")
    parser.add_argument('l', help="Length of BTC log")
    parser.add_argument('n', help="Notification Interval")

    args = parser.parse_args()
    if args.c == "BTC":
        coinIndex = 0
    elif args.c == "ETH":
        coinIndex = 1

    list_length = args.l
    list_length = int(list_length)
    min = args.n
    min = int(min)

    if coinIndex == 0:
        coinName = 'Bitcoin'
    elif coinIndex == 1:
        coinName = 'Ethereum'

    # constant identifiers for the project are mentioned below.
    BITCOIN_PRICE_THRESHOLD = int(args.t)
    base_API_url = 'https://api.nomics.com/v1/currencies/ticker?'
    BITCOIN_API_URL = base_API_url + 'key=4279dd1d7b991cb52f8dede936c29d61'
    baseUrl = 'https://maker.ifttt.com/trigger'
    IFTTT_WEBHOOKS_URL = baseUrl + '/{}/with/key/cknJo_YPsoKtpUrWOia0xp'

    btc = Bitcoin(BITCOIN_API_URL, IFTTT_WEBHOOKS_URL, BITCOIN_PRICE_THRESHOLD)

    btc_log = []
    while True:
        # Getting BTC price, BTC emergency threshold.
        btc_price, btc_threshold = btc.get_latest_btc_price(coinIndex)
        date = time.asctime(time.localtime(time.time()))
        btc_log.append({'date': date, 'price': btc_price})

        btc.post_ifttt_webhook('btc_price_update', coinName, btc_price)

        # For emergency notification.
        if btc_threshold < BITCOIN_PRICE_THRESHOLD:
            btc.post_ifttt_webhook('btc_emergency', coinName, btc_price)

        # BTC notification on gmail with reference website url.
        reference_web_url = 'https://www.coindesk.com/price/bitcoin'
        btc.post_ifttt_webhook_mail(
            'btc_price_on_gmail', coinName, btc_price, reference_web_url)

        # If 5 BTC prices are populated make a log and send a notification.
        if len(btc_log) == list_length:
            btc_dict_log = btc.making_btc_log(btc_log, btc_price, date)
            history_Text = "History of " + coinName
            btc.post_ifttt_webhook(
                'btc_price_update', history_Text, btc_dict_log)
            btc_log = []

        # For Sleep time and pinging a notification update every 5 mins.
        sleepTime = min * 60
        time.sleep(sleepTime)
