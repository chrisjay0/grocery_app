from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# Domain dataclass for User model
@dataclass
class UserDomain:
    id: int
    username: str
    password: str
    email: str
    favorite_product_ids: Optional[list[int]] = None
    grocery_list_ids: Optional[list[int]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Domain dataclass for UserPreference model
@dataclass
class UserPreferenceDomain:
    id: int
    user: UserDomain
    app_settings: str = None
    dietary_preferences: str = None
    zip_code: str = None
    max_travel_distance: int = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

