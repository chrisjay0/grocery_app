from decouple import config
import base64
import httpx
from typing import Dict, Union, List
import time
import logging
from decimal import Decimal
import asyncio

BASE_URL = "https://api.kroger.com/v1"
CLIENT_ID = config("KROGER_ID")
API_KEY = config("KROGER_SECRET")

TOKEN_URL = f"{BASE_URL}/connect/oauth2/token"
TOKEN_EXPIRED = 24
SCOPE = "product.compact"

NEARBY_DISTANCE = 35
ITEM_LIMIT = 3
# STORE_LIMIT = 6

DEFAULT_ZIP = "45052"

token_cache = {"token": None, "timestamp": 0}


async def refresh_token():
    credentials = f"{CLIENT_ID}:{API_KEY}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}",
    }
    token_data = {"grant_type": "client_credentials", "scope": SCOPE}
    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_URL, headers=headers, data=token_data)
    token_cache["token"] = response.json()["access_token"]
    token_cache["timestamp"] = time.time()


def refresh_headers():
    return {
        "Authorization": f'Bearer {token_cache["token"]}',
        "Content-Type": "application/json",
    }


def is_token_valid():
    if token_cache["token"] is None:
        return False
    age_in_seconds = time.time() - token_cache["timestamp"]
    age_in_minutes = age_in_seconds / 60
    return age_in_minutes > TOKEN_EXPIRED


async def try_request_data(req_url: str, headers: dict) -> List[dict]:
    """Attempts to return the data list from a given request url and headers. Refreshes the token if neccesary.

    Args:
        req_url (str): Request url to kroger api
        headers (dict): Request headers to kroger api

    Returns:
        List[dict]: Data from requested response
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(req_url, headers=headers)

    if response.status_code == 401:
        await refresh_token()
        headers = refresh_headers()
        async with httpx.AsyncClient() as client:
            response = await client.get(req_url, headers=headers)

    try:
        data = response.json()["data"]
        return data

    except Exception as e:
        logging.error(
            f"An unexpected error occurred while fetching store locations. Error: {e}"
        )
        return []


def filter_out_no_price(term: str, products: List[Dict]) -> List[Dict]:
    def has_price(product: Dict) -> bool:
        items = product.get("items", [])
        if items and isinstance(items, list):
            price = items[0].get("price", {})
            return "regular" in price and price["regular"] is not None
        return False

    filtered_products = list(filter(has_price, products))

    if not filtered_products:
        logging.warning(f"No products found for {term} with a price")

    return filtered_products


async def fetch_products_by_term(
    term: str, store_id: str, limit: int = ITEM_LIMIT
) -> List[Dict]:
    req_url = f"{BASE_URL}/products?filter.limit={limit}&filter.term={term}&filter.locationId={store_id}"
    headers = refresh_headers()
    data = await try_request_data(req_url, headers)
    logging.info(f"Found items for {term}: {data}")
    return filter_out_no_price(term, data)


def parse_stores(data: List[Dict]) -> List[Dict]:
    parsed_stores = []

    for store in data:
        parsed_store = {}
        parsed_store["api_reference"] = store["locationId"]
        parsed_store["name"] = store["name"]
        parsed_store["chain"] = store["chain"]
        parsed_store["zip_code"] = store["address"]["zipCode"]
        parsed_store["address"] = ", ".join(
            filter(
                None,
                [
                    store["address"].get(key)
                    for key in ["addressLine1", "city", "state", "zipCode"]
                ],
            )
        )
        parsed_store["latitude"] = store["geolocation"]["latitude"]
        parsed_store["longitude"] = store["geolocation"]["longitude"]
        parsed_stores.append(parsed_store)

    return parsed_stores


def parse_product_data(data: Dict) -> Dict:
    product_data = {}
    product_data["name"] = data["description"]
    product_data["price"] = data["items"][0]["price"]["regular"]
    product_data["UPC"] = data["upc"]
    return product_data

async def fetch_best_prices(term: str, stores: List) -> List[Dict]:

    # This inner function fetches products for a single store and returns the best deal
    async def fetch_best_for_store(store):
        logging.info(f"Searching {store.name} for {term}...")
        products = await fetch_products_by_term(term, store.api_reference)
        logging.info(f"Found {len(products)} products")

        # Ensure products is a list and not empty
        if not products or not isinstance(products, list):
            logging.error(
                f"No products found for {term} in {store.name} or not recognizing as list..."
            )
            logging.info(f"Skipping {store.name}...")
            return None

        best_deal = None
        best_deal_price = float("inf")  # Set an initial high value for comparison

        for product in products:
            logging.info(f'Checking {product["description"]}...')
            # Guard against potential missing keys or data structures
            items = product.get("items", [])
            if not items:
                logging.error(f"{product}")
                continue

            current_price = items[0].get("price", {}).get("regular", float("inf"))

            if current_price < best_deal_price:
                best_deal = product
                best_deal_price = current_price

        # Ensure we found a valid best deal before appending
        if best_deal and best_deal_price < float("inf"):
            parsed_product = parse_product_data(best_deal)
            print(f"Found best deal: {parsed_product}")
            return {"store": store, "product": parsed_product}
        return None

    # Use asyncio.gather to fetch products for all stores concurrently
    results = await asyncio.gather(*(fetch_best_for_store(store) for store in stores))
    # Filter out any None results
    prices = [result for result in results if result]

    return prices


async def fetch_best_prices_old(term: str, stores: List) -> List[Dict]:
    """Retrieves items from the closest stores, finds the cheapest, and returns a parsed list of dicts.

    Args:
        term (str): the search term for the item being searched
        zip_code (str): The zip code to search near.

    Returns:
        List[Dict]: A list of dictionaries each containing a specific store and the cheapest product.
    """

    prices = []

    logging.info(f"Searching {len(stores)} stores for {term}")

    for store in stores:
        logging.info(f"Searching {store.name} for {term}...")
        products = await fetch_products_by_term(term, store.api_reference)
        logging.info(f"Found {len(products)} products")

        # Ensure products is a list and not empty
        if not products or not isinstance(products, list):
            logging.error(
                f"No products found for {term} in {store.name} or not recognizing as list..."
            )
            logging.info(f"Skipping {store.name}...")
            continue

        best_deal = None
        best_deal_price = float("inf")  # Set an initial high value for comparison

        for product in products:
            logging.info(f'Checking {product["description"]}...')
            # Guard against potential missing keys or data structures
            items = product.get("items", [])
            if not items:
                logging.error(f"{product}")
                continue

            current_price = items[0].get("price", {}).get("regular", float("inf"))

            if current_price < best_deal_price:
                best_deal = product
                best_deal_price = current_price

        # Ensure we found a valid best deal before appending
        if best_deal and best_deal_price < float("inf"):
            parsed_product = parse_product_data(best_deal)
            print(f"Found best deal: {parsed_product}")
            prices.append({"store": store, "product": parsed_product})

    return prices


async def fetch_locations() -> List[Dict]:
    headers = refresh_headers()
    req_url = f"{BASE_URL}/locations"

    data = await try_request_data(req_url, headers=headers)

    if data:
        return data
    else:
        logging.error("No locations found.")
        return []
