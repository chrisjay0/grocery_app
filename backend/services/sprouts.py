import requests
from typing import Dict, List

def fetch_sprouts_prices(item_names: List[str]) -> Dict:

    def getItemDict(item: str) -> dict:
        
        url = f"https://shop.sprouts.com/api/v2/store_products?limit=12&offset=0&search_term={item}&sort=rank"

        payload = {}
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'Cookie': 'session-sprouts=.eJwdjslugzAARP_F5zSqabNxqyKU2gqmISQGLoiAUUzMUmwCdtV_r9XDXN5oNO8HZNXA5B24VS4kW4CsZ0OTt6xVwFXDaIlkUvKuzVT3YC1wAdP4fjsUPOAYXQyChOPd0kJYOFdtYwpHPG9i16d7tEYNbpLI06S56GMkHunBU-Rwek_PkBPjGctEEuE6bdBETDHZjUTt1aQxrnJ64kGNtG-82XYzOU88oaHK6er_K3bEA9X9WNJZHvdWqtmNjMJnGfs8aENd0otEjbiX1sOPkhWpk8mvTyaIX5el48zbbfVFVB9-B7NPi49PHIRaYB2b6dkVa_riqeNa6A4swCjZkPESuI7zBuFmA1e_f8WMbMI.GAXyDw.gBrNKcw1l-KoF1RRVHhU1avAJ5k; __cf_bm=RnTb1SfDIx0r0tPb4OMwPzGN4MhLeRizpY6ELZOEax8-1696897678-0-Aahy/HcyQ8d60m2h+8aUU5/6H8N91ysNU7JF3rsoB2fI83G7XwNUgJ1DAt5B7I3qsw7kWZwEjzgo6LGctvZOBvU='
            }

        response = requests.request("GET", url, headers=headers, data=payload)
        
        def extract_lowest_price_product(data):
            """
            Extracts the item with the lowest price from the given JSON structure.

            Args:
            - data (dict): The JSON structure containing product information.

            Returns:
            - dict: A dictionary with the name of the product with the lowest price as the key 
                    and its base price as the value.
            """
            items = data.get('items', [])
            if not items:
                return {}

            # Extract the name and base price of each product into a dictionary
            product_prices = {item['name']: item['base_price'] for item in items}

            # Find the item with the lowest price
            lowest_price_product = min(product_prices, key=product_prices.get)
            
            return {lowest_price_product: product_prices[lowest_price_product]}

        return extract_lowest_price_product(response.json())

    def createDictOfItemPrices(items: List[str]) -> Dict:
        prices = {}
        for item in items:
            prices.update(getItemDict(item))
        return {"Sprouts": prices}
    
    return createDictOfItemPrices(item_names)

print(fetch_sprouts_prices(['tofu']))