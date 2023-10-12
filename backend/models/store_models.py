from datetime import datetime
from database import db

# Chain model
class Chain(db.Model):
    __tablename__ = 'Chain'
    
    ChainID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), unique=True, nullable=False)
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    LastModified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# StoreLocation model
class StoreLocation(db.Model):
    __tablename__ = 'StoreLocation'
    
    StoreLocationID = db.Column(db.Integer, primary_key=True)
    ChainID = db.Column(db.Integer, db.ForeignKey('Chain.ChainID', ondelete='CASCADE'), nullable=False)
    StoreAPIRef = db.Column(db.String(255))
    Address = db.Column(db.String(500))
    ZipCode = db.Column(db.String(10))
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    LastModified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    products = db.relationship('StorePrice', backref='store')
    product_prices = db.relationship('StorePrice', backref='store_location')

# StorePrice model
# many-to-many relationship between Product and StoreLocation to store product price
class StorePrice(db.Model):
    __tablename__ = 'StorePrice'
    
    StorePriceID = db.Column(db.Integer, primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('Product.ProductID', ondelete='CASCADE'), nullable=False)
    StoreLocationID = db.Column(db.Integer, db.ForeignKey('StoreLocation.StoreLocationID'), nullable=False)
    Price = db.Column(db.Float(precision=2))
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    LastModified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
