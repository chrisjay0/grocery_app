from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import desc, func
from sqlalchemy.exc import SQLAlchemyError
import logging
import requests
from geopy.geocoders import Nominatim
from decimal import Decimal




from .models import Search as SearchModel, StorePrice, Product, Store, Store as StoreModel
from .domains import SearchDomain, StoreDomain
from .database import db
from .services import fetch_best_prices, fetch_locations, parse_stores

from sqlalchemy import func
import decimal
from typing import List

# from .services.kroger.util import KROGER_CHAINS, fetch_best_kroger_price
from .database import db
# from app import app








R = 6371  # Radius of the Earth in kilometers

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the Haversine distance."""
    dlat = func.radians(lat2 - lat1)
    dlon = func.radians(lon2 - lon1)
    a = func.sin(dlat / 2) * func.sin(dlat / 2) + func.cos(func.radians(lat1)) * func.cos(func.radians(lat2)) * func.sin(dlon / 2) * func.sin(dlon / 2)
    c = 2 * func.atan2(func.sqrt(a), func.sqrt(1 - a))
    distance = R * c
    return distance

# def fetch_prices_nearby_stores(term: str, stores: List[StoreDomain]) -> List[dict]:
#     prices = []
#     for store in stores:
#         if store.chain in KROGER_CHAINS:
#             prices.append(fetch_best_kroger_price(term=term, store_id=store.api_reference))
            
#     return prices

# Store Domain Utilities
class StoreUtils:
    @classmethod
    def get_closest_stores(
        cls, lat: decimal.Decimal, lon: decimal.Decimal, limit: int = 3
    ) -> List[StoreDomain]:
        """Get the closest stores to a given lat/lon"""
        try:
            logging.info('Initiating db session...')
            session = db.session
            
            logging.info('Attempting query one...')
            subq = session.query(
                StoreModel,
                haversine(StoreModel.Lat, StoreModel.Long, lat, lon).label("distance"),
                func.row_number().over(partition_by=StoreModel.Chain, order_by=haversine(StoreModel.Lat, StoreModel.Long, lat, lon)).label("row_num")
            ).subquery()
            
            logging.info('Attempting query two...')
            closest_stores = session.query(subq).filter(subq.c.row_num == 1).order_by(subq.c.distance).limit(limit).all()
            
            logging.info('Attempting to return store domains from results...')
            return [StoreDomain.from_orm(store) for store in closest_stores]
        
        except Exception as e:
            logging.error(f"An unexpected error occurred while finding closest stores. Error: {e}")
            return []


def get_lat_lon(zip_code: str) -> tuple[Decimal, Decimal]:
    """
    Get latitude and longitude for a given zip code.

    Args:
        zip_code (str): Zip code to get latitude and longitude for

    Returns:
        tuple: Tuple of latitude and longitude
    """
    url = f"https://nominatim.openstreetmap.org/search?format=json&accept-language=en&zoom=3&postalcode={zip_code}&country=united states"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()[0]
    
    lat = data['lat']
    lon = data['lon']
    
    return (lat, lon)


def get_youngest_search(term: str, zip_code: str) -> SearchDomain | None:
    """
    Get the youngest search for a term and zip code combination. If no term and zip code combination is found, return None.
    
    Args:
        term (str): String representing a search for product
        zip_code (str): Zip code to search for products nearby

    Returns:
        SearchDomain | None
    """

    session = db.session
    
    try:
        result = session.query(SearchModel).filter(
            SearchModel.Term == term,
            SearchModel.ZipCode == zip_code
        ).order_by(desc(SearchModel.LastModified)).first()
        
        if result:
            return SearchDomain.from_orm(result)
        else:
            return None
            
    except Exception as e:
        print(e)
        return None
        
    finally:
        session.close()
    






def fetch_db_prices_search(search: SearchDomain) -> Optional[List[dict]]:
    """
    Fetches prices from database for a given search.

    Args:
        search (SearchDomain): SearchDomain object representing a search

    Returns:
        List[dict]: List of dictionaries representing store and product details.
    """

    session = db.session
    
    try:
        # Query based on the search ID
        results = session.query(StorePrice).filter(StorePrice.SearchID == search.id).all()
        
        # Transform results into desired format
        prices = [
            {
                "store": {
                    "name": price.store.Name,
                    # Add other store details here if needed
                },
                "product": {
                    "name": price.product.Name,
                    # Add other product details here if needed
                },
                "price": price.Price
            }
            for price in results
        ]
        
        return prices if prices else None
            
    except Exception as e:
        print(e)
        return None
        
    finally:
        session.close()

def save_search_data(search_domain: SearchDomain, data: List[dict]) -> SearchDomain | None:
    """
    Saves a new search entry in the database and creates or updates related entries.

    Args:
        search_domain (SearchDomain): SearchDomain object representing a search.
        data (List[dict]): List of dictionaries with store and product details.

    Returns:
        bool: True if successful, False otherwise.
    """

    session = db.session

    try:
        # check if it is an existing search entry
        if search_domain.id:
            search_entry = session.query(SearchModel).get(search_domain.id)
            
        # if it's not existing we create a new one
        else:
            search_entry = SearchModel(Term=search_domain.term, ZipCode=search_domain.zip_code)
            session.add(search_entry)
            session.flush()

        logging.info('Attempting to begin for loop for data list...')
        for item in data:
            logging.info('Attempting to extract store from item...')
            store_data = item['store']
            product_data = item['product']

            
            logging.info('Attempting to fetch or create store...')
            # Fetch or create Store
            store = session.query(Store).filter_by(Name=store_data.name).first()
            if not store:
                store = store_data.to_orm()
                session.add(store)

            # Fetch or create Product
            logging.info('Attempting to fetch or create product...')
            product = session.query(Product).filter_by(UPC=product_data['UPC']).first()
            if not product:
                product = Product(
                    Name=product_data['name'],
                    UPC=product_data['UPC']
                )
                session.add(product)

            # Commit to get IDs for the newly created store and product if needed
            logging.info('Attempting to flush to create unique IDs...')
            session.flush()

            # Fetch or create StorePrice
            logging.info('Attempting to fetch or create store price...')
            store_price = session.query(StorePrice).filter_by(
                SearchID=search_entry.SearchID, 
                ProductID=product.ProductID, 
                StoreID=store.StoreID
            ).first()

            if not store_price:
                store_price = StorePrice(
                    SearchID=search_entry.SearchID, 
                    ProductID=product.ProductID, 
                    StoreID=store.StoreID,
                    Price=product_data['price']
                )
                session.add(store_price)
            else:
                store_price.Price = product_data['price']

        session.commit()
        return SearchDomain.from_orm(search_entry)

    except Exception as e:
        print(f"Exception in save_search_data: {e}")
        print(e)
        session.rollback()
        return None

    finally:
        session.close()

def get_prices(term: str, zip_code: str, lat: Decimal, lon: Decimal) -> List[dict]:
    """
    Checks for matching fresh searches.
    - if fresh search found return prices in dict
    - if stale or no search found, call api's and update search and prices
    
    Args:
        term (str): String representing a search for product
        zip_code (str): Zip code to search for products nearby

    Returns:
        List[dict]
    """
    try:
        search = get_youngest_search(term, zip_code)

        # Check if a search found is fresh
        if search:
            day_old = datetime.now() - timedelta(days=1)
            print(f'Found search: {search.updated_at} vs {day_old}')
            if search.updated_at > day_old:
                
                print(f'returning search fresh search')
                return fetch_db_prices_search(search)
        
        # Stale or no search found, fetching from API
        logging.info('Search not found or stale, fetching from API...')
        
        logging.info('Attempting to find closest stores from db...')
        stores = StoreUtils.get_closest_stores(lat=lat, lon=lon)
        logging.info(f'Results: {len(stores)} stores found.')
        
        logging.info('Attempting to fetch prices from kroger...')
        results = fetch_best_prices(term=term, stores=stores)
        
        logging.info(f'Results: {len(results)} prices found')
        logging.info(f'Results: {results}')
        
        if not results:
            logging.warning(f"No results found for term: {term}, zip_code: {zip_code}")
            return []
        
        # If a search was found but it's stale, reuse it
        # Otherwise, create a new one
        if not search:
            search_model = SearchModel(Term=term, ZipCode=zip_code)
            search = SearchDomain.from_orm(search_model)
            
        # Save the search and price
        saved = save_search_data(search, results)
        
        if not saved:
            logging.error(f"Failed to save search data for term: {term}, zip_code: {zip_code}")
            return []

        # Return the prices for the new search
        return fetch_db_prices_search(saved)

    except SQLAlchemyError:
        logging.error(f"Database error occurred while fetching prices for term: {term}, zip_code: {zip_code}")
        return []

    except requests.exceptions.RequestException:
        logging.error(f"Connection error while fetching prices for term: {term}, zip_code: {zip_code}")
        return []

    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching prices for term: {term}, zip_code: {zip_code}. Error: {e}")
        return []
    
def update_stores(stores: List[dict]) -> None:
    """
    Updates stores in the database.

    Args:
        stores (List[dict]): List of dictionaries with store details.
    """
    session = db.session
    
    try:
        for store in stores:
            # Fetch or create Store
            store_entry = session.query(Store).filter_by(StoreAPIRef=store['api_reference'], Chain=store['chain']).first()
            if not store_entry:
                store_entry = Store(
                    StoreAPIRef=store['api_reference'],
                    Name=store['name'],
                    Chain=store['chain'],
                    ZipCode=store['zip_code'],
                    Address=store['address'],
                    Lat=store['latitude'],
                    Long=store['longitude']
                )
                session.add(store_entry)
            else:
                store_entry.Name = store['name']
                store_entry.Chain = store['chain']
                store_entry.ZipCode = store['zip_code']
                store_entry.Address = store['address']
                store_entry.Lat = store['latitude']
                store_entry.Long = store['longitude']
            
            session.flush()
            
        session.commit()
        print('Stores updated successfully')
        
    except Exception as e:
        print(e)
        session.rollback()
        

    
# with app.app_context():
    
#     url = "https://nominatim.openstreetmap.org/search?format=json&accept-language=en&zoom=3&postalcode=93401&country=united states"

#     payload = {}
#     headers = {}

#     response = requests.request("GET", url, headers=headers, data=payload)
#     data = response.json()[0]
#     dic = {}
#     dic['lat'] = data['lat']
#     dic['lon'] = data['lon']
    
#     # print(dic['lat'])
#     # print(response.json())
#     # print(response.json())
    
#     # Haversine formula components
#     R = 6371  # Radius of the Earth in kilometers

#     def haversine(lat1, lon1, lat2, lon2):
#         """Calculate the Haversine distance."""
#         dlat = func.radians(lat2 - lat1)
#         dlon = func.radians(lon2 - lon1)
#         a = func.sin(dlat / 2) * func.sin(dlat / 2) + func.cos(func.radians(lat1)) * func.cos(func.radians(lat2)) * func.sin(dlon / 2) * func.sin(dlon / 2)
#         c = 2 * func.atan2(func.sqrt(a), func.sqrt(1 - a))
#         distance = R * c
#         return distance

#     # Given latitude and longitude
#     given_lat = dic['lat']
#     given_lon = dic['lon']

#     # Create a session
#     session = db.session

#     # # Query to find the closest store
#     # closest_store = session.query(Store).order_by(haversine(Store.Lat, Store.Long, given_lat, given_lon)).first()

#     # Subquery for distance and row number
#     subq = session.query(
#         Store,
#         haversine(Store.Lat, Store.Long, given_lat, given_lon).label("distance"),
#         func.row_number().over(partition_by=Store.Chain, order_by=haversine(Store.Lat, Store.Long, given_lat, given_lon)).label("row_num")
#     ).subquery()

#     # Main query to get the three closest stores with unique "Chain"
#     closest_stores = session.query(subq).filter(subq.c.row_num == 1).order_by(subq.c.distance).limit(3).all()

#     for store in closest_stores:
#         print(store.Name)

    
    
#     # update_stores(parse_stores(fetch_locations()))
    
#     # def get_country(lat, lon):
#     #     url = f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&accept-language=en&zoom=3'
#     #     try:
#     #         result = requests.get(url=url)
#     #         result_json = result.json()
#     #         return result_json['display_name']
#     #     except:
#     #         return None

#     # print(get_country(32.782023,35.478867)) # results in Israel
