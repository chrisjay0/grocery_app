from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
import logging
import requests

from models import Search as SearchModel, StorePrice, Product, Store
from domains import SearchDomain
from database import db
from services import fetch_best_prices


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

        for item in data:
            store_data = item['store']
            product_data = item['product']

            # Fetch or create Store
            store = session.query(Store).filter_by(Name=store_data['name']).first()
            if not store:
                store = Store(
                    StoreAPIRef=store_data['api_reference'],
                    Name=store_data['name'],
                    Chain=store_data['chain'],
                    ZipCode=store_data['zip_code'],
                    Address=store_data['address']
                )
                session.add(store)

            # Fetch or create Product
            product = session.query(Product).filter_by(UPC=product_data['UPC']).first()
            if not product:
                product = Product(
                    Name=product_data['name'],
                    UPC=product_data['UPC']
                )
                session.add(product)

            # Commit to get IDs for the newly created store and product if needed
            session.flush()

            # Fetch or create StorePrice
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
        print(e)
        session.rollback()
        return None

    finally:
        session.close()

def get_prices(term: str, zip_code: str) -> List[dict]:
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
            if search.updated_at > day_old:
                return fetch_db_prices_search(search)
        
        # Stale or no search found, fetching from API
        logging.info('Search not found or stale, fetching from API...')
        
        results = fetch_best_prices(term=term, zip_code=zip_code)
        
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
    
# from app import app
# with app.app_context():

#     print(get_prices('butter', '90001'))
    # print(get_youngest_search('bread', '90001'))
    # print(fetch_db_prices_search())
    # print(save_search_data(search, results))
    # print(save_search_data(search, results))
    # session = db.session
    # search_m = SearchModel(Term='test search', ZipCode='86753')
    # print(f'This is the search model: {search_m}')
    # search_d = SearchDomain.from_orm(search_m)
    # print(f'This is the search domain: {search_d}')


# from app import app
# with app.app_context():
#     print(get_prices('cereal', '45052'))
# #     # search_model = SearchModel(Term='milk', ZipCode='90001')
# #     # search = SearchDomain.from_orm(search_model)
# #     # data = fetch_best_prices(term=search.term, zip_code=search.zip_code)
# #     # save_search_data(search, data)