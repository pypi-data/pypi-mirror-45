import requests

name = 'shopify_converter'


class Converter(object):
    def __init__(self, shop_name, shop_key, shop_type):
        '''
        Params:
        - shop_name (String): yourshop.myshopify.com | yourshop.onshopbase.com
        - shop_key (String): key from Shopify
        - shop_type (String): Shopify | ShopBase
        '''
        self.shop_name = shop_name
        self.shop_key = shop_key
        self.shop_type = shop_type

    def request(self, url):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-{}-Access-Token'.format(self.shop_type): self.shop_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code // 200 != 1:
            raise Exception
        return response.json()
