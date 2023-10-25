from sqlalchemy import func
import decimal
from typing import List

from .models import StoreModel
from .domains import StoreDomain
from .services.kroger.util import KROGER_CHAINS, fetch_best_kroger_price
from .database import db








R = 6371  # Radius of the Earth in kilometers

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the Haversine distance."""
    dlat = func.radians(lat2 - lat1)
    dlon = func.radians(lon2 - lon1)
    a = func.sin(dlat / 2) * func.sin(dlat / 2) + func.cos(func.radians(lat1)) * func.cos(func.radians(lat2)) * func.sin(dlon / 2) * func.sin(dlon / 2)
    c = 2 * func.atan2(func.sqrt(a), func.sqrt(1 - a))
    distance = R * c
    return distance

def fetch_prices_nearby_stores(term: str, stores: List[StoreDomain]) -> List[dict]:
    prices = []
    for store in stores:
        if store.chain in KROGER_CHAINS:
            prices.append(fetch_best_kroger_price(term=term, store_id=store.api_reference))
            
    return prices

# Store Domain Utilities
class StoreUtils:
    @classmethod
    def get_closest_stores(
        cls, lat: decimal.Decimal, lon: decimal.Decimal, limit: int = 5
    ) -> List[StoreDomain]:
        """Get the closest stores to a given lat/lon"""

        session = db.session
        
        subq = session.query(
            StoreModel,
            haversine(StoreModel.Lat, StoreModel.Long, lat, lon).label("distance"),
            func.row_number().over(partition_by=StoreModel.Chain, order_by=haversine(StoreModel.Lat, StoreModel.Long, lat, lon)).label("row_num")
        ).subquery()
        
        closest_stores = session.query(subq).filter(subq.c.row_num == 1).order_by(subq.c.distance).limit(3).all()
        
        return [StoreDomain.from_orm(store) for store in closest_stores]