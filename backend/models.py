from datetime import datetime
from backend.database import db

# Search model
class Search(db.Model):
    __tablename__ = 'Search'
    
    SearchID = db.Column(db.Integer, primary_key=True)
    Term = db.Column(db.String(255), nullable=False)
    ZipCode = db.Column(db.String(10), nullable=False)
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    LastModified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    store_prices = db.relationship("StorePrice", back_populates="search")

# Product model
class Product(db.Model):
    __tablename__ = 'Product'
    
    ProductID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    UPC = db.Column(db.String(50), unique=True, nullable=False)
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    LastModified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    store_prices = db.relationship("StorePrice", back_populates="product")

# Store model
class Store(db.Model):
    __tablename__ = 'Store'
    
    StoreID = db.Column(db.Integer, primary_key=True)
    Chain = db.Column(db.String(20), nullable=False)
    StoreAPIRef = db.Column(db.String(255))
    Name = db.Column(db.String(255))
    Address = db.Column(db.String(500))
    ZipCode = db.Column(db.String(10))
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    LastModified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    product_prices = db.relationship("StorePrice", back_populates="store")
    
# Association tables
class StorePrice(db.Model):
    __tablename__ = "StorePrice"
    
    StorePriceID = db.Column(db.Integer, primary_key=True)
    Price = db.Column(db.Float(precision=2))
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    LastModified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign keys
    SearchID = db.Column(db.Integer, db.ForeignKey("Search.SearchID"))
    ProductID = db.Column(db.Integer, db.ForeignKey("Product.ProductID"))
    StoreID = db.Column(db.Integer, db.ForeignKey("Store.StoreID"))

    # Relationships
    search = db.relationship("Search", back_populates="store_prices")
    product = db.relationship("Product", back_populates="store_prices")
    store = db.relationship("Store", back_populates="product_prices")