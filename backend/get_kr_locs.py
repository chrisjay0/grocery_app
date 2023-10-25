from decouple import config
import base64
from typing import Dict, List
import requests
from backend.util import update_stores

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

#######################################################################################


url = "https://api.kroger.com/v1/connect/oauth2/token"
credentials = f"{config('KROGER_ID')}:{config('KROGER_SECRET')}"
encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
payload = {}
headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}",
    }
token_data = {"grant_type": "client_credentials", "scope": "product.compact"}

response = requests.request("POST", url, headers=headers, data=token_data)

token = response.json()["access_token"]


url = "https://api.kroger.com/v1/locations"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
response = requests.request("GET", url, headers=headers)

unparsed_stores = response.json()["data"]

parse_stores = parse_stores(unparsed_stores)

update_stores(parse_stores(unparsed_stores))
