import sys
import time
import requests
import logging
import json

from .base import AbstractImporter
from productfeeds.models import Product

logger = logging.getLogger(__name__)

PRODUCTS_URL = 'https://api.convertiser.com/publisher/products/v2/?key={}'
REQUEST_TIMEOUT = 120


class ConvertiserImporter(AbstractImporter):

    def __init__(self, token=None, offers=None, website_key=None, articlecode_prefix='con_', page_size=20000,
                 *args, **kwargs):

        super(ConvertiserImporter, self).__init__(*args, articlecode_prefix=articlecode_prefix, **kwargs)
        self.page_size = page_size
        self.website_key = website_key
        self.offers = offers
        self.token = token

    def get_feeds(self):
        return self.offers

    def _fetch(self, offer):
        response = requests.post(
                    PRODUCTS_URL.format(self.website_key),
                    headers={'Authorization': 'Token {}'.format(self.token), 'Content-Type': 'application/json'},
                    data=json.dumps({
                        "filters": {"offer_id": {"lookup": "exact", "value": offer}},
                        "page": 1, "page_size": self.page_size
                    }),
                    timeout=REQUEST_TIMEOUT
        )
        return response.json()

    def _generate_feed_items(self, data):
        for item in data['data']:
            yield item

    def _build_product(self, feed, product):
        p = Product()
        p.d['client'] = product['offer']
        articlecode = self._build_articlecode("{}_{}".format(product['offer_id'], product['id']))
        p.d['articlecode'] = articlecode
        p.d['title'] = product['title']
        p.d['brand'] = product['brand']
        categories = product['product_type'].split('/')
        p.d['category'] = categories[0]
        try:
            p.d['subcategory1'] = categories[1]
        except:
            pass
        try:
            p.d['subcategory2'] = categories[2]
        except:
            pass
        p.d['description'] = product['description']
        if sys.version_info[0] < 3:
            p.d['title'] = p.d['title'].encode('utf-8')
            p.d['description'] = p.d['description'].encode('utf-8')
            p.d['brand'] = p.d['brand'].encode('utf-8')
            p.d['category'] = p.d['category'].encode('utf-8')
        p.d['producturl'] = product['link']
        p.d['thumburl'] = product['images']['thumb_180']
        p.d['imageurl'] = product['images']['default']
        p.d['price'] = product['price'].replace('PLN ', '')

        return p

