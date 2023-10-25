import asyncio
import time
import logging
from services import (
    fetch_products_by_term,
    refresh_token,
    token_cache,
    fetch_locations,
    fetch_best_prices,
)

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Store:
    def __init__(self, name, api_reference):
        self.name = name
        self.api_reference = api_reference


# results = asyncio.run(fetch_products_by_term("apple", "70300656"))
# print(results)


# asyncio.run(refresh_token())
# print(token_cache)


# term = "apple"
# store_id = "70300656"  # Replace with a valid store ID for testing
# results = asyncio.run(fetch_products_by_term(term, store_id))
# print(results)


# locations = asyncio.run(fetch_locations())
# print(locations)


term = "apple"
# Replace with a list of mock store objects or dictionaries for testing
stores = [
    Store("Store 1", "70300656"),
    Store("Store 2", "70300271"),
    Store("Store 3", "70400779"),
]

start_time = time.time()  # Capture the start time

best_prices = asyncio.run(fetch_best_prices(term, stores))

end_time = time.time()  # Capture the end time

duration = end_time - start_time  # Calculate the duration

print(f"Time taken to fetch best prices: {duration:.2f} seconds")
print(best_prices)






