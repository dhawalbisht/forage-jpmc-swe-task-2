import json
import random
import urllib.request
from urllib.error import URLError, HTTPError

# Server API URLs
QUERY = "http://localhost:8080/query?id={}"

# 500 server requests
N = 500


def getDataPoint(quote):
    stock = quote["stock"]
    bid_price = float(quote["top_bid"]["price"])
    ask_price = float(quote["top_ask"]["price"])
    price = (bid_price + ask_price) / 2
    return stock, bid_price, ask_price, price


def getRatio(price_a, price_b):
    if price_b == 0:  # Avoid division by zero
        return None
    return price_a / price_b


if __name__ == "__main__":
    prices = {}

    try:
        for _ in iter(range(N)):
            quotes = json.loads(
                urllib.request.urlopen(QUERY.format(random.random())).read()
            )
            for quote in quotes:
                stock, bid_price, ask_price, price = getDataPoint(quote)
                prices[stock] = price
                print(
                    "Quoted %s at (bid:%s, ask:%s, price:%s)"
                    % (stock, bid_price, ask_price, price)
                )
            if "A" in prices and "B" in prices:
                ratio = getRatio(prices["A"], prices["B"])
                if ratio is not None:
                    print("Ratio %s" % ratio)
                else:
                    print("Unable to calculate ratio (price B is 0)")
    except (URLError, HTTPError) as e:
        print(f"Error: {e}")
