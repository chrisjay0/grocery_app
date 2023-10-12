-- User table
CREATE TABLE "User" (
    "UserID" SERIAL PRIMARY KEY,
    "Username" VARCHAR(255) NOT NULL UNIQUE,
    "Password" VARCHAR(255) NOT NULL,
    "Email" VARCHAR(255) NOT NULL UNIQUE,
    "CreatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "LastModified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- UserPreference table
CREATE TABLE "UserPreference" (
    "PreferenceID" SERIAL PRIMARY KEY,
    "UserID" INTEGER NOT NULL REFERENCES "User"("UserID"),
    "AppSetting" VARCHAR(255),
    "DietaryPreference" VARCHAR(255),
    "ZipCode" VARCHAR(10),
    "MaxTravelDistance" DECIMAL(5,2), -- Assuming distance in miles or kilometers with two decimal precision
    "CreatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "LastModified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- UserList table
CREATE TABLE "UserGrocerylist" (
    "ListID" SERIAL PRIMARY KEY,
    "UserID" INTEGER NOT NULL REFERENCES "User"("UserID"),
    "SearchTermsAndQuantities" JSONB,
    "CreatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "LastModified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chain table
CREATE TABLE "Chain" (
    "ChainID" SERIAL PRIMARY KEY,
    "Name" VARCHAR(255) NOT NULL UNIQUE,
    "CreatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "LastModified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- StoreLocation table
CREATE TABLE "StoreLocation" (
    "StoreLocationID" SERIAL PRIMARY KEY,
    "ChainID" INTEGER NOT NULL REFERENCES "Chain"("ChainID"),
    "StoreAPIRef" INTEGER,
    "Address" VARCHAR(500),
    "ZipCode" VARCHAR(10),
    "CreatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "LastModified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PricePerProductStore table
CREATE TABLE "PricePerProductStore" (
    "PriceID" SERIAL PRIMARY KEY,
    "ProductID" INTEGER NOT NULL REFERENCES "Product"("ProductID"),
    "StoreLocationID" INTEGER NOT NULL REFERENCES "StoreLocation"("StoreLocationID"),
    "Price" DECIMAL(10,2),
    "CreatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "LastModified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Product table
CREATE TABLE "Product" (
    "ProductID" SERIAL PRIMARY KEY,
    "Name" VARCHAR(255) NOT NULL,
    "UPC" VARCHAR(50) UNIQUE,
    "CreatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "LastModified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Attribute table
CREATE TABLE "Attribute" (
    "AttributeID" SERIAL PRIMARY KEY,
    "Description" VARCHAR(255) NOT NULL UNIQUE,
    "CreatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "LastModified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ProductAttribute table
CREATE TABLE "ProductAttribute" (
    "ProductAttributeID" SERIAL PRIMARY KEY,
    "ProductID" INTEGER NOT NULL REFERENCES "Product"("ProductID"),
    "AttributeID" INTEGER NOT NULL REFERENCES "Attribute"("AttributeID"),
    "CreatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "LastModified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PricePerProductStore table
CREATE TABLE "PricePerProductStore" (
    "PriceID" SERIAL PRIMARY KEY,
    "ProductID" INTEGER NOT NULL REFERENCES "Product"("ProductID"),
    "StoreLocationID" INTEGER NOT NULL REFERENCES "StoreLocation"("StoreLocationID"),
    "Price" DECIMAL(10,2),
    "CreatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "LastModified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- UserProductFavorite table
CREATE TABLE "UserProductFavorite" (
    "FavoriteID" SERIAL PRIMARY KEY,
    "UserID" INTEGER NOT NULL REFERENCES "User"("UserID"),
    "ProductID" INTEGER NOT NULL REFERENCES "Product"("ProductID"),
    "CreatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "LastModified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- UserList table
CREATE TABLE "UserProductlist" (
    "ListID" SERIAL PRIMARY KEY,
    "UserID" INTEGER NOT NULL REFERENCES "User"("UserID"),
    "SearchTermsAndQuantities" JSONB,
    "CreatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "LastModified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
