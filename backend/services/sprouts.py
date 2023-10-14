import requests
from typing import Dict, List

STORES_URL = "https://shop.sprouts.com/api/v2/stores"

HEADERS = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'Cookie': 'session-sprouts=.eJwdjslugzAARP_F5zSqabNxqyKU2gqmISQGLoiAUUzMUmwCdtV_r9XDXN5oNO8HZNXA5B24VS4kW4CsZ0OTt6xVwFXDaIlkUvKuzVT3YC1wAdP4fjsUPOAYXQyChOPd0kJYOFdtYwpHPG9i16d7tEYNbpLI06S56GMkHunBU-Rwek_PkBPjGctEEuE6bdBETDHZjUTt1aQxrnJ64kGNtG-82XYzOU88oaHK6er_K3bEA9X9WNJZHvdWqtmNjMJnGfs8aENd0otEjbiX1sOPkhWpk8mvTyaIX5el48zbbfVFVB9-B7NPi49PHIRaYB2b6dkVa_riqeNa6A4swCjZkPESuI7zBuFmA1e_f8WMbMI.GAXyDw.gBrNKcw1l-KoF1RRVHhU1avAJ5k; __cf_bm=RnTb1SfDIx0r0tPb4OMwPzGN4MhLeRizpY6ELZOEax8-1696897678-0-Aahy/HcyQ8d60m2h+8aUU5/6H8N91ysNU7JF3rsoB2fI83G7XwNUgJ1DAt5B7I3qsw7kWZwEjzgo6LGctvZOBvU='
            }

def build_sprouts_url(item_name: str, number_products: int = 12) -> str:
    return f"https://shop.sprouts.com/api/v2/store_products?limit={number_products}&offset=0&search_term={item_name}&sort=rank"

def parse_sprouts_product(data: Dict) -> Dict:
        product = {}
        
        product['product_name'] = data['name']
        product['product_upc'] = data['ext_id']
        product['chain'] = 'Sprouts'
        product['store_price'] = data['base_price']
        
        
        store_lookup = data['fulfillment_retailer_store_id']
        payload = {}
        headers = HEADERS
    
        store_response  = requests.request("GET", STORES_URL, headers=headers, data=payload)
        stores = store_response.json()['items']
        
        store_found = False
        while not store_found:
            for store in stores:
                if store['retailer_store_id'] == store_lookup:
                    product_store = store
                    store_found = True
                    break
        
        product['store_api_code'] = product_store['id']
        product['store_address'] = ', '.join(filter(None, [product_store['address'].get(key) for key in ["address1", "address2", "address3", "city", "province", "postal_code", "country"]]))
        product['store_zip'] = product_store['address']['postal_code']
        
        return product  
     

def fetch_sprouts_product(item_name: str, zip_code: str = '00000') -> List[Dict]:
    """
    Fetches the product information for the given item name from the Sprouts API.

    Args:
    - item_name (str): The name of the item to search for.

    Returns:
    - 
    - List[dict]: A list of dictionaries containing up to 12 products. Each product dict contains the keys: product_name, produt_upc, chain, store_api_code, store_address, store_zip, store_price.
    """
    
    url = build_sprouts_url(item_name)
    payload = {}
    headers = HEADERS
    
    response = requests.request("GET", url, headers=headers, data=payload)
    
    response_items = response.json()['items']
    
    products = []
    
    for item in response_items:
        products.append(parse_sprouts_product(item))
    
    return products
        
def fetch_sprouts_price(item_name: str) -> Dict:
    products = fetch_sprouts_product(item_name)
    
    best_price = products[0]
    
    for product in products:
        if product['store_price'] < best_price['store_price']:
            best_price = product
    
    return {best_price['chain']:{best_price['product_name']: best_price['store_price']}}
