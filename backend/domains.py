from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from backend.models import Search

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
    def from_orm(cls, orm: Search) -> Optional['SearchDomain']:
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
    id: int
    chain: str
    name: str
    address: str
    zip_code: str
    api_reference: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None