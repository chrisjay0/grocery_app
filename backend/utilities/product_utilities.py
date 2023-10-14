import sys
print(sys.path)


from domains.product_domains import ProductDomain
from domains.store_domains import StoreLocationDomain
from domains.searchterm_domans import SearchTermDomain
from models.searchterm_models import SearchTerm as SearchTermModel
from typing import Dict, List
from sqlalchemy import desc




def update_product_search(term: str, zip_code: str, store: Dict, product: Dict) -> None:
    
    search_term = SearchTermDomain(term=term, zip_code=zip_code)
    product = ProductDomain(name=product['name'], UPC=product['UPC'])
    store = StoreLocationDomain(name=store['name'], store_number=store['store_number'])
    
## unsure of name maybe: get_stored_search_if_fresh 
def check_fresh_searches(term: str, zip_code: str, age_hours: int = 24) -> List[Dict] | None:
    """
    Check recent searches for a term and zip code. If a term and zip code combination is found younger than age (default 24 hours), return a list of products. If no term and zip code combination is found younger than age, return None.
    
    Args:
        term (str): String representing a search for product
        zip_code (str): Zip code to search for products nearby
        age_hours (int, optional): Age limit for searches in hours. Defaults to 24.

    Returns:
        List[Dict] | None
    """
    
    pass

def get_youngest_search(term: str, zip_code: str) -> SearchTermDomain | None:
    """
    Get the youngest search for a term and zip code combination. If no term and zip code combination is found, return None.
    
    Args:
        term (str): String representing a search for product
        zip_code (str): Zip code to search for products nearby

    Returns:
        SearchTermDomain | None
    """
    # class SearchTerm(db.Model):
    #     __tablename__ = 'SearchTerm'
        
    #     SearchTermID = db.Column(db.Integer, primary_key=True)
    #     Term = db.Column(db.String(255), nullable=False)
    #     ZipCode = db.Column(db.String(10), nullable=False)
    #     CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    #     LastModified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    #     store_products = db.relationship('StorePrice', secondary='SearchTermStorePrice', backref='SearchTerms')
    
    youngest_search = SearchTermModel.query.filter_by(Term=term, ZipCode=zip_code).order_by(desc(SearchTermModel.CreatedDate)).first()
    
    return youngest_search
    
print(get_youngest_search('milk','93401'))