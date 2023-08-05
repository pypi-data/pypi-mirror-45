import time
from shopify_converter import Converter


class ProductConverter(Converter):
    def convert(self, product_id):
        url = 'https://{}/admin/products/{}.json'.format(
            self.shop_name,
            product_id
        )
        response = self.request(url)
        return self.parse_product(response.get('product'))

    def parse_product(self, shopify_product):
        options = [option.get('name', '')
                   for option in shopify_product.get('options', [])]
        item_options = {'name': options}

        image_hash, item_images = self.__parse_images(
            shopify_product.get('images', []))
        thumbnail_proto = self.__parse_thumbnail(
            shopify_product.get('image', {}))
        variants = [self.__parse_variant(variant, image_hash, thumbnail_proto)
                    for variant in shopify_product.get('variants', [])]

        return {
            'options': item_options,
            'images': {'image': item_images},
            'item_info': self.__parse_item_info(
                shopify_product, thumbnail_proto),
            'title': shopify_product.get('title', ''),
            'description': shopify_product.get('shopify_product_html', ''),
            'status': 'I_PUSHED',
            'variants': variants,
            'platform_product_id': str(shopify_product.get('id', 0))
        }

    def __parse_properties(self, shopify_variant):
        options = ['option1', 'option2', 'option3']
        properties = {'property': []}
        for (index, option) in enumerate(options):
            option_name = shopify_variant.get(option)
            if option_name:
                properties['property'].append({
                    'option_id': index,
                    'name': option_name
                })
        return properties

    def __parse_variant(self, shopify_variant, image_hash, thumbnail_proto):
        image_id = shopify_variant.get('image_id', 0)
        if image_id:
            image_url = image_hash[image_id].get('url', '')
            image = image_hash[image_id]
        else:
            image_url = thumbnail_proto.get('url', '')
            image = thumbnail_proto

        price = {
            'created_at': int(time.time() or 0),
            'price': float(shopify_variant.get('price', 0) or 0),
            'compared_price': float(shopify_variant.get('compare_at_price', 0)
                                    or 0)
        }
        prices = {'price': [price]}

        return {
            'properties': self.__parse_properties(shopify_variant),
            'image_url': image_url,
            'inventory': shopify_variant.get('inventory_quantity', 0),
            'prices': prices,
            'platform_variant_id': str(shopify_variant.get('id', 0)),
            'status': 'V_SELECTED',
            'image': image
        }

    def __parse_item_info(self, shopify_product, thumbnail_proto):
        if thumbnail_proto:
            item_info = {
                'thumbnail': thumbnail_proto.get('url', ''),
                'thumbnail_proto': thumbnail_proto
            }
        else:
            item_info = {}

        item_info['types'] = shopify_product.get('product_type', '')
        item_info['tags'] = ','.join(
            [tag.strip() for tag in shopify_product.get('tags', '').split(',')]
        )
        item_info['min_price'] = 99999999999
        item_info['max_price'] = -99999999999
        for variant in shopify_product.get('variants', []):
            v_price = float(variant.get('price', 0) or 0)
            if item_info['min_price'] > v_price:
                item_info['min_price'] = v_price
            if item_info['max_price'] < v_price:
                item_info['max_price'] = v_price
        return item_info

    def __parse_thumbnail(self, thumbnail):
        if not thumbnail:
            return {}
        return {
            'url': thumbnail['src'],
            'status': 'IMG_SELECTED',
            'platform_image_id': str(thumbnail.get('id', 0))
        }

    def __parse_images(self, images):
        image_hash = {}
        item_images = []
        for image in images:
            item_image = {
                'url': image.get('src', ''),
                'status': 'IMG_SELECTED',
                'platform_image_id': str(image.get('id', 0))
            }
            item_images.append(item_image)
            image_hash[image.get('id', 0)] = item_image

        return image_hash, item_images
