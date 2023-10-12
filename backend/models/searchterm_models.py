from datetime import datetime
from database import db

# SearchTerm model
class SearchTerm(db.Model):
    __tablename__ = 'SearchTerm'
    
    SearchTermID = db.Column(db.Integer, primary_key=True)
    Term = db.Column(db.String(255), nullable=False)
    ZipCode = db.Column(db.String(10), nullable=False)
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    LastModified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    store_products = db.relationship('StorePrice', secondary='SearchTermStorePrice', backref='SearchTerms')

# SearchTermStoreStorePrice model
class SearchTermStorePrice(db.Model):
    __tablename__ = 'SearchTermStorePrice'
    
    SearchTermStorePriceID = db.Column(db.Integer, primary_key=True)
    SearchTermID = db.Column(db.Integer, db.ForeignKey('SearchTerm.SearchTermID', ondelete='CASCADE'), nullable=False)
    StorePriceID = db.Column(db.Integer, db.ForeignKey('StorePrice.StorePriceID', ondelete='CASCADE'), nullable=False)
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    LastModified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    store_prices  = db.relationship('StorePrice', backref='search_term')
    
    
# Grocerylist model
class GroceryList(db.Model):
    __tablename__ = 'GroceryList'
    
    GroceryListID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID', ondelete='CASCADE'), nullable=False)
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    LastModified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    search_terms = db.relationship('GroceryListSearchTerm', backref='grocery_lists')
    user = db.relationship('User', backref='grocery_lists')
    
# GrocerylistSearchTerm model
class GroceryListSearchTerm(db.Model):
    __tablename__ = 'GroceryListSearchTerm'
    
    GroceryListSearchTermID = db.Column(db.Integer, primary_key=True)
    GroceryListID = db.Column(db.Integer, db.ForeignKey('GroceryList.GroceryListID', ondelete='CASCADE'), nullable=False)
    SearchTermID = db.Column(db.Integer, db.ForeignKey('SearchTerm.SearchTermID', ondelete='CASCADE'), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    LastModified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
