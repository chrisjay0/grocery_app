import sys
print(sys.path)


from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

# Domain dataclass for Product model
@dataclass
class ProductDomain:
    id: int
    name: str
    UPC: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    attributes: Optional[list[str]] = None
    
# Domain dataclass for Attribute model
@dataclass
class AttributeDomain:
    id: int
    description: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None