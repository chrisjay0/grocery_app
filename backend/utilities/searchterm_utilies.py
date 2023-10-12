from datetime import datetime, timedelta

from models.searchterm_models import SearchTerm, SearchTermStorePrice
from models.store_models import StorePrice
from models.product_models import Product
from database import db
from services.food4less import
from services.sprouts import


def search_item(term: str, zip_code: str):
    # Step 2: Check if the term has been searched today at that ZipCode
    day_old = datetime.utcnow() - timedelta(days=1)

    search_term = (
        SearchTerm.query.filter_by(Term=term, ZipCode=zip_code)
        .filter(SearchTerm.LastModified > day_old)
        .first()
    )

    if search_term:
        return fetch_prices_for_search_term(search_term)

    # Step 4: Search the term at the ZipCode via the API
    api_results = make_api_call(
        term, zip_code
    )  # Assuming you have a function called make_api_call

    # Step 5: Insert/Update the result in the database
    handle_database_updates(api_results, term, zip_code)

    # Step 6: Return the result
    return api_results


def fetch_prices_for_search_term(search_term: SearchTerm):
    store_prices = (
        search_term.store_products
    )
    prices_data = []
    for store_price in store_prices:
        store_info = {
            "store_name": store_price.Store.StoreName,
            "product_name": store_price.Product.ProductName,
            "price": store_price.Price,
        }
        prices_data.append(store_info)

    return prices_data


def handle_database_updates(search_term_str: str, zip_code: str, api_results: dict):
    # Check if SearchTerm already exists in the database
    existing_search_term = SearchTerm.query.filter_by(
        Term=search_term_str, ZipCode=zip_code
    ).first()

    # If SearchTerm does not exist or was last updated more than 24 hours ago, fetch fresh data
    if not existing_search_term or (
        datetime.utcnow() - existing_search_term.LastModified > timedelta(days=1)
    ):
        if not existing_search_term:
            new_search_term = SearchTerm(Term=search_term_str, ZipCode=zip_code)
            db.session.add(new_search_term)
        else:
            new_search_term = existing_search_term

        # Iterate over products in api_results
        for product_data in api_results["products"]:
            # Check if Product already exists in the database
            product = Product.query.filter_by(
                ProductName=product_data["description"]
            ).first()
            if not product:
                product = Product(ProductName=product_data["description"])
                db.session.add(product)

            # Check if Store already exists
            store = Store.query.filter_by(StoreName=product_data["store"]).first()
            if not store:
                store = Store(StoreName=product_data["store"])
                db.session.add(store)

            # Check if StorePrice exists for this product-store combination
            store_price = StorePrice.query.filter_by(
                StoreID=store.StoreID, ProductID=product.ProductID
            ).first()
            if not store_price:
                store_price = StorePrice(
                    StoreID=store.StoreID,
                    ProductID=product.ProductID,
                    Price=product_data["price"],
                )
                db.session.add(store_price)
            else:
                store_price.Price = product_data["price"]

            # Update relationships
            new_search_term.store_products.append(store_price)

        # Commit the changes to the database
        db.session.commit()

        return new_search_term
    else:
        # If data is up-to-date, simply return the existing search term
        return existing_search_term
