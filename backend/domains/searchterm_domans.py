from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from models.searchterm_models import SearchTerm


# Domain dataclass for search term  model
@dataclass
class SearchTermDomain:
    id: int
    term: str
    zip_code: str
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_orm(cls, orm: SearchTerm) -> Optional['SearchTermDomain']:
        if orm is None:
            return None
        return SearchTermDomain(
            id=orm.SearchTermID,
            term=orm.Term,
            zip_code=orm.ZipCode,
            created_at=orm.CreatedDate,
            updated_at=orm.LastModified,
        )

# Domain dataclass for grocery list model
@dataclass
class GroceryListDomain:
    id: int
    name: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    groceries: list[tuple(str, int)]
