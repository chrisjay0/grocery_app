from decouple import config
import base64
import requests
from typing import Dict, Union, List
import time


BASE_URL = 'https://api-ce.kroger.com/v1'
CLIENT_ID = config('KROGER_ID')
API_KEY = config('KROGER_SECRET')

TOKEN_URL = 'https://api-ce.kroger.com/v1/connect/oauth2/token'
TOKEN_EXPIRED = 24
SCOPE = 'product.compact'  # Replace with the appropriate scope

NEARBY_DISTANCE = 5
ITEM_LIMIT = 6

token_cache = {
    'token': None,
    'timestamp': 0
}


def refresh_token():
    credentials = f"{CLIENT_ID}:{API_KEY}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_credentials}'
    }
    token_data = {
        'grant_type': 'client_credentials',
        'scope': SCOPE
    }
    response = requests.post(TOKEN_URL, headers=headers, data=token_data)
    token_cache['token'] = response.json()['access_token']
    token_cache['timestamp'] = time.time()


def is_token_valid():
    if token_cache['token'] is None:
        return False
    age_in_seconds = time.time() - token_cache['timestamp']
    age_in_minutes = age_in_seconds / 60
    return age_in_minutes > TOKEN_EXPIRED


def fetch_nearest_stores(zip_code: str, nearby_dist: int = NEARBY_DISTANCE) -> List[Dict]:
    if not is_token_valid():
        refresh_token()
    headers = {
        'Authorization': f'Bearer {token_cache["token"]}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'{BASE_URL}/locations?filter.zipCode.near={zip_code}&filter.radiusInMiles={nearby_dist}', headers=headers)
    return response.json()['data']


def fetch_products_by_term(term: str, store_id: str, limit: int = ITEM_LIMIT) -> List[Dict]:
    if not is_token_valid():
        refresh_token()
    headers = {
        'Authorization': f'Bearer {token_cache["token"]}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'{BASE_URL}/products?filter.locationId={store_id}&filter.limit={limit}&filter.term={term}', headers=headers)
    return response.json()['data']


### Workaround for Ralph's parameter issue ###
def fetch_products_for_ralphs(term: str, store_id: str, limit: int = ITEM_LIMIT) -> List[Dict]:
    
    products = fetch_products_by_term(term, '70400321')
    
    ralphs_products = []
    
    for product in products:
        id = product['productId']
    
        if not is_token_valid():
            refresh_token()
        headers = {
            'Authorization': f'Bearer {token_cache["token"]}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f'{BASE_URL}/products?filter.locationId={store_id}&filter.productId={id}&filter.limit={limit}', headers=headers)
        ralphs_products.append(response.json()['data'][0])
        
    return ralphs_products
### Workaround for Ralph's parameter issue ###
 

def parse_unique_stores(data: List[Dict]) -> List[Dict]:
    seen_chains = set()
    unique_stores = [] 

    for store in data:
        chain = store['chain']
        if chain not in seen_chains:
            seen_chains.add(chain)
            unique_stores.append(store)

    parsed_unique_stores = []
    
    for store in unique_stores:
        parsed_store = {}
        parsed_store['api_reference'] = store['locationId']
        parsed_store['name'] = store['name']
        parsed_store['chain'] = store['chain']
        parsed_store['zip_code'] = store['address']['zipCode']
        parsed_store['address'] = ', '.join(filter(None, [store['address'].get(key) for key in ["addressLine1", "city", "state", "zipCode"]]))
        parsed_unique_stores.append(parsed_store)
        
    return parsed_unique_stores
        
def fetch_nearest_unique_stores(zip_code) -> List[Dict]:
    stores = fetch_nearest_stores(zip_code)
    return parse_unique_stores(stores)

def fetch_best_prices(term: str, zip_code: str) -> List[Dict]:
    stores = fetch_nearest_unique_stores(zip_code)
    prices = []
    for store in stores:
        if store['chain'] == 'RALPHS':
            products = fetch_products_for_ralphs(term, store['api_reference'])
        else:
            products = fetch_products_by_term(term, store['api_reference'])
        best_deal = products[0]
        for product in products:
            product_price = product['items'][0].get('price', {}).get('regular', 9999)
            best_deal_price = best_deal['items'][0].get('price', {}).get('regular', 9999)
            if product_price < best_deal_price:
                best_deal = product
        prices.append({'store': store, 'product': best_deal})
        
    return prices

print(fetch_best_prices('tofu', '90001'))