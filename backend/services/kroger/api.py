from decouple import config
import base64
import requests
from typing import Dict, Union, List
import time
import logging


BASE_URL = 'https://api-ce.kroger.com/v1'
CLIENT_ID = config('KROGER_ID')
API_KEY = config('KROGER_SECRET')

TOKEN_URL = f'{BASE_URL}/connect/oauth2/token'
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

# Token management

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
    
def refresh_headers():
    return {
        'Authorization': f'Bearer {token_cache["token"]}',
        'Content-Type': 'application/json'
    }

def is_token_valid() -> bool:
    if token_cache['token'] is None:
        return False
    age_in_seconds = time.time() - token_cache['timestamp']
    age_in_minutes = age_in_seconds / 60
    return age_in_minutes > TOKEN_EXPIRED

def try_request_data(req_url: str, headers: dict) -> List[dict]:
    """Attempts to return the data list from a given request url and headers. Refreshes the token if neccesary. 

    Args:
        req_url (str): Request url to kroger api
        headers (dict): Request headers to kroger api

    Returns:
        List[dict]: Data from requested response
    """
    response = requests.get(req_url, headers=headers)
    
    if response.status_code == 401:
        refresh_token()
        headers = refresh_headers()
        response = requests.get(req_url, headers=headers)
        
    try:
        data = response.json()['data']
        return data
        
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching kroger api data. Error: {e}")
        logging.error(f"Kroger API Response: {response}")
        return []
    
# API calls

def fetch_locations() -> List[Dict]:
    
    headers = refresh_headers()
    req_url = f'{BASE_URL}/locations'
    
    data = try_request_data(req_url, headers=headers)
    
    if data:
        return data
    else:
        logging.error("No Kroger locations found.")
        return []

def fetch_products_by_term(term: str, store_id: str, limit: int = ITEM_LIMIT) -> List[Dict]:
    
    headers = refresh_headers()
    req_url = f'{BASE_URL}/products?filter.locationId={store_id}&filter.limit={limit}&filter.term={term}'
    
    data = try_request_data(req_url, headers=headers)
    
    if data:
        return data
    else:
        logging.error("No Kroger products found.")
        return []