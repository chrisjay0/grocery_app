from decouple import config
import base64
import requests
from typing import Dict, Union, List

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

print(fetch_food4less_prices(['tofu']))