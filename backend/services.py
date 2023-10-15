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
SCOPE = 'product.compact'

NEARBY_DISTANCE = 35
ITEM_LIMIT = 3
STORE_LIMIT = 6

DEFAULT_ZIP = '45052'

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


def fetch_nearest_stores(zip_code: str = DEFAULT_ZIP, nearby_dist: int = NEARBY_DISTANCE) -> List[Dict]:
    if not is_token_valid():
        refresh_token()
    
    headers = {
        'Authorization': f'Bearer {token_cache["token"]}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(f'{BASE_URL}/locations?filter.zipCode.near={zip_code}&filter.radiusInMiles={nearby_dist}&filter.limit={STORE_LIMIT}', headers=headers)
    data = response.json()['data']
    
    # Filter out stores with the chain "RALPHS"
    non_ralphs_stores = [store for store in data if store.get('chain') != 'RALPHS']
    
    # Check if non_ralphs_stores is empty
    if not non_ralphs_stores:
        # Log a message or handle as needed
        print("No non-Ralphs stores found!")
        return []

    # Return only up to the first three non-Ralphs stores
    return non_ralphs_stores[:3]



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
    # seen_chains = set()
    # unique_stores = [] 

    # for store in data:
    #     chain = store['chain']
    #     if chain not in seen_chains:
    #         seen_chains.add(chain)
    #         unique_stores.append(store)

    parsed_unique_stores = []
    
    for store in data:
        parsed_store = {}
        parsed_store['api_reference'] = store['locationId']
        parsed_store['name'] = store['name']
        parsed_store['chain'] = store['chain']
        parsed_store['zip_code'] = store['address']['zipCode']
        parsed_store['address'] = ', '.join(filter(None, [store['address'].get(key) for key in ["addressLine1", "city", "state", "zipCode"]]))
        parsed_unique_stores.append(parsed_store)
        
    return parsed_unique_stores
        
def fetch_nearest_unique_stores(zip_code: str = DEFAULT_ZIP) -> List[Dict]:
    stores = fetch_nearest_stores(zip_code)
    return parse_unique_stores(stores)

def parse_product_data(data: Dict) -> Dict:
    product_data = {}
    product_data['name'] = data['description']
    product_data['price'] = data['items'][0]['price']['regular']
    product_data['UPC'] = data['upc']
    return product_data

def fetch_best_prices(term: str, zip_code: str ) -> List[Dict]:
    """Retrieves items from the closest stores, finds the cheapest, and returns a parsed list of dicts.

    Args:
        term (str): the search term for the item being searched
        zip_code (str): The zip code to search near.

    Returns:
        List[Dict]: A list of dictionaries each containing a specific store and the cheapest product.
    """
    stores = fetch_nearest_unique_stores(zip_code)
    prices = []

    for store in stores:
        products = fetch_products_for_ralphs(term, store['api_reference']) if store['chain'] == 'RALPHS' else fetch_products_by_term(term, store['api_reference'])
        
        # Ensure products is a list and not empty
        if not products or not isinstance(products, list):
            continue

        best_deal = None
        best_deal_price = float('inf')  # Set an initial high value for comparison

        for product in products:
            # Guard against potential missing keys or data structures
            items = product.get('items', [])
            if not items:
                continue
            
            current_price = items[0].get('price', {}).get('regular', float('inf'))
            
            if current_price < best_deal_price:
                best_deal = product
                best_deal_price = current_price
        
        # Ensure we found a valid best deal before appending
        if best_deal and best_deal_price < float('inf'):
            parsed_product = parse_product_data(best_deal)
            prices.append({'store': store, 'product': parsed_product})

    return prices
