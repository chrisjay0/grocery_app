from datetime import datetime
from database import db

# Product model
class Product(db.Model):
    __tablename__ = 'Product'
    
    ProductID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    UPC = db.Column(db.String(50), unique=True)
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    LastModified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    store_prices = db.relationship('StorePrice', backref='product')

# Attribute model
class Attribute(db.Model):
    __tablename__ = 'Attribute'
    
    AttributeID = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.String(255), unique=True, nullable=False)
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    LastModified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    products = db.relationship('ProductAttribute', backref='attribute')

# ProductAttribute model
class ProductAttribute(db.Model):
    __tablename__ = 'ProductAttribute'
    
    ProductAttributeID = db.Column(db.Integer, primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('Product.ProductID', ondelete='CASCADE'), nullable=False)
    AttributeID = db.Column(db.Integer, db.ForeignKey('Attribute.AttributeID', ondelete='CASCADE'), nullable=False)
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    LastModified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
