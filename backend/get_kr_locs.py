from backend.services import parse_stores, fetch_locations
from backend.util import update_stores
import asyncio



unparsed_stores = asyncio.run(fetch_locations())

update_stores(parse_stores(unparsed_stores))
