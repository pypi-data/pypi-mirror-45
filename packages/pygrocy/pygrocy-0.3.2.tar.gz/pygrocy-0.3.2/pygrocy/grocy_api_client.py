import json
from urllib.parse import urljoin

import requests

from pygrocy.utils import parse_date, parse_int, parse_float


class GrocyApiClient(object):
    def __init__(self, base_url, api_key):
        self._base_url = base_url
        self._api_key = api_key
        self._headers = {
            "accept": "application/json",
            "GROCY-API-KEY": api_key
        }

    def get_stock(self):
        req_url = urljoin(self._base_url, "stock")
        resp = requests.get(req_url, headers=self._headers)
        parsed_json = json.loads(resp.text)
        return [CurrentStockResponse(response) for response in parsed_json]

    def get_volatile_stock(self):
        req_url = urljoin(self._base_url, "stock/volatile")
        resp = requests.get(req_url, headers=self._headers)
        parsed_json = json.loads(resp.text)
        return CurrentVolatilStockResponse(parsed_json)

    def get_product(self, product_id):
        req_url = urljoin(urljoin(self._base_url, "stock/products/"), str(product_id))
        resp = requests.get(req_url, headers=self._headers)
        parsed_json = json.loads(resp.text)
        return ProductDetailsResponse(parsed_json)


class CurrentVolatilStockResponse(object):
    def __init__(self, parsed_json):
        self._expiring_products = [ProductData(product) for product in parsed_json['expiring_products']]
        self._expired_products = [ProductData(product) for product in parsed_json['expired_products']]
        self._missing_products = [ProductData(product) for product in parsed_json['missing_products']]

    @property
    def expiring_products(self):
        return self._expiring_products

    @property
    def expired_products(self):
        return self._expired_products

    @property
    def missing_products(self):
        return self._missing_products


class CurrentStockResponse(object):
    def __init__(self, parsed_json):
        self._product_id = int(parsed_json['product_id'])
        self._amount = float(parsed_json['amount'])
        self._best_before_date = parse_date(parsed_json['best_before_date'])

    @property
    def product_id(self):
        return self._product_id

    @property
    def amount(self):
        return self._amount

    @property
    def best_before_date(self):
        return self._best_before_date


class ProductDetailsResponse(object):
    def __init__(self, parsed_json):
        self._last_purchased = parse_date(parsed_json['last_purchased'])
        self._last_used = parse_date(parsed_json['last_used'])
        self._stock_amount = int(parsed_json['stock_amount'])
        self._stock_amount_opened = parse_int(parsed_json['stock_amount_opened'])
        self._next_best_before_date = parse_date(parsed_json['next_best_before_date'])
        self._last_price = parse_float(parsed_json['last_price'])

        self._product = ProductData(parsed_json['product'])

        self._quantity_unit_purchase = QuantityUnitData(parsed_json['quantity_unit_purchase'])
        self._quantity_unit_stock = QuantityUnitData(parsed_json['quantity_unit_stock'])

        self._location = LocationData(parsed_json['location'])

    @property
    def last_purchased(self):
        return self._last_purchased

    @property
    def last_used(self):
        return self._last_used

    @property
    def stock_amount(self):
        return self._stock_amount

    @property
    def stock_amount_opened(self):
        return self._stock_amount_opened

    @property
    def next_best_before_date(self):
        return self._next_best_before_date

    @property
    def last_price(self):
        return self._last_price


class ProductData(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json['id'])
        self._name = parsed_json['name']
        self._description = parsed_json.get('description', None)
        self._location_id = parse_int(parsed_json.get('location_id', None))
        self._qu_id_stock = parse_int(parsed_json.get('qu_id_stock', None))
        self._qu_id_purchase = parse_int(parsed_json.get('qu_id_purchase', None))
        self._qu_factor_purchase_to_stock = parse_float(parsed_json.get('qu_factor_purchase_to_stock', None))
        self._barcodes = parsed_json.get('barcode', "").split(",")
        self._picture_file_name = parsed_json.get('picture_file_name', None)
        self._allow_partial_units_in_stock = bool(parsed_json.get('allow_partial_units_in_stock', None) == "true")
        self._row_created_timestamp = parse_date(parsed_json.get('row_created_timestamp', None))
        self._min_stock_amount = parse_int(parsed_json.get('min_stock_amount', None), 0)
        self._default_best_before_days = parse_int(parsed_json.get('default_best_before_days', None))

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name


class QuantityUnitData(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json['id'])
        self._name = parsed_json['name']
        self._name_plural = parsed_json['name_plural']
        self._description = parsed_json['description']
        self._row_created_timestamp = parse_date(parsed_json['row_created_timestamp'])


class LocationData(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json['id'])
        self._name = parsed_json['name']
        self._description = parsed_json['description']
        self._row_created_timestamp = parse_date(parsed_json['row_created_timestamp'])
