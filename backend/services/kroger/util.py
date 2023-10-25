from typing import List, Dict
from api import fetch_locations, fetch_products_by_term

KROGER_CHAINS = [
    "PICK N SAVE",
    "HART",
    # "RALPHS",
    "PAYLESS",
    "GERBES",
    "DILLONS",
    "QFC",
    "METRO MARKET",
    "KROGER",
    "FOOD4LESS",
    "BAKERS",
    "FRED",
    "MARIANOS",
    "VITACOST",
    "OFFBRAND",
    "RULER",
    "KINGSOOPERS",
    "FOODSCO",
    "CITYMARKET",
    "JAYC",
    "FRYS",
    "SMITHS"
]

# Kroger JSON data parsing functions

def parse_stores(data: List[Dict]) -> List[Dict]:
    
    parsed_stores = []
    
    for store in data:
        parsed_store = {}
        parsed_store['api_reference'] = store['locationId']
        parsed_store['name'] = store['name']
        parsed_store['chain'] = store['chain']
        parsed_store['zip_code'] = store['address']['zipCode']
        parsed_store['address'] = ', '.join(filter(None, [store['address'].get(key) for key in ["addressLine1", "city", "state", "zipCode"]]))
        parsed_store['latitude'] = store['geolocation']['latitude']
        parsed_store['longitude'] = store['geolocation']['longitude']
        parsed_stores.append(parsed_store)
        
    return parsed_stores

def parse_product_data(data: Dict) -> Dict:
    product_data = {}
    product_data['name'] = data['description']
    product_data['price'] = data['items'][0]['price']['regular']
    product_data['UPC'] = data['upc']
    return product_data

# Kroger fetch and parse functions

def fetch_best_kroger_price(term: str, store_id: str ) -> List[Dict]:
    
    products = fetch_products_by_term(term, store_id)
    
    if products:
        # check if products have price key and regular price
        products = [product for product in products if product['items'][0].get('price') and product['items'][0]['price'].get('regular')]

        
        
        # sort products by price
        
        