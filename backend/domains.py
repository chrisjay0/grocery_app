from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import decimal



from .models import Search, Store as StoreModel


# Domain dataclass for Product model
@dataclass
class ProductDomain:
    id: int
    name: str
    UPC: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Domain dataclass for search term  model
@dataclass
class SearchDomain:
    id: int
    term: str
    zip_code: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, orm: Search) -> Optional["SearchDomain"]:
        if orm is None:
            return None
        return SearchDomain(
            id=orm.SearchID,
            term=orm.Term,
            zip_code=orm.ZipCode,
            created_at=orm.CreatedDate,
            updated_at=orm.LastModified,
        )

    def __repr__(self):
        return f"SearchDomain(id={self.id}, term='{self.term}', zip_code='{self.zip_code}', created_at='{self.created_at:%Y-%m-%d %H:%M:%S}', updated_at='{self.updated_at:%Y-%m-%d %H:%M:%S}')"


# Domain dataclass for StoreLocation model
@dataclass
class StoreDomain:
    """Represents a store single store location"""

    id: Optional[int]
    chain: str
    name: str
    address: str
    zip_code: str
    latitude: decimal.Decimal
    longitude: decimal.Decimal
    api_reference: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_orm(cls, orm: StoreModel) -> Optional["StoreDomain"]:
        if orm is None:
            return None
        return StoreDomain(
            id=orm.StoreID,
            chain=orm.Chain,
            name=orm.Name,
            address=orm.Address,
            zip_code=orm.ZipCode,
            latitude=orm.Lat,
            longitude=orm.Long,
            api_reference=orm.StoreAPIRef,
        )
        
    def to_orm(self) -> StoreModel:
        return StoreModel(
            StoreID=self.id,
            Chain=self.chain,
            Name=self.name,
            Address=self.address,
            ZipCode=self.zip_code,
            Lat=self.latitude,
            Long=self.longitude,
            StoreAPIRef=self.api_reference,
        )
        
        