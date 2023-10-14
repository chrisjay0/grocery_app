from decouple import config
import base64
import requests
from typing import Dict, Union, List

CLIENT_ID = config('KROGER_ID')
CLIENT_SECRET = config('KROGER_SECRET')

TOKEN_URL = 'https://api-ce.kroger.com/v1/connect/oauth2/token'
SCOPE = 'product.compact'  # Replace with the appropriate scope

BASE_URL = "https://api-ce.kroger.com"
LOCATION_ID = "70400321"

def build_food4less_url(item_name: str, number_products: int = 12) -> str:
    return f"{BASE_URL}/v1/products?filter.term={item_name}&filter.locationId={LOCATION_ID}&filter.limit={number_products}"

def get_new_token():
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
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
    return response.json()['access_token']

def fetch_food4less_product(item_name: str, zip_code: str = '000000') -> List[Dict]:
    token = get_new_token()
    
    headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    response = requests.get(build_food4less_url(item_name), headers=headers)
    response_data = response.json()

    if response.status_code == 401 or ('error' in response_data and 'API-401' in response_data['error']):
        token = get_new_token()
        headers['Authorization'] = f'Bearer {token}'
        response = requests.get(build_food4less_url(item_name), headers=headers)
        response_data = response.json()
        
    
    
    # def parse_sprouts_product(data: Dict) -> Dict:
    #     product = {}
        
    #     product['product_name'] = data['name']
    #     product['product_upc'] = data['ext_id']
    #     product['chain'] = 'Sprouts'
    #     product['store_price'] = data['base_price']
        
        
    #     store_lookup = data['fulfillment_retailer_store_id']
    #     payload = {}
    #     headers = HEADERS
    
    #     store_response  = requests.request("GET", STORES_URL, headers=headers, data=payload)
    #     stores = store_response.json()['items']
        
    #     store_found = False
    #     while not store_found:
    #         for store in stores:
    #             if store['retailer_store_id'] == store_lookup:
    #                 product_store = store
    #                 store_found = True
    #                 break
        
    #     product['store_api_code'] = product_store['id']
    #     product['store_address'] = ', '.join(filter(None, [product_store['address'].get(key) for key in ["address1", "address2", "address3", "city", "province", "postal_code", "country"]]))
    #     product['store_zip'] = product_store['address']['postal_code']
        
    #     return product  
    
    def parse_food4less_product(data: Dict) -> Dict:
        product = {}
        
        product['product_name'] = data['description']
        product['product_upc'] = data['upc']
        product['chain'] = 'Food4Less'
        product['store_price'] = data['price']
        
        return product


def fetch_food4less_prices(item_names: List[str]) -> Dict:

    def get_kroger_item(item):
        CLIENT_ID = config('KROGER_ID')
        CLIENT_SECRET = config('KROGER_SECRET')

        TOKEN_URL = 'https://api-ce.kroger.com/v1/connect/oauth2/token'

        SCOPE = 'product.compact'  # Replace with the appropriate scope

        base_url = "https://api-ce.kroger.com"
        term = item
        location_id = "70400321"
        product_id = ""
        fulfillment = ""
        start = 0
        limit = 10

        PRODUCTS_URL = f"{base_url}/v1/products?filter.term={term}&filter.locationId={location_id}"

        # Function to get a new token
        def get_new_token():
            credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
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
            return response.json()['access_token']

        # Initial token request
        token = get_new_token()
        # print(token)

        # Product request with token
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(PRODUCTS_URL, headers=headers)
        response_data = response.json()

        # print(response)

        # Check if token expired or is invalid and get a new one if needed
        if response.status_code == 401 or ('error' in response_data and 'API-401' in response_data['error']):
            token = get_new_token()
            headers['Authorization'] = f'Bearer {token}'
            response = requests.get(PRODUCTS_URL, headers=headers)
            response_data = response.json()

        def parse_kroger_json(data: Dict) -> Dict[str, Union[str, float]]:
            products = data.get('data', [])
            if not products:
                return {}

            # Extracting product name and price for each product and storing them in a dictionary
            product_prices = {product['description']: product['items'][0].get('price', {}).get('regular', None) for product in products}
            
            # Removing products with None as their price
            product_prices = {k: v for k, v in product_prices.items() if v is not None}

            if not product_prices:
                return {}

            # Finding the product with the minimum price
            cheapest_product = min(product_prices, key=product_prices.get)

            return {cheapest_product: product_prices[cheapest_product]}
        
        return(parse_kroger_json(response_data))
    
    def createDictOfItemPrices(items: List[str]) -> Dict:
        prices = {}
        for item in items:
            prices.update(get_kroger_item(item))
        return {"Food 4 Less": prices}
    
    return createDictOfItemPrices(item_names)
