import time
import datetime
from shopify_converter import Converter


class OrderConverter(Converter):
    def convert(self, order_id):
        url = 'https://{}/admin/orders/{}.json'.format(
            self.shop_name,
            order_id
        )
        response = self.request(url)
        return self.parse_order(response.get('order'))

    def parse_order(self, order):
        order_variants = [
            self.__parse_variant(ov) for ov in order['line_items']]
        created_at = int(time.mktime(datetime.datetime.fromisoformat(
            order.get('created_at', '')).timetuple()))

        return {
            'shop': {'shop_name': self.shop_name},
            'customer': self.__parse_customer(order.get('customer', {})),
            'shipping_address': self.__parse_address(
                order.get('shipping_address', {})),
            'billing_address': self.__parse_address(
                order.get('billing_address', {})),
            'total_revenues': order.get('total_price', 0),
            'order_from': {
                'type': self.shop_type.upper(),
                'order_no': str(order.get('id', 0))
            },
            'display_name': order.get('name', ''),
            'order_variants': order_variants,
            'created_at': created_at,
            'platform_note': order.get('note', ''),
            'platform_created_at': created_at
        }

    def __parse_variant(self, line_item):
        order_variant_from = {
            'type': self.shop_type.upper(),
            'platform_variant_id': str(line_item.get('variant_id', 0)),
            'platform_order_variant_id': str(line_item.get('id', 0)),
            'platform_product_id': str(line_item.get('product_id', 0))
        }
        order_variant_info = {
            'title': line_item.get('title', ''),
            'variant_properties': line_item.get('variant_title', '')
        }
        order_variant = {
            'order_from': order_variant_from,
            'order_variant_info': order_variant_info,
            'quantity': line_item.get('quantity', 0),
            'unit_price': line_item.get('price', 0)
        }

        return order_variant

    def __parse_address(self, address):
        if not address:
            return {}

        return {
            'fullname': self.__get_fullname(
                address['first_name'], address['last_name']),
            'address1': address.get('address1', ''),
            'address2': address.get('address2', ''),
            'phone': address.get('phone', ''),
            'country': address.get('country', ''),
            'country_code': address.get('country_code', ''),
            'province': address.get('province', ''),
            'province_code': address.get('province_code', ''),
            'city': address.get('city', ''),
            'zip': str(address.get('zip', '')),
            'company': address.get('company', ''),
            'latitude': str(address.get('latitude')),
            'longitude': str(address.get('longitude')),
        }

    def __parse_customer(self, customer):
        return {
            'fullname': self.__get_fullname(
                customer.get('first_name', ''), customer.get('last_name', '')),
            'email': customer.get('email', ''),
            'phone_number': customer.get('phone', ''),
            'default_address': self.__parse_address(
                customer.get('default_address', {}))
        }

    def __get_fullname(self, first_name, last_name):
        return '{} {}'.format(first_name, last_name)
