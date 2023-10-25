from backend.services import parse_stores, fetch_locations
from backend.util import update_stores

update_stores(parse_stores(fetch_locations()))
