import requests


class Converter(object):
    def __init__(self, shop_name, shop_key):
        self.shop_name = shop_name
        self.shop_key = shop_key

    def request(self, url):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Shopify-Access-Token': self.shop_key
        }
        return requests.get(url, headers=headers)
