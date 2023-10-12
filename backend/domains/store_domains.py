from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# Domain dataclass for Chain model
@dataclass
class ChainDomain:
    id: int
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
# Domain dataclass for StoreLocation model
@dataclass
class StoreLocationDomain:
    id: int
    chain_id: int
    api_reference: str
    zip_code: str
    address: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Domain dataclass for PricePerProductStore model
@dataclass
class StorePrice:
    id: int
    product_id: int
    store_id: int
    price: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    