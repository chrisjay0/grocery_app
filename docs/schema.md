# GroceryAppDB Schema Documentation

This document outlines the structure of the `groceryappdb` database, which was designed to support the Grocery Comparison App. The purpose of this app is to allow users to build a grocery list and then compare prices across multiple grocery stores.

## Tables

### 1. User

Represents the registered users of the app.

| Column Name  | Data Type    | Constraints |
|--------------|--------------|-------------|
| UserID      | SERIAL       | PRIMARY KEY |
| Username    | VARCHAR(255) | NOT NULL, UNIQUE |
| Password    | VARCHAR(255) | NOT NULL |
| Email       | VARCHAR(255) | NOT NULL, UNIQUE |
| CreatedDate | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |
| LastModified| TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |

### 2. UserPreference

Stores user-specific preferences, including app settings, dietary choices, and location-related preferences.

| Column Name       | Data Type    | Constraints |
|-------------------|--------------|-------------|
| PreferenceID      | SERIAL       | PRIMARY KEY |
| UserID            | INTEGER      | FOREIGN KEY REFERENCES User(UserID) |
| AppSetting        | VARCHAR(255) | |
| DietaryPreference | VARCHAR(255) | |
| ZipCode           | VARCHAR(10)  | |
| MaxTravelDistance | DECIMAL(5,2) | |
| CreatedDate       | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |
| LastModified      | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |

### 3. Chain

Represents grocery store chains.

| Column Name  | Data Type    | Constraints |
|--------------|--------------|-------------|
| ChainID      | SERIAL       | PRIMARY KEY |
| Name         | VARCHAR(255) | NOT NULL, UNIQUE |
| CreatedDate  | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |
| LastModified | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |

### 4. StoreLocation

Specific locations or branches of a given grocery store chain.

| Column Name     | Data Type    | Constraints |
|-----------------|--------------|-------------|
| StoreLocationID | SERIAL       | PRIMARY KEY |
| ChainID         | INTEGER      | FOREIGN KEY REFERENCES Chain(ChainID) |
| StoreAPIRef     | INTEGER      | |
| Address         | VARCHAR(500) | |
| ZipCode         | VARCHAR(10)  | |
| CreatedDate     | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |
| LastModified    | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |

### 5. Item

Represents individual grocery items available for purchase.

| Column Name  | Data Type    | Constraints |
|--------------|--------------|-------------|
| ItemID       | SERIAL       | PRIMARY KEY |
| Name         | VARCHAR(255) | NOT NULL |
| UPC          | VARCHAR(50)  | UNIQUE |
| CreatedDate  | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |
| LastModified | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |

### 6. Attribute

Describes specific attributes or characteristics that an item might have (e.g., organic, gluten-free).

| Column Name  | Data Type    | Constraints |
|--------------|--------------|-------------|
| AttributeID  | SERIAL       | PRIMARY KEY |
| Description  | VARCHAR(255) | NOT NULL, UNIQUE |
| CreatedDate  | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |
| LastModified | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |

### 7. ItemAttribute

Links items to their attributes. This allows items to have multiple attributes and attributes to be associated with multiple items.

| Column Name      | Data Type    | Constraints |
|------------------|--------------|-------------|
| ItemAttributeID  | SERIAL       | PRIMARY KEY |
| ItemID           | INTEGER      | FOREIGN KEY REFERENCES Item(ItemID) |
| AttributeID      | INTEGER      | FOREIGN KEY REFERENCES Attribute(AttributeID) |
| CreatedDate      | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |
| LastModified     | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |

### 8. PricePerItemStore

Represents the price of an item at a specific store location.

| Column Name      | Data Type    | Constraints |
|------------------|--------------|-------------|
| PriceID          | SERIAL       | PRIMARY KEY |
| ItemID           | INTEGER      | FOREIGN KEY REFERENCES Item(ItemID) |
| StoreLocationID  | INTEGER      | FOREIGN KEY REFERENCES StoreLocation(StoreLocationID) |
| Price            | DECIMAL(10,2)| |
| CreatedDate      | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |
| LastModified     | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |

### 9. UserItemFavorite

Stores items that users have marked as favorites.

| Column Name  | Data Type    | Constraints |
|--------------|--------------|-------------|
| FavoriteID   | SERIAL       | PRIMARY KEY |
| UserID       | INTEGER      | FOREIGN KEY REFERENCES User(UserID) |
| ItemID       | INTEGER      | FOREIGN KEY REFERENCES Item(ItemID) |
| CreatedDate  | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |
| LastModified | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |

### 10. UserList

Represents a user's grocery list, which includes the items and quantities they intend to purchase.

| Column Name              | Data Type    | Constraints |
|--------------------------|--------------|-------------|
| ListID                   | SERIAL       | PRIMARY KEY |
| UserID                   | INTEGER      | FOREIGN KEY REFERENCES User(UserID) |
| SearchTermsAndQuantities | JSONB        | |
| CreatedDate              | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |
| LastModified             | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP |

## Conclusion

The `groceryappdb` database is structured to provide comprehensive support for the Grocery Comparison App's functionalities, including user registration, preferences management, item attributes, pricing, and more. The design ensures flexibility and scalability for future enhancements.
